from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'blog.blogapp.views',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^blog/search/', include('haystack.urls')),

    (r'blog/entry/(.*)/$', 'entry'),
    (r'blog/author/(.*)/$', 'author'),
    (r'blog/tag/(.*)/$', 'tag'),
    (r'blog/$', 'list_entries'),
    (r'authors/$', 'list_authors'),
    (r'tags/$', 'list_tags'),
    (r'^$', redirect_to, dict(url='/blog/')),
)
