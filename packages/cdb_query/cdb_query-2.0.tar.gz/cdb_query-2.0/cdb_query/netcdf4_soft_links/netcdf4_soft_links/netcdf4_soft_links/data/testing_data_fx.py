"""
Generate test data for netcdf4_soft_links
"""

import numpy as np
from collections import OrderedDict

from netCDF4 import Dataset
from ..ncutils.core import DEFAULT_ENCODING


def create_data():
    struc_dtype = [('temperature', np.dtype('float32')),
                   ('flag', np.dtype('S3')),
                   ('number', np.dtype('int32'))]
    data_dict = {'temperature': np.arange(260, 315) + 0.5,
                 'flag': ['aaa', 'aba', 'abc', 'bb', 'cab', 'bc'],
                 'number': range(10)}
    shape = (2, 2, 2)
    data = np.empty(shape, dtype=struc_dtype)
    for var in data_dict:
        gen = np.random.choice(data_dict[var], size=shape)
        for index in np.ndindex(shape):
            data[var][index] = gen[index]
    return data


def create_test_file(file_name, data, path):
    dim_values = OrderedDict([('plev', [1e5, 1e4]),
                              ('lat', [0.0, 90.0]),
                              ('lon', [0.0, 360.0])])

    # Create tempfile:
    with Dataset(file_name, 'w') as output:
        out_grp = output.createGroup(path)
        for dim_id, dim in enumerate(dim_values):
            out_grp.createDimension(dim, data.shape[dim_id])
            temp = out_grp.createVariable(dim, 'd', (dim,))
            temp[:] = np.linspace(*(dim_values[dim] +
                                    [data.shape[dim_id]]))
            temp.setncattr_string('bounds', dim + '_bnds')
            if 'bnds' not in out_grp.dimensions:
                out_grp.createDimension('bnds', 2)
                bnds = out_grp.createVariable('bnds', 'f',
                                              ('bnds',))
                for val_id, val in enumerate([0, 1]):
                    bnds[val_id] = val
            dim_bnds = out_grp.createVariable(dim + '_bnds', 'd',
                                              (dim, 'bnds'))
            dim_bnds[:] = [temp[:]*0.95, temp[:]*1.05]

        fill_value = 1e20
        for var in data.dtype.names:
            if data[var].dtype.kind in ['U', 'S']:
                datatype = np.str
            else:
                datatype = data[var].dtype
            if datatype == np.str:
                temp = out_grp.createVariable(var, datatype,
                                              tuple(dim_values.keys()))
            else:
                zlib = True
                chunksizes = data[var].shape
                fletcher32 = True
                temp = out_grp.createVariable(var, datatype,
                                              tuple(dim_values.keys()),
                                              zlib=zlib,
                                              chunksizes=chunksizes,
                                              fletcher32=fletcher32)
            try:
                dtype_fill_value = np.array([fill_value]).astype(temp.dtype)
            except (TypeError, AttributeError):
                pass
            if isinstance(dtype_fill_value, np.floating):
                temp.setncattr('_FillValue', dtype_fill_value)

            if datatype == np.str:
                for index in np.ndindex(temp.shape):
                    if hasattr(data[var][index], 'decode'):
                        temp[index] = np.str(data[var][index]
                                             .decode(DEFAULT_ENCODING))
            else:
                temp[:] = data[var]
            if temp.chunking() == 'contiguous':
                temp.setncattr_string('chunksizes', 'contiguous')
            else:
                temp.setncattr('chunksizes', temp.chunking())
            temp.setncattr_string('short_name', var)
            output.sync()
        out_grp.setncattr_string('history', 'test group for netcdf_utils')
        output.setncattr_string('history', 'test file for netcdf_utils')
    return


def generate_test_files(request, tmpdir, number=3):
    data_tmpdir = tmpdir.mkdir('data')
    for idx in range(number):
        file_name = data_tmpdir.join('test_{0}.nc'.format(idx))
        data = create_data()
        create_test_file(str(file_name), data, request.param)
        yield str(file_name), data
