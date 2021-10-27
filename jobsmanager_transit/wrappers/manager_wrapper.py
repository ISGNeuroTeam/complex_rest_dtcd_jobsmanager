import logging
import asyncio

from wrappers.jobs_queue import JobsQueue
from ot_simple_rest.jobs_manager.manager import JobsManager


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
        while self._enable:
            if not self.jobs_queue.empty():
                job = await self.jobs_queue.get()
                job = job.value
                print('testing', job.db, job.handler_id)
                job.db = self.db_conn  # injected
                print('Got a job from queue')
                # super().logger.debug('Got a job from queue')
                loop.create_task(job.start_make())
            else:
                await asyncio.sleep(0.05)
        print('Manager was stopped')
        # super().logger.info('Manager was stopped')
