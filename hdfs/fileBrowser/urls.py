from django.conf.urls import patterns, url

from fileBrowser import views

urlpatterns = patterns('',
    url(r'^browser$', views.browser_view, name='browser_view'),
    url(r'^info$', views.dir_info, name='dir_info'),
    url(r'^gridListing$', views.grid_listing, name='grid_listing'),
    url(r'^api$', views.api_view, name='api_view'),
    url(r'^hdfsBrowser$', views.first_load, name='first_load'),
    url(r'^list$', views.list, name='list'),
    url(r'^mkdir$', views.mkdir, name='mkdir'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^move$', views.move, name='move'),
    url(r'^chown$', views.chown, name='chown'),
    url(r'^chmod$', views.chmod, name='chmod')
)
