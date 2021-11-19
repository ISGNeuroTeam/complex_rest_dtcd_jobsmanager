from rest.views import APIView
from rest.response import Response, status
from rest.permissions import AllowAny
import uuid
import logging
from .. import settings

log = logging.getLogger('jobsmanager_transit')
log.setLevel(settings.ini_config['logging']['level'])


class GetResult(APIView):
    permission_classes = (AllowAny,)

    http_method_names = ['get']

    def get(self, request):
        request.arguments = dict(request.GET)
        return Response('results', status.HTTP_200_OK)