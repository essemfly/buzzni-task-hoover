from django.conf.urls import url
from hoover import views

urlpatterns = [
    url(r'^hoover/$', views.hoover_list),
    url(r'^hoover/(?P<pk>[0-9]+)/$', views.hoover_detail),
]