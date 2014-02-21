from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from products import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index),
    # url(r'^easycase/', include('easycase.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('pages.urls', namespace="pages")),
    url(r'^products/', include('products.urls', namespace="products")),
    url(r'^tasks/', include('tasks.urls', namespace="tasks")),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'pages.views.logout_view'),
)
