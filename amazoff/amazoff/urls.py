# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from publication.views import *


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', main, name='main'),
    # url(r'^books/$', book_list.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Book,
            template_name='book/book_detail.html'
        ),
        name='book'),
    url(r'^book/$',
        ListView.as_view(
            queryset=Book.objects.order_by('-publication_date')[:20],
            context_object_name='books',
            template_name='book/searched_list.html',
        ),
        name='book_list'),
    url(r'^book/search/$', book_search, name='book_search'),

    ('^activity/', include('actstream.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
