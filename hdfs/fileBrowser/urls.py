from django.conf.urls import patterns, url

from fileBrowser import views

urlpatterns = patterns('',
    url(r'^$', views.list_view, name='list_view')
)
