import logging
import uuid

from complex_rest_dtcd_jobsmanager.ot_simple_rest.handlers.eva.db_connector import PostgresConnector


class BaseHandlerMod:

    def __init__(self, db_conn_pool):
        self.logger = logging.getLogger('osr_hid')
        self.db = PostgresConnector(db_conn_pool)
        self.handler_id = str(uuid.uuid4())