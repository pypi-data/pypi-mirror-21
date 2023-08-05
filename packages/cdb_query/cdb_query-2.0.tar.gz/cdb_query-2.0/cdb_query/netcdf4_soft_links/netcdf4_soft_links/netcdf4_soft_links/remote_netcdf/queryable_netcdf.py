# External:
from netCDF4 import Dataset as nc4_Dataset
from h5netcdf.legacyapi import Dataset as h5_Dataset
from ..netcdf4_pydap import Dataset as pydap_Dataset
from ..netcdf4_pydap import ServerError
import errno
from socket import error as SocketError
from socket import timeout as socket_ReadTimeout


import time
import requests
from six.moves.urllib.error import HTTPError, URLError
import copy

# Internal:
from . import safe_handling
from ..ncutils.core import check_if_opens
from ..ncutils.retrieval import retrieve_container


class queryable_netCDF:
    def __init__(self, file_name,
                 semaphores=dict(),
                 time_var='time',
                 remote_data_node='',
                 timeout=120,
                 session=None,
                 username=None,
                 openid=None,
                 password=None,
                 authentication_uri=None,
                 use_certificates=False):
        self.file_name = file_name
        self.semaphores = semaphores
        self.time_var = time_var

        if remote_data_node in self.semaphores.keys():
            self.semaphore = semaphores[remote_data_node]
            self.handle_safely = True
        else:
            self.semaphore = safe_handling.dummy_semaphore()
            self.handle_safely = False

        self.timeout = timeout
        self.session = session
        self.authentication_uri = authentication_uri
        self.username = username
        self.openid = openid
        self.password = password
        self.use_certificates = use_certificates

        if (len(self.file_name) > 4 and
           self.file_name[:4] == 'http'):
            self.use_pydap = True
            self.max_request = 450
        else:
            self.use_pydap = False
            self.max_request = 2048
            try:
                with h5_Dataset(self.file_name, 'r'):
                    pass
                self.use_h5 = True
            except Exception:
                self.use_h5 = False
        return

    def __enter__(self):
        self.semaphore.acquire()
        return self

    def __exit__(self, *_):
        if self.handle_safely:
            # Do not release semaphore right away if data is not local:
            time.sleep(0.01)
        self.semaphore.release()
        return

    def unsafe_handling(self, function_handle, *args, **kwargs):
        if self.use_pydap:
            # We use verify=False by default. This does not
            # mean that all requests are unverified. It means
            # that requests that have to be unverified
            # will be allowed to be unverified.
            with (pydap_Dataset(
                           self.file_name,
                           timeout=self.timeout,
                           session=self.session,
                           verify=False,
                           authentication_uri=self.authentication_uri,
                           username=self.username,
                           openid=self.openid,
                           password=self.password)) as dataset:
                output = function_handle(dataset, *args, **kwargs)
        elif self.use_h5:
            with h5_Dataset(self.file_name, 'r') as dataset:
                output = function_handle(dataset, *args, **kwargs)
        else:
            with nc4_Dataset(self.file_name, 'r') as dataset:
                output = function_handle(dataset, *args, **kwargs)
        return output

    def safe_handling(self, function_handle, *args, **kwargs):
        error_statement = (('The url {0} could not be opened. '
                            'Copy and paste this url in a browser '
                            'and try downloading the file. '
                            'If it works, you can stop the download '
                            'and retry using cdb_query. If '
                            'it still does not work it is likely that '
                            'your certificates are either'
                            'not available or out of date.')
                           .format(self.file_name.replace('dodsC',
                                                          'fileServer')))
        if 'num_trials' in kwargs:
            num_trials = kwargs['num_trials']
            del kwargs['num_trials']
        else:
            num_trials = 5
        success = False
        timeout = copy.copy(self.timeout)
        for trial in range(num_trials):
            if not success:
                try:
                    # Capture errors. Important to prevent curl
                    # errors from being printed:
                    output = self.unsafe_handling(function_handle, *args,
                                                  **kwargs)
                    success = True
                except (HTTPError, URLError,
                        requests.exceptions.ReadTimeout,
                        socket_ReadTimeout,
                        ServerError) as e:
                    # Basic errors, may be worth retrying:
                    time.sleep(3*(trial + 1))
                    # Increase timeout:
                    timeout += self.timeout
                    pass
                except (RuntimeError,
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ChunkedEncodingError) as e:
                    time.sleep(3*(trial + 1))
                    pass
                except SocketError as e:
                    if e.errno != errno.ECONNRESET:
                        raise
                    time.sleep(3*(trial+1))
                    pass
                except Exception as e:
                    if (str(e).endswith('If you are unable to login, you '
                                        'must either wait or use '
                                        'authentication from '
                                        'another service.')):
                        # Auth error, may be worth retrying:
                        time.sleep(3*(trial + 1))
                        # Increase timeout:
                        timeout += self.timeout
                        pass
                    elif str(e).startswith('Unable to parse token:'):
                        # This error comes up when the resource has
                        # moved and is no longer an OPENDAP link.
                        # Simply break, thus raising a dodsError.
                        break
                    else:
                        raise
        if not success:
            raise dodsError(error_statement)
        return output

    def check_if_opens(self, num_trials=5):
        try:
            return self.safe_handling(check_if_opens,
                                      num_trials=num_trials)
        except (dodsError, OSError):
            return False

    def download(self, var, pointer_var, dimensions=dict(),
                 unsort_dimensions=dict(), sort_table=[],
                 time_var='time'):
        retrieved_data = (self
                          .safe_handling(retrieve_container,
                                         var,
                                         dimensions,
                                         unsort_dimensions,
                                         sort_table, self.max_request,
                                         time_var=self.time_var,
                                         file_name=self.file_name))
        return (retrieved_data, sort_table, pointer_var + [var])


class dodsError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
