import datetime
from django.core.management.base import NoArgsCommand
from django.conf import settings
from amazon.api import AmazonAPI
from publication.models import *
from actstream import action


class Command(NoArgsCommand):
    help = 'Update Amazon SalesRank for all books'

    def handle(self, *args, **options):
        amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)

        isbns = [book.isbn for book in Book.objects.all()]
        grouped_isbns = map(None, *[iter(isbns)]*10)

        print "=== Start daily rank update."
        for index, isbns in enumerate(grouped_isbns):
            isbns = filter(None, isbns)
            isbns = ",".join(isbns)

            print " == index : %s / items : %s" % (str(index), isbns)
            books = amazon.lookup(ItemId=isbns)

            for item in books:
                if item.item.__dict__.get('SalesRank') is None:
                    continue
                dbbook = Book.objects.get(isbn__exact=item.isbn)
                r, create = Rank.objects.get_or_create(
                    date=datetime.date.today(),
                    book=dbbook
                )
                if create:
                    print "  = daily rank added for %s" % dbbook
                    r.rank = str(item.item.SalesRank)
                    r.save()
                    action.send(Rank, verb='Rank of %s is updated \'%s => %s\'' % (dbbook.title, dbbook.rank_set.latest('date').rank, r.rank))

        print "=== Successful updated all ranks"
