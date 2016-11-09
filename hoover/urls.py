from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hoover import views

urlpatterns = [
    url(r'^search/$', views.HooverSearch.as_view()),
    url(r'^hoover/$', views.HooverList.as_view()),
    url(r'^hoover/(?P<pk>[0-9]+)/$', views.HooverDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)