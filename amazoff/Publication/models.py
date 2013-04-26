from amazon.api import AmazonAPI
from django.db import models
from django.db.models.signals import post_save
from actstream import action


class Category(models.Model):
    name = models.CharField(max_length=150, null=True)
    br_id = models.CharField(max_length=20, null=True, unique=True)

    class Meta:
        app_label = 'publication'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return '%s' % (self.name)


class Author(models.Model):
    name = models.CharField(max_length=50, null=False)

    class Meta:
        app_label = 'publication'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50, null=False)

    class Meta:
        app_label = 'publication'
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __unicode__(self):
        return self.name


class BookManager(models.Manager):
    def create_book(self, ambook):
        print "\t\'%s\' will creating." % ambook.title[:30]

        book = self.trans_amazon_to_book(ambook)

        authors = book['author']
        publisher = book['publisher']
        del book['author']
        del book['publisher']

        dbbook = self.create(**book)
        dbbook.author_add(authors)
        dbbook.publisher_add(publisher)
        dbbook.categorising(ambook)

        action.send(Book, verb='%s is creating' % dbbook.title)

    def trans_amazon_to_book(self, amazon_book):
        book = {}
        book['author'] = amazon_book.author
        book['img'] = amazon_book.medium_image_url
        book['isbn'] = amazon_book.isbn
        book['pages'] = str(amazon_book.pages)
        book['publication_date'] = amazon_book.publication_date
        book['publisher'] = amazon_book.publisher
        book['title'] = amazon_book.title
        return book


class Book(models.Model):
    author = models.ManyToManyField(Author)
    category = models.ManyToManyField(Category)
    create_date = models.DateField(null=True, auto_now_add=True)
    img = models.URLField(max_length=200, null=True)
    isbn = models.CharField(max_length=13, null=False, unique=True)
    mod_date = models.DateField(null=True, auto_now_add=True)
    pages = models.CharField(max_length=4, null=True)
    publication_date = models.DateField(null=True)
    publisher = models.ManyToManyField(Publisher)
    title = models.CharField(max_length=255, null=True)
    objects = BookManager()

    class Meta:
        app_label = 'publication'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def author_add(self, authors):
        for author in self.author.all():
            author.delete()

        for name in authors:
            author, created = Author.objects.get_or_create(
                name=name
            )
            self.author.add(author)

    def publisher_add(self, name):
        pub, created = Publisher.objects.get_or_create(
            name=name
        )
        self.publisher.add(pub)

    def categorising(self, ambook):
        print "\t\'%s\' is catogorizing." % self.title[:30]
        for br in ambook.browse_nodes:
            cat, created = Category.objects.get_or_create(
                name=br.name,
                br_id=str(br.id),
            )
            self.category.add(cat)

    def update(self, amazon_book):
        diff = self.diff_with_amazon_book(amazon_book)
        book = Book.objects.trans_amazon_to_book(amazon_book)
        if diff:
            pass
        else:
            return

        for d in diff:
            if d == 'author':
                self.author_add(book['author'])
                continue
            if d == 'publisher':
                self.publisher_add(book['publisher'])
                continue

            action.send(Book, verb='%s of %s is updated \'%s => %s\'' % (d, self.title, getattr(self, d), book[d]))
            setattr(self, d, book[d])
        print "  = %s \'%s\' is updated." % (self.isbn, diff)
        self.save()

    def diff_with_amazon_book(self, amazon_book):
        book = Book.objects.trans_amazon_to_book(amazon_book)
        diff = []
        names = [author.name for author in self.author.all()]
        if self.publisher.exists():
            publisher = [publisher.name for publisher in self.publisher.all()][0]
        else:
            publisher = ''

        if len(publisher) == 1:
            publisher = publisher[0]
        if set(names) != set(book['author']):
            diff.append('author')
        if self.img != book['img']:
            diff.append('img')
        if self.pages != book['pages']:
            diff.append('pages')
        if self.publication_date != book['publication_date']:
            diff.append('publication_date')
        if self.title != book['title']:
            diff.append('title')
        if publisher != book['publisher']:
            diff.append('publisher')
        if len(diff) > 0:
            return diff
        else:
            return False

    def __unicode__(self):
        return '%s' % self.title[:30]


class Rank(models.Model):
    rank = models.CharField(max_length=15, null=False)
    date = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book, null=True)

    class Meta:
        app_label = 'publication'
        unique_together = ('date', 'book')
        verbose_name = 'Rank'
        verbose_name_plural = 'Ranks'

    def __unicode__(self):
        return '%s (%s)' % (str(self.rank), self.date)
