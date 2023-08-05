# External:
import numpy as np
import netCDF4
import os
import tempfile
import multiprocessing
import copy
import logging

# Internal:
from ..remote_netcdf import remote_netcdf, http_netcdf
from ..ncutils import indices, replicate, append, retrieval, dimensions
from ..ncutils import time as nc_time
from ..ncutils.core import maybe_conv_bytes_to_str_array
from ..retrieval_manager import (launch_download, start_download_processes,
                                 stop_download_processes)
from ..queues_manager import NC4SL_queues_manager
from argparse import Namespace

_logger = logging.getLogger(__name__)

MAX_REQUEST_LOCAL = 2048
file_unique_id_list = ['checksum_type', 'checksum', 'tracking_id']


def _nonzeroprod(x):
    return np.prod(np.asarray(x)[np.nonzero(x)])


class read_netCDF_pointers:
    def __init__(self, data_root,
                 download_all_files=False, download_all_opendap=False,
                 min_year=None, year=None, month=None, day=None, hour=None,
                 previous=0, next=0, requested_time_restriction=[],
                 time_var='time', q_manager=None, session=None,
                 num_dl=1, serial=True, remote_netcdf_kwargs={}):
        self.data_root = data_root
        self.q_manager = q_manager
        self.num_dl = num_dl
        self.serial = serial
        self.remote_netcdf_kwargs = remote_netcdf_kwargs
        self.session = session

        self.download_all_files = download_all_files
        self.download_all_opendap = download_all_opendap

        self.time_var = nc_time.find_time_var(self.data_root,
                                              time_var=time_var)
        if (self.time_var is not None and
           len(self.data_root.variables[self.time_var]) > 0):
            # Then find time axis, time restriction and which
            # variables to retrieve:
            self.date_axis = nc_time.get_date_axis(self.data_root,
                                                   self.time_var)
            self.time_axis = self.data_root.variables[self.time_var][:]
            self.time_restriction = get_time_restriction(self.date_axis,
                                                         self.time_axis,
                                                         min_year=min_year,
                                                         years=year,
                                                         months=month,
                                                         days=day,
                                                         hours=hour,
                                                         previous=previous,
                                                         nxt=next)
            if len(requested_time_restriction) == len(self.date_axis):
                self.time_restriction = np.array(requested_time_restriction)
            # time sorting:
            self.time_restriction_sort = np.argsort(self.time_axis
                                                    [self.time_restriction])
        else:
            (self.time_axis,
             self.date_axis,
             self.time_restriction,
             self.time_restriction_sort) = (np.array([]), np.array([]),
                                            np.array([]), np.array([]))

        # Set retrieveable variables:
        if 'soft_links' in self.data_root.groups:
            # Initialize variables:
            self.retrievable_vars = [var for var in self.data_root.variables
                                     if (var in (self
                                                 .data_root
                                                 .groups['soft_links']
                                                 .variables) and
                                         var != self.time_var)]

            # Get list of paths:
            for path_desc in (['path', 'path_id', 'file_type', 'version',
                               'data_node'] + file_unique_id_list):
                try:
                    desc = maybe_conv_bytes_to_str_array(
                                self.data_root.groups['soft_links']
                                .variables[path_desc][:])
                except UnicodeDecodeError:
                    print(path_desc)
                    raise
                setattr(self, path_desc + '_list', desc)
        else:
            self.retrievable_vars = [var for var in self.data_root.variables]

        # sort by size:
        size_retrievable_vars = [_nonzeroprod(self
                                              .data_root
                                              .variables[var]
                                              .shape) for var
                                 in self.retrievable_vars]
        size_retrievable_vars_sort = np.argsort(size_retrievable_vars)[::-1]
        self.retrievable_vars = list(np.array(self.retrievable_vars)
                                     [size_retrievable_vars_sort])
        return

    def replicate(self, output, check_empty=True, chunksize=None,
                  zlib=False):
        # replicate attributes
        replicate.replicate_netcdf_file(self.data_root, output)
        # replicate and copy variables:
        for var_name in self.data_root.variables:
            (replicate
             .replicate_and_copy_variable(self.data_root, output, var_name,
                                          check_empty=check_empty, zlib=zlib,
                                          chunksize=chunksize))
        if 'soft_links' in self.data_root.groups:
            output_grp = replicate.replicate_group(self.data_root,
                                                   output, 'soft_links')
            replicate.replicate_netcdf_file(self
                                            .data_root
                                            .groups['soft_links'],
                                            output_grp)
            for var_name in self.data_root.groups['soft_links'].variables:
                (replicate
                 .replicate_and_copy_variable(self
                                              .data_root
                                              .groups['soft_links'],
                                              output_grp,
                                              var_name,
                                              check_empty=check_empty,
                                              zlib=zlib, chunksize=chunksize))
        return

    def append(self, output, check_empty=True, zlib=False):
        # replicate attributes
        replicate.replicate_netcdf_file(self.data_root, output)

        record_dimensions = append.append_record(self.data_root, output)
        # replicate and copy variables:
        for var_name in self.data_root.variables:
            if var_name not in record_dimensions:
                if (var_name in output.variables and
                    (dimensions
                     .check_dimensions_compatibility(
                            self.data_root,
                            output,
                            var_name,
                            exclude_unlimited=True)) and
                   len(record_dimensions) > 0):
                    # Variable can be appended along some record dimensions:
                    _logger.debug('Appending variable ' + var_name)
                    (append
                     .append_and_copy_variable(self.data_root,
                                               output,
                                               var_name,
                                               record_dimensions,
                                               check_empty=check_empty))
                elif (var_name not in output.variables and
                      (dimensions
                       .check_dimensions_compatibility(self.data_root,
                                                       output, var_name))):
                    # Variable can be copied:
                    _logger.debug('Copying variable ' + var_name)
                    (replicate
                     .replicate_and_copy_variable(self.data_root,
                                                  output,
                                                  var_name,
                                                  check_empty=check_empty,
                                                  zlib=zlib))

        if 'soft_links' in self.data_root.groups:
            _logger.debug('Transferring soft links')
            data_grp = self.data_root.groups['soft_links']
            output_grp = replicate.replicate_group(self.data_root,
                                                   output,
                                                   'soft_links')
            (replicate
             .replicate_netcdf_file(self.data_root.groups['soft_links'],
                                    output_grp))

            record_dimensions.update(append.append_record(data_grp,
                                                          output_grp))
            for var_name in data_grp.variables:
                if var_name not in record_dimensions:
                    if (var_name in output_grp.variables and
                        (dimensions
                         .check_dimensions_compatibility(
                                data_grp,
                                output_grp,
                                var_name,
                                exclude_unlimited=True))):
                        # Variable can be appended along the time and
                        # path dimensions:
                        (append
                         .append_and_copy_variable(data_grp,
                                                   output_grp,
                                                   var_name,
                                                   record_dimensions,
                                                   check_empty=check_empty))
                    elif (var_name not in output_grp.variables and
                          (dimensions
                           .check_dimensions_compatibility(data_grp,
                                                           output_grp,
                                                           var_name))):
                        # Variable can be copied:
                        (replicate
                         .replicate_and_copy_variable(data_grp,
                                                      output_grp,
                                                      var_name,
                                                      check_empty=check_empty,
                                                      zlib=zlib))
        return

    def retrieve(self, output, retrieval_type='assign', filepath=None,
                 out_dir='.', silent=True, zlib=False):
        options, data_node_list, processes = self._downloads(silent=silent)
        self.q_manager.set_opened()
        self._retrieve(output, retrieval_type=retrieval_type,
                       filepath=filepath, out_dir=out_dir,
                       zlib=zlib)
        self.q_manager.set_closed()
        launch_download(output, data_node_list, self.q_manager, options)
        stop_download_processes(processes)
        return

    def _retrieve(self, output, retrieval_type='assign', filepath=None,
                  out_dir='.', slices=dict(), zlib=False):
        # Define tree:
        self.tree = output.path.split('/')[1:]
        self.filepath = filepath
        self.out_dir = out_dir
        self.retrieval_type = retrieval_type

        if self.time_var is not None:
            time_slice = get_dim_slice(slices, self.time_var)
            # Record to output if output is a netCDF4 Dataset:
            slices_copy = copy.copy(slices)
            if self.time_var not in output.dimensions:
                # pick only requested times and sort them
                (nc_time
                 .create_time_axis(self.data_root,
                                   output,
                                   self.time_axis
                                   [self.time_restriction]
                                   [self.time_restriction_sort]
                                   [time_slice],
                                   time_var=self.time_var,
                                   zlib=zlib))
                # Make sure to slice other variables with a time var:
                slices_copy[self.time_var] = list(
                                              np.arange(len(self.time_axis))
                                              [self.time_restriction]
                                              [self.time_restriction_sort]
                                              [time_slice])

            # Replicate all the other variables:
            for var in (set(self.data_root.variables)
                        .difference(self.retrievable_vars)):
                if var not in output.variables:
                    output = (replicate
                              .replicate_and_copy_variable(self.data_root,
                                                           output, var,
                                                           slices=slices_copy,
                                                           zlib=zlib))

            if self.retrieval_type in ['download_files', 'download_opendap',
                                       'assign']:
                # Replicate soft links for remote_queryable data:
                output_grp = (replicate
                              .replicate_group(self.data_root, output,
                                               'soft_links'))
                for var_name in self.data_root.groups['soft_links'].variables:
                    replicate.replicate_netcdf_var(self.data_root
                                                   .groups['soft_links'],
                                                   output_grp, var_name,
                                                   zlib=zlib)
                    if (var_name != self.time_var and
                       sum(self.time_restriction) > 0):
                        if self.time_var in (self.data_root
                                             .groups['soft_links']
                                             .variables[var_name].dimensions):
                            if (self.data_root.groups['soft_links']
                               .variables[var_name].shape[0]) == 1:
                                # Prevents a bug in h5py when self.data_root is
                                # an h5netcdf file:
                                if np.all(self.time_restriction):
                                    out = maybe_conv_bytes_to_str_array(
                                           self.data_root.groups['soft_links']
                                           .variables[var_name][...])
                            else:
                                out = maybe_conv_bytes_to_str_array(
                                        self.data_root.groups['soft_links']
                                        .variables[var_name]
                                        [self.time_restriction, ...]
                                        [self.time_restriction_sort, ...]
                                        [time_slice, ...])
                            output_grp.variables[var_name][:] = out

            self.paths_sent_for_retrieval = []
            for var_to_retrieve in self.retrievable_vars:
                self._retrieve_variable(output, var_to_retrieve, zlib=zlib)

            # Only record variables at the end:
            if 'soft_links' in output.groups:
                for path_desc in (['path', 'path_id', 'file_type', 'version'] +
                                  file_unique_id_list):
                    out = maybe_conv_bytes_to_str_array(
                            getattr(self, path_desc + '_list'))
                    for idx in np.ndindex(out.shape):
                        output_grp.variables[path_desc][idx] = str(out[idx])
        else:
            # Fixed variable. Do not retrieve, just copy:
            for var in self.retrievable_vars:
                output = (replicate
                          .replicate_and_copy_variable(self.data_root,
                                                       output, var,
                                                       zlib=zlib))
        return

    def _retrieve_variable(self, output, var_to_retrieve, slices=dict(),
                           zlib=False):
        # Replicate variable to output:
        output = (replicate
                  .replicate_netcdf_var(self.data_root,
                                        output, var_to_retrieve,
                                        chunksize=-1, zlib=zlib,
                                        slices=slices))

        if sum(self.time_restriction) == 0:
            return

        # Get the requested dimensions:
        (self.dimensions,
         self.unsort_dimensions) = get_dimensions_slicing(output,
                                                          var_to_retrieve,
                                                          self.time_var)

        # Determine the paths_ids for soft links:
        time_slice = get_dim_slice(slices, self.time_var)

        if (self.data_root.groups['soft_links']
           .variables[var_to_retrieve].shape[0]) == 1:
            # Prevents a bug in h5py when self.data_root is an h5netcdf file:
            if np.all(self.time_restriction):
                self.paths_link = (self.data_root.groups['soft_links']
                                   .variables[var_to_retrieve][:, 0])
                self.indices_link = (self.data_root.groups['soft_links']
                                     .variables[var_to_retrieve][:, 1])
        else:
            self.paths_link = (self.data_root.groups['soft_links']
                               .variables[var_to_retrieve]
                               [self.time_restriction, 0]
                               [self.time_restriction_sort]
                               [time_slice])
            self.indices_link = (self.data_root.groups['soft_links']
                                 .variables[var_to_retrieve]
                                 [self.time_restriction, 1]
                                 [self.time_restriction_sort]
                                 [time_slice])

        # Convert paths_link to id in path dimension:
        # Use search sorted:
        self.paths_link = (np.argsort(self.path_id_list)
                           [np.searchsorted(self.path_id_list, self.paths_link,
                                            sorter=np.argsort(self
                                                              .path_id_list))])

        # Sort the paths so that we query each only once:
        (unique_path_list_id,
         self.sorting_paths) = np.unique(self.paths_link, return_inverse=True)

        for unique_path_id, path_id in enumerate(unique_path_list_id):
            self._retrieve_path_to_variable(unique_path_id, path_id, output,
                                            var_to_retrieve)
        return

    def _retrieve_path_to_variable(self, unique_path_id, path_id, output,
                                   var_to_retrieve):
        original_path_to_retrieve = self.path_list[path_id]

        # Next, we check if the file is available. If it is not we replace it
        # with another file with the same checksum, if there is one!
        file_type = self.file_type_list[list(self.path_list)
                                        .index(original_path_to_retrieve)]
        if hasattr(self.q_manager, 'semaphores'):
            semaphores = self.q_manager.semaphores
        else:
            semaphores = dict()
        remote_data = remote_netcdf.remote_netCDF(original_path_to_retrieve,
                                                  file_type,
                                                  semaphores=semaphores,
                                                  session=self.session,
                                                  **self.remote_netcdf_kwargs)

        # See if the available path is available for download
        # and find alternative:
        if self.retrieval_type == 'download_files':
            file_types = remote_netcdf.downloadable_file_types
        elif self.retrieval_type == 'download_opendap':
            file_types = remote_netcdf.remote_queryable_file_types
        elif self.retrieval_type == 'load':
            file_types = remote_netcdf.local_queryable_file_types
        elif self.retrieval_type == 'assign':
            file_types = (remote_netcdf.remote_queryable_file_types +
                          remote_netcdf.local_queryable_file_types)

        path_to_retrieve = (remote_data
                            .check_if_available_and_find_alternative(
                                    self.path_list, self.file_type_list,
                                    self.checksum_list,
                                    file_types,
                                    num_trials=2))

        # See if there is a better file_type available:
        file_types_alt = remote_netcdf.local_queryable_file_types
        if (self.retrieval_type == 'download_files' and
           not self.download_all_files):
            file_types_alt += remote_netcdf.remote_queryable_file_types

        alt_path_to_retrieve = (remote_data
                                .check_if_available_and_find_alternative(
                                        self.path_list,
                                        self.file_type_list,
                                        self.checksum_list,
                                        file_types_alt,
                                        num_trials=2))

        # Create a sort table:
        sort_table = (np.arange(len(self.sorting_paths))
                      [self.sorting_paths == unique_path_id])

        if alt_path_to_retrieve is not None:
            # Do not retrieve if a 'better' file type exists and is available
            if ((self.retrieval_type == 'download_files' and
                 not self.download_all_files) or
                (self.retrieval_type == 'download_opendap' and
                 not self.download_all_opendap)):
                assign_leaf_missing(output, sort_table,
                                    self.tree + [var_to_retrieve])
                return
            # Only in the download_files case, do not change path:
            if not (self.retrieval_type == 'download_files' and
                    self.download_all_files):
                path_to_retrieve = alt_path_to_retrieve

        # If path_to_retrieve is None, fill with missing values.
        # This prevents a rare bug in netcdf4-python:
        if path_to_retrieve is None:
            assign_leaf_missing(output, sort_table,
                                self.tree + [var_to_retrieve])
            return

        # Get the file_type, checksum and version of the file to retrieve:
        path_index = list(self.path_list).index(path_to_retrieve)
        file_type = self.file_type_list[path_index]
        version = 'v' + str(self.version_list[path_index])
        checksum = self.checksum_list[path_index]
        checksum_type = self.checksum_type_list[path_index]

        # Reverse pick time indices correponsing to the unique path_id:
        if file_type == 'slcontainer':
            # If the data is in the current file, the data lies in the
            # corresponding time step:
            time_indices = (np.arange(len(self.sorting_paths), dtype=int)
                            [self.sorting_paths == unique_path_id])
        else:
            time_indices = (self.indices_link
                            [self.sorting_paths == unique_path_id])

        download_args = (0, path_to_retrieve, file_type,
                         var_to_retrieve, self.tree)

        _logger.info('Retrieving {0} from {1}'.format(var_to_retrieve,
                                                      path_to_retrieve))
        if self.retrieval_type != 'download_files':
            # This is an important test that should be included in future
            # releases:
            # with (netCDF4
            #       .Dataset(path_to_retrieve.split('|')[0])) as data_test:
            #     data_date_axis = (nc_time
            #                       .get_date_axis(data_test,'time')[time_indices])
            (self.dimensions[self.time_var],
             self.unsort_dimensions[self.time_var]) = (indices
                                                       .prepare_indices(
                                                            time_indices))

            download_kwargs = {'dimensions': self.dimensions,
                               'unsort_dimensions': self.unsort_dimensions,
                               'sort_table': sort_table}

            # Keep a list of paths sent for retrieval:
            self.paths_sent_for_retrieval.append(path_to_retrieve)
            if file_type == 'slcontainer':
                # The data is already in the file, we must copy it!
                retrieved_data = (retrieval
                                  .retrieve_container(self.data_root,
                                                      var_to_retrieve,
                                                      self.dimensions,
                                                      self.unsort_dimensions,
                                                      sort_table,
                                                      MAX_REQUEST_LOCAL))
                result = (retrieved_data, sort_table,
                          self.tree + [var_to_retrieve])
                assign_leaf(output, *result)
            else:
                if 'soft_links' in output.groups:
                    new_path = ('slcontainer/' +
                                os.path.basename(self.path_list[path_index]))
                    new_file_type = 'slcontainer'
                    self._add_path_to_soft_links(new_path, new_file_type,
                                                 path_index,
                                                 self.sorting_paths ==
                                                 unique_path_id,
                                                 output.groups['soft_links'],
                                                 var_to_retrieve)

                if (file_type in remote_netcdf.local_queryable_file_types and
                   'download' not in self.retrieval_type):
                    # Load and simply assign:
                    remote_data = remote_netcdf.remote_netCDF(path_to_retrieve,
                                                              file_type)
                    result = remote_data.download(
                                    *download_args[3:],
                                    download_kwargs=download_kwargs)
                    assign_leaf(output, *result)
                else:
                    data_node = remote_netcdf.get_data_node(path_to_retrieve,
                                                            file_type)
                    # Send to the download queue:
                    self.q_manager.put_to_data_node(data_node,
                                                    download_args +
                                                    (download_kwargs,))
        else:
            if path_to_retrieve not in self.paths_sent_for_retrieval:
                new_path = (http_netcdf
                            .destination_download_files(self.path_list
                                                        [path_index],
                                                        self.out_dir,
                                                        var_to_retrieve,
                                                        version,
                                                        self.tree))
                new_file_type = 'local_file'
                self._add_path_to_soft_links(new_path, new_file_type,
                                             path_index,
                                             self.sorting_paths ==
                                             unique_path_id,
                                             output.groups['soft_links'],
                                             var_to_retrieve)
                download_kwargs = {'out_dir': self.out_dir,
                                   'version': version,
                                   'checksum': checksum,
                                   'checksum_type': checksum_type}
                # Keep a list of paths sent for retrieval:
                self.paths_sent_for_retrieval.append(path_to_retrieve)

                data_node = remote_netcdf.get_data_node(path_to_retrieve,
                                                        file_type)
                # Send to the download queue:
                self.q_manager.put_to_data_node(data_node,
                                                download_args +
                                                (download_kwargs,))
        return

    def _add_path_to_soft_links(self, new_path, new_file_type, path_index,
                                time_indices_to_replace, output,
                                var_to_retrieve):
        path_id = hash(new_path)
        if new_path not in self.path_list:
            self.path_list = np.append(self.path_list, new_path)
            self.file_type_list = np.append(self.file_type_list, new_file_type)
            data_node = remote_netcdf.get_data_node(
                                new_path, new_file_type)
            self.data_node_list = np.append(self.data_node_list, data_node)
            self.path_id_list = np.append(self.path_id_list, path_id)
            for path_desc in ['version'] + file_unique_id_list:
                desc = getattr(self, path_desc + '_list')[path_index]
                out = np.append(getattr(self, path_desc + '_list'), desc)
                setattr(self, path_desc + '_list', out)

        (output.variables[var_to_retrieve]
         [time_indices_to_replace, 0]) = path_id
        return output

    def open(self):
        self.tree = []
        filehandle, self.filepath = tempfile.mkstemp()
        # must close file number:
        os.close(filehandle)
        self.output_root = netCDF4.Dataset(self.filepath, 'w',
                                           format='NETCDF4',
                                           diskless=True, persist=False)
        self._is_open = True
        return

    def __enter__(self):
        self.open()
        return self

    def _downloads(self, silent=True):
        options = Namespace(silent=silent, serial=self.serial,
                            num_dl=self.num_dl)
        data_node_list = list(np.unique(self.data_root
                                        .groups['soft_links']
                                        .variables['data_node'][:]))
        if self.q_manager is None:
            processes_names = [multiprocessing.current_process().name]
            self.q_manager = NC4SL_queues_manager(options, processes_names)
            for data_node in data_node_list:
                self.q_manager.queues.add_new_data_node(data_node)

        processes = start_download_processes(options, self.q_manager)
        return options, data_node_list, processes

    def assign(self, var_to_retrieve, slices=dict(), silent=True,
               zlib=False):
        if not self._is_open:
            raise IOError('read_soft_links must be opened to assign')

        options, data_node_list, processes = self._downloads(silent=silent)
        self.variables = dict()
        # Create type download_opendap_and_load!
        self.retrieval_type = 'assign'
        self.out_dir = '.'
        self.paths_sent_for_retrieval = []

        time_slice = get_dim_slice(slices, self.time_var)

        self.output_root.createGroup(var_to_retrieve)
        nc_time.create_time_axis(self.data_root,
                                 self.output_root.groups[var_to_retrieve],
                                 self.time_axis[self.time_restriction]
                                 [self.time_restriction_sort]
                                 [time_slice],
                                 zlib=zlib)
        self.q_manager.set_opened()
        self._retrieve_variable(self.output_root.groups[var_to_retrieve],
                                var_to_retrieve, slices=slices,
                                zlib=zlib)
        self.q_manager.set_closed()
        launch_download(self.output_root.groups[var_to_retrieve],
                        data_node_list, self.q_manager, options)
        stop_download_processes(processes)

        for var in self.output_root.groups[var_to_retrieve].variables:
            self.variables[var] = (self.output_root.groups[var_to_retrieve]
                                   .variables[var])
        return

    def close(self):
        self.output_root.close()
        try:
            os.remove(self.filepath)
        except OSError:
            pass
        self._is_open = False
        return

    def __exit__(self, *_):
        self.close()
        return


def add_previous(time_restriction):
    return np.logical_or(time_restriction, np.append(time_restriction[1:],
                         False))


def add_next(time_restriction):
    return np.logical_or(time_restriction, np.insert(time_restriction[:-1], 0,
                         False))


def time_restriction_years(min_year, years, date_axis, time_restriction_any):
    if years is not None:
        years_axis = np.array([date.year for date in date_axis])
        if min_year is not None:
            # Important for piControl:
            time_restriction = np.logical_and(time_restriction_any,
                                              [True if year in years
                                               else False
                                               for year in
                                               (years_axis - years_axis.min() +
                                                min_year)])
        else:
            time_restriction = np.logical_and(time_restriction_any,
                                              [True if year in years
                                               else False
                                               for year in years_axis])
        return time_restriction
    else:
        return time_restriction_any


def time_restriction_months(months, date_axis, time_restriction_for_years):
    if months is not None:
        months_axis = np.array([date.month for date in date_axis])
        # time_restriction=np.logical_and(time_restriction,months_axis==month)
        time_restriction = np.logical_and(time_restriction_for_years,
                                          [True if month in months
                                           else False
                                           for month in months_axis])
        return time_restriction
    else:
        return time_restriction_for_years


def time_restriction_days(days, date_axis, time_restriction_any):
    if days is not None:
        days_axis = np.array([date.day for date in date_axis])
        time_restriction = np.logical_and(time_restriction_any,
                                          [True if day in days
                                           else False
                                           for day in days_axis])
        return time_restriction
    else:
        return time_restriction_any


def time_restriction_hours(hours, date_axis, time_restriction_any):
    if hours is not None:
        hours_axis = np.array([date.hour for date in date_axis])
        time_restriction = np.logical_and(time_restriction_any,
                                          [True if hour in hours
                                           else False
                                           for hour in hours_axis])
        return time_restriction
    else:
        return time_restriction_any


def get_time_restriction(date_axis, time_axis,
                         min_year=None, years=None, months=None,
                         days=None, hours=None,
                         previous=0, nxt=0):
    time_restriction = np.ones(date_axis.shape, dtype=np.bool)

    time_restriction = time_restriction_years(min_year, years, date_axis,
                                              time_restriction)
    time_restriction = time_restriction_months(months, date_axis,
                                               time_restriction)
    time_restriction = time_restriction_days(days, date_axis,
                                             time_restriction)
    time_restriction = time_restriction_hours(hours, date_axis,
                                              time_restriction)

    if (previous > 0 or
       nxt > 0):
        sort_indices = np.argsort(time_axis)

        sorted_time_restriction = time_restriction[sort_indices]
        if previous > 0:
            for prev_num in range(previous):
                sorted_time_restriction = add_previous(sorted_time_restriction)
        if nxt > 0:
            for nxt_num in range(nxt):
                sorted_time_restriction = add_next(sorted_time_restriction)
        time_restriction[sort_indices] = sorted_time_restriction
    return time_restriction


def get_dimensions_slicing(dataset, var, time_var):
    # Set the dimensions:
    dimensions = dict()
    unsort_dimensions = dict()
    for dim in dataset.variables[var].dimensions:
        if dim != time_var:
            if dim in dataset.variables:
                dimensions[dim] = dataset.variables[dim][:]
            else:
                dimensions[dim] = np.arange(len(dataset.dimensions[dim]))
            unsort_dimensions[dim] = None
    return dimensions, unsort_dimensions


def get_dim_slice(slices, dim):
    dim_slice = slice(None)
    if dim in slices:
        dim_slice = slices[dim]
    return dim_slice


def assign_leaf(output, val, sort_table, tree):
    variable = output.variables[tree[-1]]
    val = np.ma.masked_invalid(val)
    if len(variable.shape) > 1:
        for idx, sort_idx in enumerate(sort_table):
            variable[sort_idx, ...] = val[idx, ...]
    elif len(variable.shape) == 1:
        for idx, sort_idx in enumerate(sort_table):
            variable[sort_idx] = val[idx:idx+1]
    else:
        variable[:] = val
    return


def assign_leaf_missing(output, sort_table, tree):
    variable = output.variables[tree[-1]]
    if len(variable.shape) > 1:
        for idx, sort_idx in enumerate(sort_table):
            variable[sort_idx, ...] = np.ma.masked_all(variable.shape[1:])
    elif len(variable.shape) == 1:
        for idx, sort_idx in enumerate(sort_table):
            variable[sort_idx] = np.ma.masked_all((1,))
    else:
        variable[:] = np.ma.masked_all((1,))
    return
