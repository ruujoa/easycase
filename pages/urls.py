# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from pages import views

urlpatterns = patterns('',
    # Examples:
    url(r'^(?P<project_id>\d+)/$', views.index, name='index'),
    url(r'^(?P<project_id>\d+)/(?P<page_id>\d+)/elements/$', views.element_index, name='element_index'),
    url(r'^(?P<project_id>\d+)/(?P<page_id>\d+)/$', views.detail,name='detail'),
    url(r'^create/(?P<project_id>\d+)$', views.create_page,name='create_page'),
    url(r'^delete/(?P<project_id>\d+)/(?P<page_id>\d+)$', views.delete_page,name='delete_page'),
    url(r'^create_element/(?P<project_id>\d+)/(?P<page_id>\d+)$', views.create_element,name='create_element'),
    url(r'^(?P<project_id>\d+)/(?P<page_id>\d+)/edit_element/(?P<element_id>\d+)$', views.edit_element,name='edit_element'),
    url(r'^(?P<project_id>\d+)/(?P<page_id>\d+)/delete_element/(?P<element_id>\d+)$', views.delete_element,name='delete_element'),
    url(r'^search_page/$', views.search_page, name='search_page'),
    url(r'^search_element/$', views.search_element, name='search_element'),
)
