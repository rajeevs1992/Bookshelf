from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$','bookshelf.views.index'),
	(r'^login/','bookshelf.views.userLogin'),
	(r'^logout/','bookshelf.views.userLogout'),
	(r'^details/(?P<key>.*)/$','bookshelf.views.details'),
	(r'^download/(?P<key>.*)/$','bookshelf.views.download'),
	(r'^upload/','bookshelf.views.upload'),
	(r'^search/','bookshelf.views.search'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
		     'document_root': settings.MEDIA_ROOT,}),)
