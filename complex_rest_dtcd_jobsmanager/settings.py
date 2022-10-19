import configparser

from core.settings.ini_config import merge_ini_config_with_defaults

# from pathlib import Path
import os
from configparser import ConfigParser

######################
# PRODUCER

# # # # # #  Configuration section  # # # # # # #

basedir = os.path.dirname(os.path.abspath(__file__))

ot_simple_rest_conf = ConfigParser()
ot_simple_rest_conf.read(os.path.join(basedir, 'ot_simple_rest.conf'))

db_conf = dict(ot_simple_rest_conf['db_conf'])
mem_conf = dict(ot_simple_rest_conf['mem_conf'])
disp_conf = dict(ot_simple_rest_conf['dispatcher'])
resolver_conf = dict(ot_simple_rest_conf['resolver'])
static_conf = dict(ot_simple_rest_conf['static'])
user_conf = dict(ot_simple_rest_conf['user'])
pool_conf = dict(ot_simple_rest_conf['db_pool_conf'])
distribution_conf = dict(ot_simple_rest_conf['distribution'])

default_ini_config = {
    'logging': {
        'level': 'INFO'
    },
    'db_conf': {
        'host': 'localhost',
        'port': '5432',
        'database': 'jobsmanager_transit',
        'user': 'jobsmanager_transit',
        'password': 'jobsmanager_transit'
    }
}

config_parser = configparser.ConfigParser()

# config_parser.read(Path(__file__).parent / 'jobsmanager_transit.conf')
# config_parser.read(__file__ + '../jobsmanager_transit.conf')
config_parser.read(__file__[0:__file__.rfind('/')] + '/jobsmanager_transit.conf') # not allowed to use pathlib?
ini_config = merge_ini_config_with_defaults(config_parser, default_ini_config)
