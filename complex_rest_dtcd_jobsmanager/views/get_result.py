import os

from rest.views import APIView
from rest.response import Response, status
from rest.permissions import AllowAny
import uuid
import logging

from ..wrappers.jobs_wrapper import FakeJobWrapper
from .. import settings
from ..manager_singleton import CONNECTOR
from ot_simple_connector.job import Job
from ..exceptions import CacheExists

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
        self.distribution_conf = settings.distribution_conf
        self.data_path = self.mem_conf['path']
        self.base_url = self.static_conf['base_url']
        self.monolith = False if settings.distribution_conf.get('monolith') == 'False' else True
        self.with_nginx = False if settings.static_conf.get('use_nginx') == 'False' else True
        self._cache_name_template = 'search_{}.cache/data'
        self._schema = '_SCHEMA'

    def get(self, request):
        cid = dict(request.GET).get('cid')
        if not cid:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cid = cid[0]
        if not self.monolith:
            try:
                self.copy_dataset_from_platform(cid)
            except CacheExists:
                return Response(self.load_and_send_from_memcache(cid), status=status.HTTP_200_OK)
            return Response(self.generate_data_links(cid), status=status.HTTP_200_OK)
        elif self.with_nginx:
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
            return {'status': 'failed', 'error': f'No cache with id={cid}'}

        self.logger.debug('Cache with id={} exists'.format(cid))
        listing = os.listdir(cache_full_path)
        cache_list = [f for f in listing if f.endswith('.json') or self._schema in f]
        cache_list = [os.path.join(cache_dir, f) for f in cache_list]
        urls_list = [self.base_url.format(f) for f in cache_list]
        response = {"status": "success", "data_urls": urls_list}
        self.logger.debug(response)
        return response

    def copy_dataset_from_platform(self, cid):
        job = Job(session=CONNECTOR.session,
                      query_text=None,
                      cache_ttl=None,
                      tws=None,
                      twf=None,
                      sid=cid)

        job.cid = cid

        dataset = job.dataset

        cache_dir = self._cache_name_template.format(cid)
        cache_full_path = os.path.join(self.data_path, cache_dir)

        if os.path.exists(cache_full_path):
            self.logger.warning('Cache with id={} already exists'.format(cid))
            raise CacheExists
        os.makedirs(cache_full_path)
        for url in dataset.data_urls:
            chunk = CONNECTOR.session.get(url).text
            with open(os.path.join(cache_full_path, url[url.rfind(os.sep) + 1:]), 'w') as fw:
                fw.write(chunk)
        with open(os.path.join(cache_full_path, self._schema), 'w') as fw:
            fw.write(dataset.schema)
        self.logger.debug('Dataset for id={} copied'.format(cid))

    @staticmethod
    def load_and_send_from_memcache(cid):
        result = FakeJobWrapper(settings=settings).load_and_send_from_memcache(cid)
        return result
