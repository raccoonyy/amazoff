from actstream import action
from amazon.api import AmazonAPI
from datetime import date, timedelta
from django.conf import settings
from django.core.management.base import NoArgsCommand
from publication.models import *
import time


class Command(NoArgsCommand):
    help = 'Download New Books from Amazon'

    def handle(self, *args, **options):
        amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
        yesterday = date.today() - timedelta(days=1)
        pubs = Publisher.objects.filter(last_updated__gte=yesterday)
        # pubs = Publisher.objects.all()

        for pub in pubs:
            print "=== Check for publisher: \'%s\'" % pub
            amazon_books = amazon.search_n(150, SearchIndex='Books', Publisher=pub, BrowseNode='5', Power='pubdate:after 2012', Sort='daterank')

            for amazon_book in amazon_books:
                if amazon_book.isbn is None:
                    continue
                try:
                    dbbook = Book.objects.get(isbn__exact=amazon_book.isbn)
                    dbbook.update(amazon_book)
                except Book.DoesNotExist:
                    Book.objects.create_book(amazon_book)
            pub.save()
            time.sleep(4)

        print "=== Successful downloaded new books"
