import sys
import asyncio
import os
import logging
from configparser import ConfigParser
from psycopg2.pool import ThreadedConnectionPool
from message_broker import AsyncConsumer as Consumer
from json import loads
from jobsmanager_transit.wrappers.simple_request import SimpleRequest
from jobsmanager_transit.ot_simple_rest.utils.primitives import EverythingEqual
from jobsmanager_transit.ot_simple_rest.jobs_manager.manager import JobsManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # in order to override loggers from simple rest
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('worker')


async def async_range(count):
    for i in range(count):
        yield i


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

    manager = JobsManager(db_pool, mem_conf, disp_conf, resolver_conf)

    topic = 'testopic'

    async with Consumer(topic, value_deserializer=loads) as consumer:
        async for msg in consumer:
            logger.info('received message')
            job_description = msg.value
            logger.info(job_description)
            request = SimpleRequest(job_description['body_arguments'], job_description['remote_ip'])

            await manager.make_job(
                hid=job_description['handler_id'],
                request=request,
                indexes=[EverythingEqual()])  # todo authorization
            queue_size = manager.jobs_queue.qsize()
            logger.info('job was made')
            async for _ in async_range(queue_size):
                job = await manager.jobs_queue.get()
                logger.info('Got a job from queue')
                try:
                    await job.start_make()
                except Exception as e:
                    logger.error(f'Error occurred while start making job: {e}')
                await asyncio.sleep(0.001)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
