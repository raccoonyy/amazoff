# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
# from django.views.generic.simple import redirect_to
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
    url(r'^books/$', books, name='books'),
    url(r'^books/new/$', new_books, name='new_books'),
    url(r'^books/new/(?P<delta>\d+)days_ago/$', new_books, name='new_books'),
    url(r'^books/updated/$', updated_books, name='updated_books'),
    url(r'^books/updated/(?P<delta>\d+)days_ago/$', updated_books, name='updated_books'),
    url(r'^books/ranked/$', ranked_books, name='ranked_books'),
    url(r'^books/ranked/(?P<delta>\d+)days_ago/$', ranked_books, name='ranked_books'),
    url(r'^books/ranked/(?P<delta>\d+)days_ago/(?P<rank_range>\d+)/$', ranked_books, name='ranked_books'),
    url(r'^book/search/$', book_search, name='book_search'),

    ('^activity/', include('actstream.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
