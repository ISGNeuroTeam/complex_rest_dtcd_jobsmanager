from cache import cache_page
from .views.check_job import CheckJob
from .views.make_job import MakeJobMod
from .views.get_result import GetResult
from django.urls import re_path

# Use cache_page decorator for caching view

# urlpatterns = [
#     path('example/', cache_page(60 * 15)(ExampleView.as_view())),
# ]

urlpatterns = [
    re_path(r'^checkjob/?$', CheckJob.as_view()),
    re_path(r'^makejob/?$', MakeJobMod.as_view()),
    re_path(r'^getresult/?$', GetResult.as_view())
]
