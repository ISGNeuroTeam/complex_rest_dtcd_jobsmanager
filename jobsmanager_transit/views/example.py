import logging

from cache import get_cache, cache_page

from rest.views import APIView
from rest.response import Response, status
from rest.permissions import IsAuthenticated, AllowAny

from settings import ini_config

# you can use default logger for plugin
log = logging.getLogger('jobsmanager_transit')

# use ini_config dictionary to get config from jobsmanager_transit.conf
log.setLevel(ini_config['logging']['level'])

# several caches available
# cache in Redis
c = get_cache('RedisCache', namespace='jobsmanager_transit', timeout=300, max_entries=300)

# cache in default complex rest databse
# c = get_cache('DatabaseCache', namespace='jobsmanager_transit', timeout=300, max_entries=300)

# c = get_cache('FileCache', namespace='jobsmanager_transit', timeout=300, max_entries=300)
# c = get_cache('LocMemCache', namespace='jobsmanager_transit', timeout=300, max_entries=300)

# Cache using example:
c.set('var_name', 'Some value', timeout=200)
# print(c.get('var_name'))


class ExampleView(APIView):
    # add permission classes AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
    permission_classes = (AllowAny, )

    # choose http methods you need
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get(self, request):
        # To get url params use request.GET dictionary
        # Example: request.GET.get('some param', None)

        log.info('Get request to jobsmanager_transit')
        return Response(
            {
                'message': 'plugin with name jobsmanager_transit created successfully. This is get request',
                'url_params': dict(request.GET)
            },
            status.HTTP_200_OK
        )

    def post(self, request):
        # To get body fields use request.data dictionary
        # request.data.get('some_field', None)

        log.info('Post request to jobsmanager_transit')
        return Response(
            {
                'message': 'plugin with name jobsmanager_transit created successfully. This is post request',
                'body_params': request.data
            },
            status.HTTP_200_OK
        )



