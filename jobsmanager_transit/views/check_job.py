from rest.views import APIView
from rest.response import Response, status
from rest.permissions import AllowAny
import uuid
import logging
from .. import settings

log = logging.getLogger('jobsmanager_transit')
log.setLevel(settings.ini_config['logging']['level'])


class CheckJob(APIView):
    handler_id = str(uuid.uuid4())
    permission_classes = (AllowAny,)

    http_method_names = ['get']

    def get(self, request):
        request.arguments = dict(request.GET)
        try:
            request.arguments["original_otl"][0] = request.arguments["original_otl"][0].encode('utf-8')
            response = settings.MANAGER.check_job(hid=self.handler_id, request=request)
        except Exception as e:
            error_msg = {"status": "rest_error", "server_error": "Internal Server Error", "status_code": 500,
                         "error": e.args[0]}  # weird
            # add logs
            return Response({'message': str(error_msg)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # add logs
        return Response({'message': str(response)}, status.HTTP_200_OK)
