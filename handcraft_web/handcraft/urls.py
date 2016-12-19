from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', 'handcraft.views.index'),
    (r'^api/user/$', 'handcraft.api.api_user'),
    (r'^skin_config/$', 'handcraft.views.skin_config'),
    #(r'^install/$', 'handcraft.views.install'),
    (r'^base/$', 'handcraft.views.base'),
    (r'^login/$', 'handcraft.views.login'),
    (r'^logout/$', 'handcraft.views.logout'),
    #(r'^file/upload/$', 'handcraft.views.upload'),
    #(r'^file/download/$', 'handcraft.views.download'),
    (r'^error/$', 'handcraft.views.httperror'),
    (r'^huser/', include('huser.urls')),
    (r'^hasset/', include('hasset.urls')),
    (r'^hmonit/', include('hmonit.urls')),
    (r'^hlog/', include('hlog.urls')),
    #(r'^jperm/', include('hperm.urls')),
    (r'^node_auth/', 'handcraft.views.node_auth'),

)
