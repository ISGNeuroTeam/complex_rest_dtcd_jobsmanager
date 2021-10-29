import asyncio
import logging
import re
import uuid

from jobsmanager_transit.ot_simple_rest.handlers.jobs.makejob import MakeJob
from rest_framework.request import Request

from rest.permissions import AllowAny

from rest.views import APIView
from rest.response import Response

from ..settings import user_conf, MANAGER
from .base_handler import BaseHandlerMod


class MakeJobMod(APIView, BaseHandlerMod, MakeJob):
    handler_id = str(uuid.uuid4())
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_index_access = False if user_conf['check_index_access'] == 'False' else True
        self.jobs_manager = MANAGER
        self.logger = logging.getLogger('osr_hid')
        self.user_id = None

    @staticmethod
    def _get_original_otl(query_str):
        original_otl = re.sub(r"\|\s*ot\s[^|]*\|", "", query_str)
        original_otl = re.sub(r"\|\s*simple[^\"]*", "", original_otl)
        original_otl = original_otl.replace("oteval", "eval")
        original_otl = original_otl.strip()
        return original_otl

    @staticmethod
    def _convert_to_binary(request_data):
        for data in request_data.values():
            data[0] = data[0].encode('utf-8')

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
        # original_otl = self._get_original_otl(
        #     request.data.get('original_otl', '')[0]  # why they put it in a LIST? cannot use a string pattern on a bytes-like object DECODE FIRST?
        # )
        self._convert_to_binary(request.data)  # todo for testing REMOVE
        # indexes = re.findall(r"index\s?=\s?([\"\']?_?\w*[\w*][_\w+]*?[\"\']?)", original_otl)
        # user_accessed_indexes = [EverythingEqual()] # todo authorization
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            # зовем продюсера: который передает словари
            self.jobs_manager.jobs_queue.put({'handler_id': self.handler_id,
                                              'body_arguments': request.data,
                                              'remote_ip': remote_ip,
                                              'indexes': ['*']})  # * means that EverythingEqual object is used
        )
        self.logger.debug(f'MakeJob RESPONSE: {response}', extra={'hid': self.handler_id})
        return Response(response)
