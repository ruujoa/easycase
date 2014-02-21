# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from products import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^(?P<product_id>\d+)/projects/$', views.project_index, name='project_index'),
    url(r'^(?P<product_id>\d+)/$', views.detail,name='detail'),
    url(r'^(?P<product_id>\d+)/(?P<project_id>\d+)/$', views.detail_project,name='detail_project'),
    url(r'^create/$', views.create_product,name='create_product'),
    url(r'^edit/(?P<product_id>\d+)$', views.edit_product,name='edit_product'),
    url(r'^delete/(?P<product_id>\d+)$', views.delete_product,name='delete_product'),
    url(r'^create_project/(?P<product_id>\d+)$', views.create_project,name='create_project'),
    url(r'^(?P<product_id>\d+)/edit_project/(?P<project_id>\d+)$', views.edit_project,name='edit_project'),
    url(r'^(?P<product_id>\d+)/delete_project/(?P<project_id>\d+)$', views.delete_project,name='delete_project'),
    url(r'^search_product/$', views.search_product, name='search_product'),
    url(r'^search_project/$', views.search_project, name='search_project'),
    url(r'^upload/$', views.upload_file, name='upload'),
)
