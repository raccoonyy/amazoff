# -*- coding: utf-8 -*-
import re

from actstream.models import action_object_stream
# from actstream.models import model_stream
from amazon.api import AmazonAPI
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# from django.core.urlresolvers import reverse
from django.db.models import Min, Count
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from publication.models import Author, Book, Publisher, Rank


# def main(request):
#     variables = {
#         'user': request.user,
#         'books': Book.objects.filter(rank__rank__lte=10000)[:30]
#     }
#     return render(request, 'main.html', variables)


def main(request):
    """
    ``User`` focused activity stream.
    """

    return redirect('/books/')


class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'


class PublisherList(ListView):
    model = Publisher
    context_object_name = 'publishers'
    queryset = Publisher.objects.order_by('name')


class PublisherDetail(DetailView):
    model = Publisher
    queryset = Publisher.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        order = 'title'
        if 'order' in self.kwargs:
            order = self.kwargs['order']
        if order == 'title':
            context['book_list'] = Book.objects.filter(publisher=self.object).order_by('title')
        if order == 'publication_date':
            context['book_list'] = Book.objects.filter(publisher=self.object).order_by('-publication_date')
        if order == 'rank':
            context['book_list'] = Book.objects.filter(publisher=self.object, rank__isnull=False).annotate(min_rank=Min('rank__rank')).order_by('min_rank')

        context['order'] = order
        context['publisher'] = self.object
        context['publishers'] = Publisher.objects.all()

        return context


class PublisherBookList(ListView):
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.args[0])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super(PublisherBookList, self).get_context_data(**kwargs)
        context['publisher'] = self.publisher
        context['publishers'] = Publisher.objects.all()
        return context


def books(request):
    return render(request, 'main.html', {'books': Book.objects.order_by('-create_date')[:100]})


def new_books(request, delta=1):
    delta = int(delta)
    days_ago = date.today() - timedelta(days=delta)
    ctype = ContentType.objects.get_for_model(User)
    actor = request.user
    created_streams = User.objects.get(username='created_streams')
    action_list = action_object_stream(created_streams, timestamp__gte=days_ago)

    variables = {
        'ctype': ctype,
        'actor': actor,
        'action_list': action_list,
        'delta': delta,
    }

    return render(request, 'activity/new_actions.html', variables)


def updated_books(request, delta=1):
    delta = int(delta)
    days_ago = date.today() - timedelta(days=delta)
    ctype = ContentType.objects.get_for_model(User)
    actor = request.user
    updated_streams = User.objects.get(username='updated_streams')
    action_list = action_object_stream(updated_streams, timestamp__gte=days_ago)

    variables = {
        'ctype': ctype,
        'actor': actor,
        'action_list': action_list,
        'days_ago': days_ago,
    }

    return render(request, 'activity/updated_actions.html', variables)


def ranked_books(request, day='all'):
    # delta = int(delta)
    # days_ago = date.today() - timedelta(days=delta)

    # for r in Rank.objects.filter(rank__lte=rank_range).order_by('rank'):
    #     if r.target_actions.exists() and r.target_actions.get().timestamp.date() >= days_ago:
    #         action_list.append(r.target_actions.get())
    # # action_list = [action for action in model_stream(Rank) if action.target.rank < range]
    # ctype = ContentType.objects.get_for_model(User)
    # actor = request.user
    if day == 'all':
        return render(request, 'book/ranked_all_books.html', {
            'books': Book.objects.filter(rank__isnull=False).annotate(min_rank=Min('rank__rank')).order_by('min_rank'),
        })

    day = int(day)
    days_ago = date.today() - timedelta(days=day)

    ranks = Rank.objects.filter(date=days_ago).order_by('rank').select_related()

    return render(request, 'book/ranked_books.html', {
        'ranks': ranks,
        'day': day
    })


def add_book(request, isbn):
    amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
    amazon_book = amazon.lookup(ItemId=isbn)
    Book.objects.create_book(amazon_book)

    if request.is_ajax():
        return HttpResponse(status=200)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))


def book_search(request):
    if ('search_in_amazon' in request.GET) and (request.GET['search_in_amazon'] == u'true'):
        variables = book_search_in_amazon(request)
        return render(request, 'book/book_search.html', variables)

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
        amazon_books = amazon.search_n(40, Keywords=query_string, SearchIndex='Books', BrowseNode='5', Sort='daterank')

        books = []
        for amazon_book in amazon_books:
            if amazon_book.isbn is None:
                continue
            book = Book.objects.trans_amazon_to_book(amazon_book)
            b = Book.objects.filter(isbn=amazon_book.isbn)
            if len(b) > 0:
                book['pk'] = b[0].pk
            else:
                book['pk'] = 0
            books.append(book)

        variables = {
            'books': books,
            'search_in_amazon': True
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
