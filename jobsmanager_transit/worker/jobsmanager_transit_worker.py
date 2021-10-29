import sys
sys.path.insert(0, '.')
from core.settings.base import PLUGINS_DIR
sys.path.insert(1, PLUGINS_DIR)
import asyncio
import os
from configparser import ConfigParser
from psycopg2.pool import ThreadedConnectionPool
from jobsmanager_transit.ot_simple_rest.jobs_manager.jobs import Job
from message_broker import AsyncConsumer as Consumer
from json import loads
from jobsmanager_transit.wrappers.simple_request import SimpleRequest
from jobsmanager_transit.ot_simple_rest.utils.primitives import EverythingEqual
import logging
# from cloudpickle import loads
# from jobsmanager_transit.wrappers import manager_wrapper

# from task_scheduler.tasks import DbTasksSchduler
# import uwsgi

async def main():
    # # # # # #  Configuration section  # # # # # # #

    basedir = os.path.dirname(os.path.abspath(__file__))

    config = ConfigParser()
    config.read(os.path.join(basedir, '../ot_simple_rest.conf'))

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

    # manager = manager_wrapper.JobsManagerWrapper(db_conn_pool=db_pool, mem_conf=mem_conf, disp_conf=disp_conf,
    #                                              resolver_conf=resolver_conf)
    # await manager.start()
    topic = 'testopic'

    async with Consumer(topic, value_deserializer=loads) as consumer:
        async for msg in consumer:
            print('received message')
            # вызываем await makejob у менеджера
            # async for
            job_description = msg.value
            print(job_description)
            request = SimpleRequest(job_description['request']['body_arguments'],  # словарь передаем
                                    job_description['request']['remote_ip'])
            if job_description['indexes'][0] == '*':
                job_description['indexes'][0] == EverythingEqual()
            else:
                pass  # todo authorization
            job = Job(id=job_description['handler_id'],
                      request=request,
                      indexes=job_description['indexes'],
                      db_conn=db_pool,
                      mem_conf=job_description['mem_conf'],
                      resolver_conf=job_description['resolver_conf'],
                      tracker_max_interval=job_description['tracker_max_interval'])
            job.status = job_description['status']
            job.resolved_data = job_description['resolved_data']
            job.search = job_description['search']
            job.logger = logging.getLogger('osr_hid')
            # job.db = db_pool  # injected
            print('job recreated')
            asyncio.create_task(job.start_make())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
