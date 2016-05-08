'''
Created on May 8, 2016

@author: jvazquez
'''
import os

from configparser import ConfigParser
import logconfig

CONFIG_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             "../compose/configuration"))
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.ini")
LOG_CONFIG = os.path.join(CONFIG_FOLDER, "logging.json")


def get_config():
    configuration = ConfigParser()
    configuration.read(CONFIG_FILE)
    return configuration


def setup_log():
    logconfig.from_json(LOG_CONFIG)
