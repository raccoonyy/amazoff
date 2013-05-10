import datetime
import time
from datetime import date, timedelta
from django.core.management.base import NoArgsCommand
from django.conf import settings
from amazon.api import AmazonAPI
from publication.models import *
from actstream import action


class Command(NoArgsCommand):
    help = 'Update Amazon SalesRank for all books'

    def handle(self, *args, **options):
        amazon = AmazonAPI(settings.AMAZON_ACCESS_KEY, settings.AMAZON_SECRET_KEY, settings.AMAZON_ASSOC_TAG)
        # yesterday = date.today() - timedelta(days=1)

        # isbns = [book.isbn for book in Book.objects.filter(mod_date__gte=yesterday)]
        isbns = [book.isbn for book in Book.objects.all()]
        grouped_isbns = map(None, *[iter(isbns)]*10)

        print "=== Start daily rank update."
        for index, isbns in enumerate(grouped_isbns):
            time.sleep(4)
            isbns = filter(None, isbns)
            isbns = ",".join(isbns)

            print " == index : %s / items : %s" % (str(index), isbns)
            books = amazon.lookup(ItemId=isbns)

            for item in books:
                if item.item.__dict__.get('SalesRank') is None:
                    continue
                dbbook = Book.objects.get(isbn__exact=item.isbn)

                try:
                    r = Rank.objects.get(date=datetime.date.today(), book=dbbook)
                    continue
                except:
                    pass

                print "  = daily rank added for %s" % dbbook
                r = Rank.objects.create(
                    date=datetime.date.today(),
                    book=dbbook,
                    rank=item.item.SalesRank
                )

                from django.contrib.auth.models import User
                streams = User.objects.get(username='streams')
                ranked_streams = User.objects.get(username='ranked_streams')

                action.send(dbbook, verb='Rank is updated',
                    action_object=ranked_streams,
                    target=r,
                    comment='new rank is %s\'' % r.rank)

        print "=== Successful updated all ranks"
