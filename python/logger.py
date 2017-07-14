#!/usr/bin/env python
#
# Copyright (C) 2017 ShadowMan
#
import logging


class LoggerDisabled(RuntimeWarning):
    pass


class LoggerNotInit(Exception):
    pass


class Logger(object):

    def __init__(self, level: str, console: bool=False, log_file: str=None,
                 message_fmt=None, time_fmt=None):
        self.level = level
        logging.basicConfig(level=level, format='')

        self.logger = logging.getLogger()
        self.formatter = None
        self.logger_init()
        self.formatter_init(message_fmt, time_fmt)
        self.handler_init(console, log_file)

    def logger_init(self):
        self.logger.setLevel(self.level)
        while len(self.logger.handlers):
            self.logger.removeHandler(self.logger.handlers[0])

    def formatter_init(self, message_fmt: str, time_fmt: str):
        if message_fmt is None:
            message_fmt = '%(asctime)-12s: %(levelname)-8s %(message)s'
        if time_fmt is None:
            time_fmt = '%m/%d/%Y %H:%M:%S'
        self.formatter = logging.Formatter(message_fmt, time_fmt)

    def handler_init(self, console: bool, log_file: str):
        if log_file is not None:
            handler = logging.FileHandler(log_file)
        elif console is True:
            handler = logging.StreamHandler()
        else:
            raise LoggerDisabled('logger disabled now')

        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)
        logging.getLogger('').addHandler(handler)

    @staticmethod
    def logger_level(level: str):
        level = str(level).upper()
        if level == 'DEBUG':
            return logging.DEBUG
        elif level == 'INFO':
            return logging.INFO
        elif level == 'WARNING':
            return logging.WARNING
        elif level == 'ERROR':
            return logging.ERROR
        else:
            return logging.INFO

    @staticmethod
    def get_instance():
        if not hasattr(Logger, 'g_instance'):
            raise LoggerNotInit('please init logger first')
        return getattr(Logger, 'g_instance')


def init(level: str, console: bool=False, log_file: str=None,
         message_fmt=None, time_fmt=None):
    Logger.g_instance = Logger(level, console, log_file, message_fmt, time_fmt)


def debug(message):
    logging.debug(message)


def info(message):
    logging.info(message)


def warning(message):
    logging.warning(message)


def error(message):
    logging.error(message)


def error_exit(message):
    error(message)
    exit()
