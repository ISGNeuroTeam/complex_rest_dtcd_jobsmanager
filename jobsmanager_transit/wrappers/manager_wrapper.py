import logging
import asyncio

from jobsmanager_transit.wrappers.jobs_queue import JobsQueue
from jobsmanager_transit.ot_simple_rest.jobs_manager.manager import JobsManager


logger = logging.getLogger('osr')


class JobsManagerWrapper(JobsManager):

    def __init__(self, db_conn_pool, mem_conf, disp_conf,
                 resolver_conf):
        super().__init__(db_conn_pool, mem_conf, disp_conf,
                         resolver_conf)
        self.jobs_queue = JobsQueue()

    async def _start_monitoring(self):
        """
        Runs endless loop with jobs check and execute code in it.

        :return:        None
        """

        print('Watchdog was started')
        logger.info('Watchdog was started')
        loop = asyncio.get_running_loop()
        print(self._enable)
        while self._enable:
            print('check empty')
            if not self.jobs_queue.empty():
                print('getting the message')
                job = await self.jobs_queue.get()
                print('wessage received')
                job = job.value
                print('testing', job.db, job.handler_id)
                job.db = self.db_conn  # injected
                print('Got a job from queue')
                loop.create_task(job.start_make())
            else:
                await asyncio.sleep(0.05)
        print('Manager was stopped')
