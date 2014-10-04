from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('devel.views',
    url(r'^$', 'index'),
    url(r'^create/$', 'create'),
    url(r'^cluster/$', 'cluster'),
    url(r'^check_image/$', 'check_image'),
    url(r'^check_image/(?P<page>\d+)/$', 'check_image'),
    url(r'^image_group/(?P<image_group_type_id>\d+)/(?P<num>\d+)/(?P<page>\d+)/$', 'image_group'),
)
