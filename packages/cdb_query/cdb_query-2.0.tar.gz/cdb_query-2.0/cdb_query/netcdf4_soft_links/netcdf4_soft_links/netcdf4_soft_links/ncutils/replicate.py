# External:
import numpy as np
import netCDF4
import logging

# Internal:
from .indices import slice_a_slice
from .core import (default, setncattr, getncattr, DEFAULT_MAX_REQUEST,
                   maybe_conv_bytes_to_str, maybe_conv_bytes_to_str_array)
from .dimensions import _is_dimension_present
from .time import find_time_dim, variables_list_with_time_dim
from .defaults import replicate as ncu_defaults
from .dataset_compat import (_isunlimited, _sanitized_datatype,
                             _dim_len, _shape)

try:
    import dask.array as da
    import dask
    with_dask = True
except ImportError:
    with_dask = False

_logger = logging.getLogger(__name__)


@default(mod=ncu_defaults)
def replicate_full_netcdf_recursive(dataset, output,
                                    transform=(lambda x, y, z: y),
                                    slices=dict(),
                                    check_empty=False,
                                    allow_dask=False,
                                    zlib=False):
    replicate_netcdf_file(dataset, output)

    for var_name in dataset.variables:
        replicate_and_copy_variable(dataset, output, var_name,
                                    transform=transform,
                                    slices=slices,
                                    check_empty=check_empty,
                                    allow_dask=allow_dask,
                                    zlib=zlib)
    for dim_name in dataset.dimensions:
        replicate_netcdf_dimension(dataset, output, dim_name,
                                   slices=slices, zlib=zlib)
    if len(dataset.groups.keys()) > 0:
        for group in dataset.groups:
            output_grp = replicate_group(dataset, output, group)
            replicate_full_netcdf_recursive(dataset.groups[group],
                                            output_grp,
                                            transform=transform,
                                            slices=slices,
                                            check_empty=check_empty,
                                            allow_dask=allow_dask,
                                            zlib=zlib)
    return output


@default(mod=ncu_defaults)
def replicate_and_copy_variable(dataset, output, var_name,
                                datatype=None, fill_value=None,
                                add_dim=None,
                                chunksize=None, zlib=False,
                                transform=(lambda x, y, z: y),
                                slices=dict(),
                                check_empty=False,
                                allow_dask=False):

    if not isinstance(slices, dict):
        # Assume it is a function that takes the dataset as input and outputs
        # a slicing dict
        comp_slices = slices(dataset)
    else:
        comp_slices = slices

    replicate_netcdf_var(dataset, output, var_name,
                         datatype=datatype, fill_value=fill_value,
                         add_dim=add_dim,
                         slices=comp_slices,
                         chunksize=chunksize, zlib=zlib)

    # Apply a transformation if dimensions are in slices:
    if (set(comp_slices.keys())
       .issubset(dataset.variables[var_name].dimensions)):
        transform(dataset, output, comp_slices)

    if len(dataset.variables[var_name].dimensions) == 0:
        # Scalar variable:
        value = dataset.variables[var_name][...]
        if not np.ma.is_masked(value):
            # If not masked, assign. Otherwise, do nothing
            # try:
            output.variables[var_name][...] = value
            # except AttributeError as e:
            #     # This appears to be a netcdf4 bug.
            #     # Skip this error at moment.
            #     if not (str(e) == "type object 'str' has "
            #                       "no attribute 'kind'" and
            #             value == ''):
            #         raise
        return output

    variable_size = min(_shape(dataset, var_name))
    storage_size = variable_size
    if hasattr(dataset.variables[var_name], '_h5ds'):
        # Use the hdf5 library to find the real size of the stored array:
        variable_size = dataset.variables[var_name]._h5ds.size
        storage_size = dataset.variables[var_name]._h5ds.id.get_storage_size()

    if variable_size > 0 and storage_size > 0:
        if with_dask and allow_dask:
            output = incremental_setitem_with_dask(dataset, output, var_name,
                                                   check_empty, comp_slices)
        else:
            output = incremental_setitem_without_dask(
                                        dataset, output, var_name,
                                        check_empty, comp_slices)
    else:
        _logger.debug('Do not copy data since source variable is empty.')
    return output


def incremental_setitem_with_dask(dataset, output, var_name, check_empty,
                                  comp_slices):
    var_shape = variable_shape(dataset, var_name, comp_slices)
    max_request = DEFAULT_MAX_REQUEST
    max_first_dim_steps = max(int(np.floor(max_request*1024*1024 /
                                  (32*np.prod(var_shape[1:])))), 1)

    getitem_tuple = tuple([comp_slices[var_dim]
                           if var_dim in comp_slices
                           else slice(None) for var_dim in
                           dataset.variables[var_name].dimensions])
    base_chunks = storage_chunks(dataset, var_name)
    source = da.from_array(dataset.variables[var_name],
                           chunks=base_chunks)[getitem_tuple]
    if source.dtype.itemsize > 0:
        out_shape = variable_shape(output, var_name)
        source = source.rechunk((max_first_dim_steps, ) +
                                out_shape[1:])

    dest = WrapperSetItem(output.variables[var_name], check_empty)

    with dask.set_options(get=dask.async.get_sync):
        da.store(source, dest)
    return output


def incremental_setitem_without_dask(dataset, output, var_name, check_empty,
                                     comp_slices):
    var_shape = variable_shape(dataset, var_name, comp_slices)
    max_request = DEFAULT_MAX_REQUEST
    max_first_dim_steps = max(int(np.floor(max_request*1024*1024 /
                                  (32*np.prod(var_shape[1:])))), 1)
    num_frst_dim_chk = int(np.ceil(var_shape[0] /
                           float(max_first_dim_steps)))

    for frst_dim_chk in range(num_frst_dim_chk):
        first_dim_slice = slice(frst_dim_chk*max_first_dim_steps,
                                min((frst_dim_chk + 1)*max_first_dim_steps,
                                    var_shape[0]), 1)
        output = copy_dataset_first_dim_slice(dataset, output, var_name,
                                              first_dim_slice,
                                              check_empty,
                                              slices=comp_slices)
    return output


def copy_dataset_first_dim_slice(dataset, output, var_name, first_dim_slice,
                                 check_empty, slices=dict()):
    comb_slices = slices.copy()
    first_dim = dataset.variables[var_name].dimensions[0]
    if first_dim in comb_slices:
        comb_slices[first_dim] = slice_a_slice(comb_slices[first_dim],
                                               first_dim_slice)
    else:
        comb_slices[first_dim] = first_dim_slice

    getitem_tuple = tuple([comb_slices[var_dim]
                           if var_dim in comb_slices
                           else slice(None, None, 1) for var_dim in
                           dataset.variables[var_name].dimensions])

    try:
        source = increasing_getitem(dataset.variables[var_name], getitem_tuple)
        dest = WrapperSetItem(output.variables[var_name], check_empty)
        dest[first_dim_slice, ...] = source
    except UnicodeDecodeError:
        # In netCDF4-python, an empty string variable raises an
        # error. Here, we thus assume it is empty and we do not
        # assign a value.
        pass
    return output


def increasing_getitem(source, getitem_tuple):
    try:
        dest = source[getitem_tuple]
    except TypeError:
        sorted_getitem = []
        sorter = []
        for item in getitem_tuple:
            if (isinstance(item, list) and
               len(item) > 1 and
               np.min(np.diff(item)) < 0):
                sorted_getitem.append(sorted(item))
                sorter.append(np.argsort(np.argsort(item)))
            else:
                sorted_getitem.append(item)
                sorter.append(None)
        dest = source[tuple(sorted_getitem)]
        for idx, val in enumerate(sorter):
            if val is not None:
                dest = np.ma.take(dest, val, axis=idx)
    return dest


def variable_shape(dataset, var_name, comp_slices=dict()):
    base_var_shape = _shape(dataset, var_name)
    # Create the output variable shape, allowing slices:
    return tuple([base_var_shape[dim_id] if dim not in comp_slices
                  else len(np.arange(base_var_shape[dim_id])
                           [comp_slices[dim]])
                  for dim_id, dim in enumerate(dataset
                                               .variables[var_name]
                                               .dimensions)])


def storage_chunks(dataset, var_name):
    var_shape = variable_shape(dataset, var_name)
    if dataset.variables[var_name].chunking() == 'contiguous':
        base_chunks = (1,) + var_shape[1:]
    else:
        base_chunks = dataset.variables[var_name].chunking()
    return base_chunks


class WrapperSetItem:
    def __init__(self, dest, check_empty=True):
        self._dest = dest
        self._check_empty = check_empty

    def __setitem__(self, key, value):
        # Assign only if not masked everywhere:
        if (not hasattr(value, 'mask') or
            not self._check_empty or
           not value.mask.all()):

            sanitized_value = np.ma.filled(
                                    maybe_conv_bytes_to_str_array(value))
            try:
                self._dest[tuple(key)] = sanitized_value
            except AttributeError as e:  # pragma: no cover. This is rare.
                errors_to_ignore = ["'str' object has no attribute 'size'",
                                    "'unicode' object has no attribute 'size'"]
                if (str(e) in errors_to_ignore and
                   len(key) == 1):
                    for value_idx in np.nditer(sanitized_value):
                        (self._dest[tuple(key)]
                         [value_idx]) = sanitized_value[value_idx]
                else:
                    raise

    def __getattr__(self, key):
        return getattr(self._dest, key)


@default(mod=ncu_defaults)
def replicate_group(dataset, output, group_name):
    output_grp = create_group(dataset, output, group_name)
    replicate_netcdf_file(dataset.groups[group_name], output_grp)
    return output_grp


@default(mod=ncu_defaults)
def create_group(dataset, output, group_name):
    if group_name not in output.groups:
        output_grp = output.createGroup(group_name)
    else:
        output_grp = output.groups[group_name]
    return output_grp


@default(mod=ncu_defaults)
def replicate_netcdf_file(dataset, output):
    replicate_attributes(dataset, output)
    return output


@default(mod=ncu_defaults)
def replicate_netcdf_var_att(dataset, output, var):
    replicate_attributes(dataset.variables[var],
                         output.variables[var])
    return output


def replicate_attributes(dataset, output):
    data_attrs = dataset.ncattrs()
    out_attrs = output.ncattrs()
    for att in [item for item in data_attrs
                if item not in out_attrs]:
        att_val = getncattr(dataset, att)

        if isinstance(att_val, dict):
            atts_pairs = [(att+'.' + key, att_val[key])
                          for key in att_val]
        else:
            atts_pairs = [(att, att_val)]

        for att, att_val in atts_pairs:
            # This fix is for compatitbility with h5netcdf:
            if (hasattr(att_val, 'dtype') and
               att_val.dtype == np.dtype('O')):
                att_val = np.asarray(att_val, dtype='str')
            try:
                setncattr(output, maybe_conv_bytes_to_str(att),
                          maybe_conv_bytes_to_str(att_val))
            except AttributeError:
                if att.startswith('_'):
                    # Private attribute was already set:
                    pass
                else:
                    raise


@default(mod=ncu_defaults)
def replicate_netcdf_var_dimensions(dataset, output, var,
                                    slices=dict(),
                                    datatype=None,
                                    fill_value=None,
                                    add_dim=None,
                                    chunksize=None, zlib=False):
    for dims in dataset.variables[var].dimensions:
        output = replicate_netcdf_dimension(dataset, output, dims,
                                            slices=slices,
                                            datatype=datatype,
                                            fill_value=fill_value,
                                            add_dim=add_dim,
                                            chunksize=chunksize,
                                            zlib=zlib)
    return output


def replicate_netcdf_dimension(dataset, output, dim, slices=dict(),
                               datatype=None, fill_value=None,
                               add_dim=None, chunksize=None, zlib=False):
    if (not _is_dimension_present(output, dim) and
       _is_dimension_present(dataset, dim)):
        if _isunlimited(dataset, dim):
            output.createDimension(dim, None)
        elif dim in slices:
            output.createDimension(dim,
                                   len(np.arange(_dim_len(dataset, dim))
                                       [slices[dim]]))
        else:
            output.createDimension(dim, _dim_len(dataset, dim))
        if dim in dataset.variables:
            replicate_netcdf_var(dataset, output, dim,
                                 zlib=zlib, slices=slices)
            if dim in slices:
                output.variables[dim][:] = increasing_getitem(
                                            dataset.variables[dim],
                                            (slices[dim], ))
            else:
                output.variables[dim][:] = dataset.variables[dim][:]
            if ('bounds' in output.variables[dim].ncattrs() and
                getncattr(output.variables[dim], 'bounds')
               in dataset.variables):
                var_bounds = getncattr(output.variables[dim], 'bounds')
                if var_bounds not in output.variables:
                    output = replicate_netcdf_var(dataset, output,
                                                  var_bounds, zlib=zlib,
                                                  slices=slices)
                    if dim in slices:
                        getitem_tuple = tuple([slices[var_bounds_dim]
                                               if var_bounds_dim
                                               in slices
                                               else slice(None, None, 1)
                                               for var_bounds_dim in
                                               (dataset
                                                .variables[var_bounds]
                                                .dimensions)])
                        output.variables[var_bounds][:] = increasing_getitem(
                                                           dataset
                                                           .variables
                                                           [var_bounds],
                                                           getitem_tuple)
                    else:
                        output.variables[var_bounds][:] = (dataset
                                                           .variables
                                                           [var_bounds][:])
        else:
            # Create a dummy dimension variable:
            dim_var = output.createVariable(dim, np.float, (dim,),
                                            chunksizes=(1,), zlib=zlib)
            if dim in slices:
                dim_var[:] = (np.arange(_dim_len(dataset, dim))
                              [slices[dim]])
            else:
                dim_var[:] = np.arange(_dim_len(dataset, dim))
    return output


@default(mod=ncu_defaults)
def replicate_netcdf_other_var(dataset, output, var, time_dim,
                               zlib=False):
    # Replicates all variables except specified variable:
    variables_list = [other_var
                      for other_var
                      in variables_list_with_time_dim(dataset, time_dim)
                      if other_var != var]
    for other_var in variables_list:
        output = replicate_netcdf_var(dataset, output, other_var,
                                      zlib=zlib)
    return output


@default(mod=ncu_defaults)
def replicate_netcdf_var(dataset, output, var,
                         slices=dict(),
                         datatype=None, fill_value=None,
                         add_dim=None, chunksize=None,
                         zlib=False):
    if var not in dataset.variables:
        return output

    output = replicate_netcdf_var_dimensions(dataset, output,
                                             var, slices=slices,
                                             zlib=zlib)
    if var in output.variables:
        # var is a dimension variable and does not need to be created:
        return output

    if datatype is None:
        datatype = _sanitized_datatype(dataset, var)
    if (isinstance(datatype, netCDF4.CompoundType) and
       datatype.name not in output.cmptypes):
        datatype = output.createCompoundType(datatype.dtype, datatype.name)

    kwargs = dict()
    if (fill_value is None and
        '_FillValue' in dataset.variables[var].ncattrs() and
       datatype == _sanitized_datatype(dataset, var)):
        kwargs['fill_value'] = getncattr(dataset.variables[var], '_FillValue')
    else:
        kwargs['fill_value'] = fill_value

    if var not in output.variables:
        dimensions = dataset.variables[var].dimensions
        time_dim = find_time_dim(dataset)
        var_shape = variable_shape(dataset, var, slices)
        kwargs['chunksizes'] = dataset.variables[var].chunking()
        if (chunksize == -1 or
           kwargs['chunksizes'] == 'contiguous' or
           kwargs['chunksizes'] is None):
            kwargs['chunksizes'] = tuple([1 if dim == time_dim
                                          else var_shape[dim_id]
                                          for dim_id, dim
                                          in enumerate(dimensions)])
        if kwargs['chunksizes'] != 'contiguous':
            kwargs['chunksizes'] = tuple([min(shp, chk) for shp, chk
                                          in zip(var_shape,
                                                 kwargs['chunksizes'])])
        # Chunk must be at least 1:
        kwargs['chunksizes'] = tuple([max(chk, 1) for chk
                                      in kwargs['chunksizes']])
        # Set filters:
        if dataset.variables[var].filters() is not None:
            for item in dataset.variables[var].filters():
                kwargs[item] = dataset.variables[var].filters()[item]
        if zlib and 'zlib' in kwargs and not kwargs['zlib']:
            # Remove filters:
            for key in ['fletcher32', 'complevel', 'shuffle']:
                if key in kwargs:
                    del kwargs[key]
        # Ensure that zlib is set to requested:
        kwargs['zlib'] = zlib
        output.createVariable(var, datatype, dimensions, **kwargs)
    output = replicate_netcdf_var_att(dataset, output, var)
    return output


@default(mod=ncu_defaults)
def find_time_dim_and_replicate_netcdf_file(dataset, output, time_var='time'):
    return (find_time_dim(dataset, time_var=time_var),
            replicate_netcdf_file(dataset, output))
