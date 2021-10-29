import logging
from jobsmanager_transit.wrappers.jobs_queue import JobsQueue
from jobsmanager_transit.ot_simple_rest.jobs_manager.manager import JobsManager


logger = logging.getLogger('osr')


class JobsManagerWrapper(JobsManager):

    def __init__(self, db_conn_pool, mem_conf, disp_conf,
                 resolver_conf):
        super().__init__(db_conn_pool, mem_conf, disp_conf,
                         resolver_conf)
        self.jobs_queue = JobsQueue()
