from datetime import date, timedelta
from django.core.management.base import NoArgsCommand
from django.conf import settings
from amazon.api import AmazonAPI
from publication.models import *


class Command(NoArgsCommand):
    help = 'Update Amazon SalesRank for all books'

    def handle(self, *args, **options):
        amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
        yesterday = date.today() - timedelta(days=2)

        isbns = [book.isbn for book in Book.objects.filter(mod_date__lte=yesterday)]
        grouped_isbns = map(None, *[iter(isbns)]*10)

        print "=== Start daily book update."
        for index, isbns in enumerate(grouped_isbns):
            isbns = filter(None, isbns)
            isbns = ",".join(isbns)

            print " == index : %s / items : %s" % (str(index), isbns)
            amazon_books = amazon.lookup(ItemId=isbns)

            for amazon_book in amazon_books:
                try:
                    dbbook = Book.objects.get(isbn__exact=amazon_book.isbn)
                    dbbook.update(amazon_book)
                except Book.DoesNotExist:
                    Book.objects.create_book(amazon_book)

        print "=== Successful updated all books"
