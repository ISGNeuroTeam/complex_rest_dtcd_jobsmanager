from .views.check_job import CheckJob
from .views.make_job import MakeJobMod
from .views.get_result import GetResult
from django.urls import re_path

__author__ = "Ilia Sagaidak"
__copyright__ = "Copyright 2021, ISG Neuro"
__credits__ = []
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Ilia Sagaidak"
__email__ = "isagaidak@isgneuro.com"
__status__ = "Dev"

urlpatterns = [
    re_path(r'^checkjob/?$', CheckJob.as_view()),
    re_path(r'^makejob/?$', MakeJobMod.as_view()),
    re_path(r'^getresult/?$', GetResult.as_view())
]
