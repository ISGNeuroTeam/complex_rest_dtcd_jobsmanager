import asyncio
import logging
import re
import uuid

from complex_rest_dtcd_jobsmanager.ot_simple_rest.handlers.jobs.makejob import MakeJob
from rest_framework.request import Request

from rest.permissions import AllowAny

from rest.views import APIView
from rest.response import Response

from ..settings import user_conf
from .base_handler import BaseHandlerMod

from ..manager_singleton import MANAGER


class MakeJobMod(APIView, BaseHandlerMod, MakeJob):
    handler_id = str(uuid.uuid4())
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_index_access = False if user_conf.get('check_index_access') == 'False' else True
        self.jobs_manager = MANAGER
        self.logger = logging.getLogger('osr_hid')
        self.user_id = None

    @staticmethod
    def _get_client_ip(request_meta):
        x_forwarded_for = request_meta.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request_meta.get('REMOTE_ADDR')
        return ip

    def post(self, request: Request):
        remote_ip = self._get_client_ip(request.META)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            self.jobs_manager.jobs_queue.put({'handler_id': self.handler_id,
                                              'body_arguments': request.data,
                                              'remote_ip': remote_ip})
        )
        self.logger.debug(f'MakeJob RESPONSE: {response}', extra={'hid': self.handler_id})
        return Response(response)
