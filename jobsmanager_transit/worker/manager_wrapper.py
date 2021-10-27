import sys
sys.path.append('../plugin_dev/jobsmanager_transit/jobsmanager_transit/worker')
from jobs_manager.manager import JobsManager
import asyncio
import jobs_queue


class JobsManagerWrapper(JobsManager):

    def __init__(self, db_conn_pool, mem_conf, disp_conf,
                 resolver_conf):
        super().__init__(db_conn_pool, mem_conf, disp_conf,
                         resolver_conf)
        self.jobs_queue = jobs_queue.JobsQueue()

    async def _start_monitoring(self):
        """
        Runs endless loop with jobs check and execute code in it.

        :return:        None
        """

        print('Watchdog was started')
        # super().logger.info('Watchdog was started')
        loop = asyncio.get_event_loop()
        while self._enable:
            if not self.jobs_queue.empty():
                job = await self.jobs_queue.get()
                job = await job
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
