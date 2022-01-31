from psycopg2.pool import ThreadedConnectionPool


class ThreadedConnectionPoolWrapper(ThreadedConnectionPool):

    def __init__(self, minconn, maxconn, *args, **kwargs):
        super().__init__(minconn, maxconn, *args, **kwargs)

    def __del__(self):
        self.closeall()
