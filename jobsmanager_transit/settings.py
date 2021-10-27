import configparser

from core.settings.ini_config import merge_ini_config_with_defaults

from pathlib import Path
import os
from configparser import ConfigParser
from psycopg2.pool import ThreadedConnectionPool

from wrappers import manager_wrapper

######################
# PRODUCER

# # # # # #  Configuration section  # # # # # # #

basedir = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser()
config.read(os.path.join(basedir, 'ot_simple_rest.conf'))

db_conf = dict(config['db_conf'])
db_conf_eva = dict(config['db_conf_eva'])
mem_conf = dict(config['mem_conf'])
disp_conf = dict(config['dispatcher'])
resolver_conf = dict(config['resolver'])
static_conf = dict(config['static'])
user_conf = dict(config['user'])
pool_conf = dict(config['db_pool_conf'])

# # # # # # # # # # # # # # # # # # # # # # # # # #

db_pool = ThreadedConnectionPool(int(pool_conf['min_size']), int(pool_conf['max_size']), **db_conf)
db_pool_eva = ThreadedConnectionPool(int(pool_conf['min_size']), int(pool_conf['max_size']), **db_conf_eva)

MANAGER = manager_wrapper.JobsManagerWrapper(db_conn_pool=db_pool, mem_conf=mem_conf, disp_conf=disp_conf,
                                             resolver_conf=resolver_conf)
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

config_parser.read(Path(__file__).parent / 'jobsmanager_transit.conf')

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
