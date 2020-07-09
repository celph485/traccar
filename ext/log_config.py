import logging
from config_file import *
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import date


class LogConfig:

    __level = config['CURR_LOG_LEVEL']

    def __init__(self, name):
        self.__name = name

    @classmethod
    def __log_file_path(cls):
        Path(config['LOG_DIR']).mkdir(parents=True, exist_ok=True)
        curr_date_str = date.today().strftime(config['DEF_DATE_FORMAT'])
        file_path = "{}{}{}_{}.log".format(config['LOG_DIR'], config['DIR_SEP'], config['APP_NAME'], curr_date_str)
        return file_path

    @classmethod
    def __get_file_handler(cls):
        max_file_size = config['MAX_LOG_FILE_SIZE_IN_BYTES']
        max_file_backup = config['MAX_BACKUP_PER_DAY']
        file_path = LogConfig.__log_file_path()
        file_fmt = '%(asctime)s :: %(levelname)-8s :: %(message)s'
        handler = RotatingFileHandler(file_path,
                                      maxBytes=max_file_size,
                                      backupCount=max_file_backup,
                                      delay=True)
        handler.setFormatter(logging.Formatter(file_fmt))
        return handler

    @classmethod
    def __get_console_handler(cls):
        console_fmt = '%(levelname)-8s :: %(filename)-18s:%(lineno)3d :: %(message)s'
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(console_fmt))
        return handler

    def get_logger(self):
        log = logging.getLogger(self.__name)
        log.setLevel(LogConfig.__level)
        log.addHandler(LogConfig.__get_file_handler())
        log.addHandler(LogConfig.__get_console_handler())
        return log
