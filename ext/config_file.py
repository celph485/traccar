import logging
import os
import platform
import config_builder as cb
from pathlib import Path

__dir_sep = os.path.sep
__usr_home = str(Path.home())
__app_name = 'external'

__config = {
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
    'MAX_BACKUP_PER_DAY': 2_000,
    'MQ_HOST': '120.63.189.207',
    'MQ_PORT': '5656',
    'MQ_USER': 'guest',
    'MQ_PASSWD': 'guest',
    'MQ_DEST': 'ext.gps.event.tc',
    'TARGET_WS_URL': 'http://103.231.40.50:5175',
}

config = cb.create_config()
mapping_config = cb.get_mapping_dict()

req = {
    'imei_no': '',
    'lattitude': '',
    'longitude': '',
    'lattitude_direction': 'N',
    'longitude_direction': 'E',
    'speed': '0',
    'digital_port1': '0',
    'digital_port2': '0',
    'digital_port3': '0',
    'digital_port4': '0',
    'analog_port1': '0',
    'analog_port2': '0',
    'angle': '0',
    'satellite': '0',
    'time': '',
    'battery_voltage': '20',
    'gps_validity': 'A'
}
