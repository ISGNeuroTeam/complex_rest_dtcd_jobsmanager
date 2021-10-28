import asyncio
import logging
import re

from jobsmanager_transit.ot_simple_rest.handlers.jobs.makejob import MakeJob
from rest_framework.request import Request

from rest.permissions import AllowAny

from rest.views import APIView
from rest.response import Response

from ..settings import user_conf, MANAGER
from .base_handler import BaseHandlerMod


class MakeJobMod(APIView, BaseHandlerMod, MakeJob):
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

    def post(self, request: Request):
        original_otl = self._get_original_otl(
            request.data.get('original_otl', '')
        )
        indexes = re.findall(r"index\s?=\s?([\"\']?_?\w*[\w*][_\w+]*?[\"\']?)", original_otl)
        if not request.user.id:
            pass
        else:
            self.user_id = request.user.guid  # TODO Check
        user_accessed_indexes = self.get_user_indexes_rights(indexes)
        if not user_accessed_indexes:
            return Response({"status": "fail", "error": "User has no access to index"})
        self.logger.debug(f'User has access. Indexes: {user_accessed_indexes}.', extra={'hid': self.handler_id})

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.jobs_manager.make_job(
                hid=self.handler_id,
                request=type('request', (type,), {'arguments': request.data, 'body_arguments': request.data}), # TODO Check! что аргументс, боди аргументс
                indexes=user_accessed_indexes)
        )
        self.logger.debug(f'MakeJob RESPONSE: {response}', extra={'hid': self.handler_id})
        return Response(response)
