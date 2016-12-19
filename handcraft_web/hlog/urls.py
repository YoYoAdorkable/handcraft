# coding:utf-8
from django.conf.urls import patterns, include, url
from hlog.views import *

urlpatterns = patterns('',
    url(r'^$', log_list),
    url(r'^log_list/(\w+)/$', log_list),
    url(r'^log_kill/', log_kill),
    url(r'^history/$', log_history),
    url(r'^search/$', log_search),
    url(r'^log_weblog/$', log_weblog),
    url(r'^log_urllist/$', log_urllist),
    url(r'^log_errorlist/$', log_errorlist),
)
