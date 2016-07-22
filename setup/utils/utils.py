#!/usr/bin/python
# -*- coding: utf-8; -*-

import os
import stat
import logging
from etc import settings


__all__ = ["Config", "Logger", "APP_ROOT"]


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s[%(process)d/%(threadName)s]: %(message)s",
    file_name="opswork_setup.log"
)
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CONFIG_DIR = os.path.join(APP_ROOT, "etc")
DEFAULT_CONF_FILE = "settings.py"
os.environ.setdefault("SETUP_OPSWORK", "setup.etc.settings")


class Logger(object):
    """
    Logging class
    """

    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR
    }

    def __init__(self, component=None):
        if component is None:
            component = self.__class__.__name__

        self.log_level = self.__class__.LOG_LEVELS.get(
            settings.LOGGER_LEVEL,
            logging.INFO
        )
        self.component = component

    def get_logger(self):
        logger = logging.getLogger(self.component)
        logger.setLevel(self.log_level)
        return logger