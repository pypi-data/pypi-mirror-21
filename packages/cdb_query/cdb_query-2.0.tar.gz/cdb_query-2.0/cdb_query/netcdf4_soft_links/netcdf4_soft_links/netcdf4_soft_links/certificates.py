# External:
import sys
import getpass
import select
from six.moves import input

# External by related:
from .netcdf4_pydap import esgf


def prompt_for_username_and_password(options):
    if ((hasattr(options, 'openid') and options.openid is not None) and
       esgf._get_node(options.openid) == 'https://ceda.ac.uk'):
        if (hasattr(options, 'username') and options.username is None):
            options.username = input('Enter CEDA Username: ')

    if not hasattr(options, 'password'):
        options.password = None

    if (hasattr(options, 'openid') and
        options.openid is not None and
       options.password is None):

        if not (hasattr(options, 'password_from_pipe') and
                options.password_from_pipe):
            options.password = (getpass.getpass('Enter Credential phrase: ')
                                .strip())
        else:
            prompt_timeout = 1
            i, o, e = select.select([sys.stdin], [], [], prompt_timeout)
            if i:
                options.password = sys.stdin.readline().strip()
            else:
                raise EnvironmentError('--password_from_pipe selected but '
                                       'no password was piped.')
    return options
