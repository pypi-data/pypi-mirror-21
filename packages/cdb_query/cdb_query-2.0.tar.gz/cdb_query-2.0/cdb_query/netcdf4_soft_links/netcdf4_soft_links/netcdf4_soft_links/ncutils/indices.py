# External:
import numpy as np
from itertools import groupby

from .core import default
from .defaults import indices as ncu_defaults


def get_indices_from_dim(source, output, dim=None):
    # This function finds which indices from source should be used
    # and in which order:
    # Special case where both dimensions are lenght one.
    # Then it is unambiguous:
    if len(source) == 1 and len(output) == 1:
        return np.array([0])

    def _isclose(x, y):
        check = np.isclose(x, y, atol=1e-5)
        if (dim is not None and
           dim.lower() in ['lon', 'longitude']):
            # Longitude dimension, compare modulo 360.0
            x_mod = np.mod(x, 360.0)
            y_mod = np.mod(y, 360.0)
            check = np.logical_or(
                        check,
                        np.logical_or(np.isclose(x_mod, y_mod, atol=1e-5),
                                      np.logical_or(
                                          np.isclose(x_mod, y_mod - 360.0,
                                                     atol=1e-5),
                                          np.isclose(x_mod - 360.0, y_mod,
                                                     atol=1e-5))))
        return check

    indices = np.arange(max(source.shape))[np.in1d(source, output)]
    try:
        return np.array([indices[source[indices] == val][0]
                         for val in output])
    except IndexError:
        # The in1d might have encountered a floating point error. Make the
        # equality fuzzy:
        indices = (np.arange(max(source.shape))[np.array(
                                                    [np.any(
                                                       _isclose(output, item))
                                                     for item in source])])
        return np.array([indices[_isclose(source[indices], val)][0]
                         for val in output])


def convert_indices_to_slices(indices):
    # This feature is currently broken (December 2014):
    if len(indices) > 1:
        steps = np.maximum(np.unique(np.diff(indices)), 1)
        optimal_step = steps[np.argmin(
                               [len(convert_indices_to_slices_step(indices, x))
                                for x in steps])]
        return convert_indices_to_slices_step(indices, optimal_step)
    else:
        return convert_indices_to_slices_step(indices, 1)


def convert_indices_to_slices_step(indices, step):
    slices = []
    for key, it in groupby(enumerate(indices), lambda x: x[1] - step*x[0]):
        indices_slice = [y for x, y in it]
        slices.append(slice(indices_slice[0], indices_slice[-1]+1, step))
    return slices


def slice_a_slice(initial_slice, slice_to_use):
    """
    This function is not commutative
    """
    if (isinstance(slice_to_use, slice) and
       isinstance(initial_slice, slice)):
        return convert_indices_to_slices_step(range(initial_slice.start,
                                                    initial_slice.stop,
                                                    initial_slice.step)
                                              [slice_to_use],
                                              initial_slice.step *
                                              slice_to_use.step)[0]
    elif isinstance(initial_slice, slice):
        return (np.arange(initial_slice.start, initial_slice.stop,
                          initial_slice.step)[slice_to_use]
                .astype(int).tolist())
    else:
        return np.array(initial_slice)[slice_to_use].tolist()


def prepare_indices(indices):
    sort_indices = np.argsort(indices)
    # Sort:
    indices = indices[sort_indices]
    # provide the inverse:
    unsort_indices = np.argsort(sort_indices)

    # Finally, convert the indices to slices:
    indices = convert_indices_to_slices(indices)
    return indices, unsort_indices


def largest_hyperslab(slices_dict):
    return np.prod([max([slice_length(item) for item in slices_dict[dim]])
                    for dim in slices_dict])


def slice_length(slice_item):
    return len(range(slice_item.start, slice_item.stop, slice_item.step))


@default(mod=ncu_defaults)
def retrieve_slice(variable, indices, unsort_indices, dim, dimensions,
                   dim_id, max_request, getitem_tuple=tuple()):
    if len(dimensions) > 0:
        return take_safely(np.ma.concatenate([retrieve_slice(variable,
                                              indices,
                                              unsort_indices,
                                              dimensions[0],
                                              dimensions[1:],
                                              dim_id + 1,
                                              max_request,
                                              getitem_tuple=getitem_tuple+(x,))
                                              for x in indices[dim]],
                                             axis=dim_id),
                           unsort_indices[dim], axis=dim_id)
    else:
        return take_safely(np.ma.concatenate([getitem_from_variable(
                                                    variable,
                                                    getitem_tuple + (x,),
                                                    max_request)
                                              for x in indices[dim]],
                                             axis=dim_id),
                           unsort_indices[dim], axis=dim_id)


def take_safely(x, indices, axis=0):
    if x.shape[axis] == 0:
        axes = len(x.shape) * [None]
        for id in range(len(axes)):
            axes[id] = x.shape[id]
        axes[axis] = len(indices)
        return np.ma.masked_all(axes)
    else:
        return np.ma.take(x, indices, axis=axis)


def getitem_from_variable(variable, getitem_tuple, max_request):
    if (max_request is None or
        max_request*1024*1024 >
       32*np.prod([slice_length(item) for item in getitem_tuple])):
        return variable[getitem_tuple]
    else:
        # Max number of steps along first dimension:
        max_steps = np.maximum(
                        int(np.floor(
                               max_request*1024*1024 /
                               (32*np.prod([slice_length(item)
                                            for item in getitem_tuple[1:]])))),
                        1)

        first_dim_length = ((getitem_tuple[0].stop - getitem_tuple[0].start) //
                            getitem_tuple[0].step)
        num_split = np.minimum(first_dim_length // max_steps, first_dim_length)

        id_lists = np.array_split(np.arange(getitem_tuple[0].start,
                                            getitem_tuple[0].stop,
                                            getitem_tuple[0].step), num_split)

        slice_list = [convert_indices_to_slices_step(x,
                                                     getitem_tuple[0].step)[0]
                      for x in id_lists]
        return np.ma.concatenate([variable[(x,) + getitem_tuple[1:]]
                                  for x in slice_list],
                                 axis=0)
