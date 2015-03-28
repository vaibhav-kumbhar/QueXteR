from django.conf.urls import patterns,url
urlpatterns = patterns('project.apps.data.views',
	url(r'^homepage$','index',name="homepage_index"),
