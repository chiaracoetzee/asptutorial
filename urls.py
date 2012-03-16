from django.conf.urls.defaults import patterns, include, url
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^demo/$', 'demo.views.index'),
    url(r'^demo/runsejits/$', 'demo.views.runsejits'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # In production these are served directly as static documents, this
    # is used only in debug mode.
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.dirname(__file__) + '/resources'}),
)
