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
    url(r'^books/new/in_(?P<delta>\d+)days/$', new_books, name='new_books'),
    url(r'^books/updated/$', updated_books, name='updated_books'),
    url(r'^books/updated/in_(?P<delta>\d+)days/$', updated_books, name='updated_books'),
    url(r'^books/ranked/$', ranked_books, name='ranked_books'),
    # url(r'^books/ranked/$', ranked_books, name='ranked_books'),
    url(r'^books/ranked/(?P<day>\d+)days_ago/$', ranked_books, name='ranked_books'),
    url(r'^books/ranked/(?P<day>\w+)/$', ranked_books, name='ranked_books'),
    url(r'^book/add/(?P<isbn>\d{9}[\d|X])/$', add_book, name='add_book'),
    url(r'^book/add/(?P<isbn>\d{12}[\d|X])/$', add_book, name='add_book'),
    url(r'^book/search/$', book_search, name='book_search'),

    ('^activity/', include('actstream.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
