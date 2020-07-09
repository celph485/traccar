import logging
import os
import platform
from pathlib import Path

CONFIG_PROP_LOC = 'D:\\app\\g\\traccar\\setup\\config.properties'
MAPPING_PROP_LOC = 'D:\\app\\g\\traccar\\setup\\mapping.properties'
__dir_sep = os.path.sep
__usr_home = str(Path.home())
__app_name = 'external'


def create_config():
    print('Creating config')
    def_dict = __get_default_config()
    config_dict = __get_config_dict()
    config = {**def_dict, **config_dict}
    return config.copy()


def get_mapping_dict():
    print('Reading mapping properties.')
    return __read_data_from_prop_file(MAPPING_PROP_LOC)


def __get_default_config():
    return {
        'APP_NAME': __app_name,
        'SYS_NAME': platform.system(),
        'SYS_RELEASE': platform.release(),
        'SYS_VERSION': platform.version(),
        'DIR_SEP': __dir_sep,
        'USER_DIR': __usr_home,
        'LOG_DIR': "{}{}{}{}logs".format(__usr_home,
                                         __dir_sep,
                                         __app_name,
                                         __dir_sep),
        'CURR_LOG_LEVEL': 10,
        'DEF_DATE_FORMAT': '%Y_%m_%d',
        'DEF_DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
        'MAX_LOG_FILE_SIZE_IN_BYTES': 20_000_000,
        'MAX_BACKUP_PER_DAY': 2_000
    }


def __get_config_dict():
    print('Reading config properties.')
    return __read_data_from_prop_file(CONFIG_PROP_LOC)


def __read_data_from_prop_file(file_path):
    prop = {}
    print('Reading properties from {}'.format(file_path))
    with open(file_path, 'r') as f:
        for line in f:
            # removes trailing whitespace and '\n' chars
            line = line.rstrip()

            if "=" not in line:
                # skips blanks and comments w/o =
                continue

            if line.startswith("#"):
                # skips comments which contain =
                continue

            k, v = line.split("=", 1)
            k = __format_key(k)
            prop[k] = v
    return prop.copy()


def __format_key(key_str):
    str_1 = key_str.replace('-', '_')
    str_2 = str_1.upper()
    return str_2
