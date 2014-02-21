from django.conf.urls import patterns, url, include
from tasks import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
#     url(r'^(?P<product_id>\d+)/projects/$', views.project_index, name='project_index'),
    url(r'^(?P<task_id>\d+)/$', views.detail,name='detail'),
#     url(r'^(?P<product_id>\d+)/(?P<project_id>\d+)/$', views.detail_project,name='detail_project'),
    url(r'^create/$', views.create_task,name='create_task'),
    url(r'^edit/(?P<task_id>\d+)$', views.edit_task,name='edit_task'),
    url(r'^delete/(?P<task_id>\d+)$', views.delete_task,name='delete_task'),
#     url(r'^create_project/(?P<product_id>\d+)$', views.create_project,name='create_project'),
#     url(r'^(?P<product_id>\d+)/edit_project/(?P<project_id>\d+)$', views.edit_project,name='edit_project'),
#     url(r'^(?P<product_id>\d+)/delete_project/(?P<project_id>\d+)$', views.delete_project,name='delete_project'),
    url(r'^search_task/$', views.search_task, name='search_task'),
#     url(r'^search_project/$', views.search_project, name='search_project'),
)