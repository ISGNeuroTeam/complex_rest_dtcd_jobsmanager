from rest.views import APIView
from rest.response import Response, status
from rest.permissions import AllowAny, IsAuthenticated
import uuid
import logging
from .. import settings
from ..manager_singleton import MANAGER

log = logging.getLogger('jobsmanager_transit')
log.setLevel(settings.ini_config['logging']['level'])


class CheckJob(APIView):
    handler_id = str(uuid.uuid4())
    permission_classes = (AllowAny, )

    http_method_names = ['get', 'post']

    def _check_job(self, request):
        try:
            request.arguments["original_otl"][0] = request.arguments["original_otl"][0].encode('utf-8')
            response = MANAGER.check_job(hid=self.handler_id, request=request)
        except Exception as e:
            error_msg = {"status": "rest_error", "server_error": "Internal Server Error", "status_code": 500,
                         "error": e.args[0]}
            return Response(error_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response, status.HTTP_200_OK)

    def get(self, request):
        request.arguments = dict(request.GET)
        return self._check_job(request)

    def post(self, request):
        request.arguments = request.data
        request.arguments = {k: [str(v)] for k, v in request.arguments.items()}
        return self._check_job(request)
