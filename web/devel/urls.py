from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('devel.views',
    url(r'^$', 'index'),
    url(r'^create/$', 'create'),
    url(r'^cluster/$', 'cluster'),
    url(r'^show_bing_images/$', 'show_bing_images'),
    url(r'^show_bing_images/(?P<page>\d+)/$', 'show_bing_images'),
)
