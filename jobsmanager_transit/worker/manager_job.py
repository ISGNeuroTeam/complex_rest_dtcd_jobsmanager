import logging
import re
from jobs_manager.jobs import Job
from parsers.otl_resolver.Resolver import Resolver


class ManagerJob(Job):

    def __init__(self, *, id, request, db_conn, mem_conf, resolver_conf,
                 tracker_max_interval, indexes=None):
        super().__init__(id=id, request=request, db_conn=db_conn, mem_conf=mem_conf, resolver_conf=resolver_conf,
                         tracker_max_interval=tracker_max_interval, indexes=indexes)
        # to serialize and transmit this object to another process (consumer). Will be assigned after deserialization
        self.db_conn = None
