# coding:utf-8
from django.conf.urls import patterns, include, url
from hmonit.views import *

urlpatterns = patterns('',
    url(r'^monit_add/$', monit_add),
    url(r"^monit_add_multi/$", monit_add_batch),
    url(r'^monit_list/$', monit_list),
    url(r'^monit_iplist/$', monit_iplist),
    url(r'^monit_urllist/$', monit_urllist),
    url(r'^monit_urllist1/$', monit_urllist1),
    url(r'^monit_alarmlist/$', monit_alarmlist),
    url(r'^monit_dnslist/$', monit_dnslist),
    url(r'^monit_dnsadd/$', monit_dnsadd),
    url(r'^monit_dnstail/$', monit_dnstail),
    url(r'^monit_dnsedit/$', monit_dnsedit),
    url(r'^monit_dnsalarmlist/$', monit_dnsalarmlist),
    url(r'^monit_dnsalarmdel/(\w+)/$', monit_dnsalarmdel),
    url(r'^monit_portlist/$', monit_portlist),
    url(r'^monit_portadd/$', monit_portadd),
    url(r'^monit_porttail/$', monit_porttail),
    url(r'^monit_portedit/$', monit_portedit),
    url(r'^monit_port_iplist/$', monit_port_iplist),
    url(r'^monit_port_list/$', monit_port_list),
    url(r'^monit_portdel/(\w+)/$', monit_portdel),
    url(r'^monit_port_ipdel/(\w+)/$', monit_port_ipdel),
    url(r'^monit_port_del/(\w+)/$', monit_port_del),
    url(r'^search/$', monit_search),
    #url(r'^errorlog_search/$', monit_errorlog_search),
    url(r"^monit_detail/$", monit_detail),
    #url(r"^dept_host_ajax/$", dept_host_ajax),
    url(r"^show_all_ajax/$", show_all_ajax),
    #url(r'^idc_add/$', idc_add),
    #url(r'^idc_list/$', idc_list),
    #url(r'^idc_edit/$', idc_edit),
    #url(r'^idc_detail/$', idc_detail),
    #url(r'^idc_del/$', idc_del),
    #url(r'^group_add/$', group_add),
    #url(r'^group_edit/$', group_edit),
    #url(r'^group_list/$', group_list),
    #url(r'^group_detail/$', group_detail),
    #url(r'^group_del_host/$', group_del_host),
    #url(r'^group_del/$', group_del),
    url(r'^monit_del/(\w+)/$', monit_del),
    url(r'^monit_iplistdel/(\w+)/$', monit_iplistdel),
    url(r'^monit_dnsdel/(\w+)/$', monit_dnsdel),
    url(r'^monit_alarmdel/(\w+)/$', monit_alarmdel),
    url(r'^monit_edit/$', view_splitter, {'su': monit_edit, 'adm': monit_edit_adm}),
    #url(r'^monit_edit/batch/$', monit_edit_batch),
    #url(r'^monit_edit_common/batch/$', monit_edit_common_batch),
)
