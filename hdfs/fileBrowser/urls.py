from django.conf.urls import patterns, url

from fileBrowser import views

urlpatterns = patterns('',
    #url(r'^$', views.list_view, name='list_view')
    #url(r'^$', views.browser_view, name='browser_view')
	url(r'^browser$', views.browser_view, name='browser_view'),
    url(r'^api$', views.api_view, name='api_view')
)
