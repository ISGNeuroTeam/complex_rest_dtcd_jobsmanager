from rest.views import APIView
from rest.response import Response, status
from rest.permissions import AllowAny
import uuid
import logging
from .. import settings

log = logging.getLogger('jobsmanager_transit')
# log.info('plugin works at testview')

class TestJob:
    def __init__(self):
        self.handler_id = 21
        self.request = 42
        self.indexes = None
        self.db = 'connection pool'
        self.mem_conf = 'mem_conf'
        self.resolver_conf = 'resolver_conf'
        self.tracker_max_interval = 10
        self.status = {'status': 'created'}
        self.resolved_data = None
        self.search = None


class TestView(APIView):
    handler_id = str(uuid.uuid4())
    permission_classes = (AllowAny,)

    http_method_names = ['get']

    def get(self, request):
        log.info('>get started')
        try:
            response = 'check if worker got the message'
            j = TestJob()
        except Exception as e:
            error_msg = {"status": "rest_error", "server_error": "Internal Server Error", "status_code": 500,
                         "error": e.args[0]}  # weird
            # add logs
            return Response({'message': str(error_msg)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # add logs
        return Response({'message': str(response)}, status.HTTP_200_OK)