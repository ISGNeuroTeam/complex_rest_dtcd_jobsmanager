import os
from configparser import ConfigParser
from psycopg2.pool import ThreadedConnectionPool
from complex_rest_dtcd_jobsmanager.wrappers import jobs_wrapper, pool_wrapper

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
pool_conf = dict(ot_simple_rest_conf['db_pool_conf'])

# # # # # # # # # # # # # # # # # # # # # # # # # #

db_pool = pool_wrapper.ThreadedConnectionPoolWrapper(int(pool_conf['min_size']), int(pool_conf['max_size']), **db_conf)

MANAGER = jobs_wrapper.JobsManagerWrapper(db_conn_pool=db_pool, mem_conf=mem_conf, disp_conf=disp_conf,
                                             resolver_conf=resolver_conf)