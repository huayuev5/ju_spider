import os
import dummy
PROJECT_ROOT = os.path.dirname(dummy.__file__)

if not PROJECT_ROOT:
    STATIC_ROOT = 'static'
    LOG_PATH = 'logs'
    INPUT_FILE_PATH = 'config/input.xls'
else:
    STATIC_ROOT = PROJECT_ROOT + '/static'
    LOG_PATH = '%s/logs' % PROJECT_ROOT
    INPUT_FILE_PATH = '%s/config/input.xls' % PROJECT_ROOT


MYSQL_USER = 'ju_user'
MYSQL_PASSWORD = 'ju201412'
