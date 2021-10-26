import asyncio
from pathlib import Path
import os
import logging.config
from configparser import ConfigParser
from psycopg2.pool import ThreadedConnectionPool
from worker import manager_wrapper


# from task_scheduler.tasks import DbTasksSchduler
# import uwsgi

async def main():
    # # # # # #  Configuration section  # # # # # # #

    basedir = os.path.dirname(os.path.abspath(__file__))

    config = ConfigParser()
    config.read(os.path.join(basedir, 'worker/ot_simple_rest.conf'))

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

    manager = manager_wrapper.JobsManagerWrapper(db_conn_pool=db_pool, mem_conf=mem_conf, disp_conf=disp_conf,
                                                 resolver_conf=resolver_conf)
    await manager.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
