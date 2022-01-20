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

# # # # # # # # # # # # # # # # # # # # # # # # # #

# db_pool = ThreadedConnectionPool(int(pool_conf['min_size']), int(pool_conf['max_size']), **db_conf)
#
# MANAGER = jobs_wrapper.JobsManagerWrapper(db_conn_pool=db_pool, mem_conf=mem_conf, disp_conf=disp_conf,
#                                              resolver_conf=resolver_conf)
######################

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
config_parser.read(__file__ + '../jobsmanager_transit.conf')

ini_config = merge_ini_config_with_defaults(config_parser, default_ini_config)

# configure your own database if you need
# DATABASE = {
#         "ENGINE": 'django.db.backends.postgresql',
#         "NAME": ini_config['db_conf']['database'],
#         "USER": ini_config['db_conf']['user'],
#         "PASSWORD": ini_config['db_conf']['password'],
#         "HOST": ini_config['db_conf']['host'],
#         "PORT": ini_config['db_conf']['port']
# }
