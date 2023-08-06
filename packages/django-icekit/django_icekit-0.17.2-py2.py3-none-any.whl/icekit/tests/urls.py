from django.conf.urls import patterns, url, include
from icekit.project.glamkit_urls import urlpatterns as glamkit_patterns

urlpatterns = patterns(
    '',
    url(r'^404/$', 'icekit.response_pages.views.page_not_found', name='404'),
    url(r'^500/$', 'icekit.response_pages.views.server_error', name='500'),
    url(r'^', include(glamkit_patterns)),
)
