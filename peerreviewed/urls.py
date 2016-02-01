from django.conf.urls import patterns, include, url
from django.contrib import admin
from browse.views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'peerreviewed.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name="index"),
)
