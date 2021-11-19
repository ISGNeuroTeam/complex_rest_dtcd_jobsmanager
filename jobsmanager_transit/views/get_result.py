import os

from rest.views import APIView
from rest.response import Response, status
from rest.permissions import AllowAny
import uuid
import logging

from wrappers.jobs_wrapper import FakeJobWrapper
from .. import settings

log = logging.getLogger('jobsmanager_transit')
log.setLevel(settings.ini_config['logging']['level'])


class GetResult(APIView):
    permission_classes = (AllowAny,)

    http_method_names = ['get']

    handler_id = str(uuid.uuid4())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('osr_hid')
        self.mem_conf = settings.mem_conf
        self.static_conf = settings.static_conf
        self.data_path = self.mem_conf['path']
        self.base_url = self.static_conf['base_url']
        self.with_nginx = False if settings.static_conf.get('use_nginx') == 'False' else True
        self._cache_name_template = 'search_{}.cache/data'

    def get(self, request):
        cid = dict(request.GET).get('cid')
        if not cid:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if self.with_nginx:
            return Response(self.generate_data_links(cid), status=status.HTTP_200_OK)
        else:
            return Response(self.load_and_send_from_memcache(cid), status=status.HTTP_200_OK)

    def generate_data_links(self, cid):
        """
        Makes listing of directory with cache data and generate links
        for that data with url pattern.

        :param cid:         OT_Dispatcher's job cid
        :return:
        """
        cache_dir = self._cache_name_template.format(cid)
        cache_full_path = os.path.join(self.data_path, cache_dir)

        if not os.path.exists(cache_full_path):
            self.logger.error('No cache with id={}'.format(cid))
            return self.write({'status': 'failed', 'error': 'No cache with id={}'.format(cid)})
            # raise tornado.web.HTTPError(405, f'No cache with id={cid}')

        self.logger.debug('Cache with id={} exists'.format(cid))
        listing = os.listdir(cache_full_path)
        cache_list = [f for f in listing if f.endswith('.json') or 'SCHEMA' in f]
        cache_list = [os.path.join(cache_dir, f) for f in cache_list]
        urls_list = [self.base_url.format(f) for f in cache_list]
        response = {"status": "success", "data_urls": urls_list}
        self.logger.debug(response)
        return response

    @staticmethod
    def load_and_send_from_memcache(cid):
        result = FakeJobWrapper(settings=settings).load_and_send_from_memcache(cid)
        return result
