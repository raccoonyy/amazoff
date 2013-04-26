# -*- coding: utf-8 -*-
import re

from actstream.models import action_object_stream
from amazon.api import AmazonAPI
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from publication.models import *
from publication.views import *
from actstream.models import model_stream


def main(request):
    variables = {
        'user': request.user,
        'books': Book.objects.order_by('-mod_date')
    }
    return render(request, 'main.html', variables)


def book_search(request):
    if ('search_in_amazon' in request.GET) and (request.GET['search_in_amazon'] == u'true'):
        variables = book_search_in_amazon(request)

    if ('q' in request.GET) and (request.GET['q'] is not '') and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title'])

        books = Book.objects.filter(entry_query)

        variables = {
            'books': books
        }
        return render(request, 'book/book_search.html', variables)
    else:
        variables = {
            'books': False,
        }
    return render(request, 'book/book_search.html', variables)


def book_search_in_amazon(request):
    if ('q' in request.GET) and (request.GET['q'] is not '') and request.GET['q'].strip():
        query_string = request.GET['q']

        amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
        amazon_books = amazon.search_n(10, Keywords=query_string, SearchIndex='Books', BrowseNode='5', Sort='daterank')

        books = []
        for amazon_book in amazon_books:
            book = Book.objects.trans_from_amazon_book(amazon_book)
            b = Book.objects.filter(isbn=amazon_book.isbn)
            if len(b) > 0:
                book['pk'] = b[0].pk
            else:
                book['pk'] = 0
            books.append(book)

        variables = {
            'books': books,
        }
    return variables


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None    # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None   # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
