import logging
from complex_rest_jobsmanager_transit.wrappers.jobs_queue import JobsQueue
from complex_rest_jobsmanager_transit.ot_simple_rest.jobs_manager.manager import JobsManager
from complex_rest_jobsmanager_transit.ot_simple_rest.jobs_manager.jobs import Job

logger = logging.getLogger('osr_wrapped')


class JobsManagerWrapper(JobsManager):

    def __init__(self, db_conn_pool, mem_conf, disp_conf,
                 resolver_conf):
        super().__init__(db_conn_pool, mem_conf, disp_conf,
                         resolver_conf)
        self.jobs_queue = JobsQueue()


class FakeJobWrapper(Job):

    def __init__(self, *args, settings=None, **kwargs):
        if settings:
            super().__init__(id=0, request=None, db_conn=None, mem_conf=settings.mem_conf, resolver_conf=None,
                             tracker_max_interval=0, indexes=None)
            self.logger = logger
