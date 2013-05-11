# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'publication_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('br_id', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True)),
        ))
        db.send_create_signal('publication', ['Category'])

        # Adding model 'Author'
        db.create_table(u'publication_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('publication', ['Author'])

        # Adding model 'Publisher'
        db.create_table(u'publication_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('publication', ['Publisher'])

        # Adding model 'Book'
        db.create_table(u'publication_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True)),
            ('img', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=13)),
            ('mod_date', self.gf('django.db.models.fields.DateField')(auto_now=True, null=True, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('publication_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('publication', ['Book'])

        # Adding M2M table for field author on 'Book'
        db.create_table(u'publication_book_author', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['publication.book'], null=False)),
            ('author', models.ForeignKey(orm['publication.author'], null=False))
        ))
        db.create_unique(u'publication_book_author', ['book_id', 'author_id'])

        # Adding M2M table for field category on 'Book'
        db.create_table(u'publication_book_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['publication.book'], null=False)),
            ('category', models.ForeignKey(orm['publication.category'], null=False))
        ))
        db.create_unique(u'publication_book_category', ['book_id', 'category_id'])

        # Adding M2M table for field publisher on 'Book'
        db.create_table(u'publication_book_publisher', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['publication.book'], null=False)),
            ('publisher', models.ForeignKey(orm['publication.publisher'], null=False))
        ))
        db.create_unique(u'publication_book_publisher', ['book_id', 'publisher_id'])

        # Adding model 'Rank'
        db.create_table(u'publication_rank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publication.Book'], null=True)),
        ))
        db.send_create_signal('publication', ['Rank'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'publication_category')

        # Deleting model 'Author'
        db.delete_table(u'publication_author')

        # Deleting model 'Publisher'
        db.delete_table(u'publication_publisher')

        # Deleting model 'Book'
        db.delete_table(u'publication_book')

        # Removing M2M table for field author on 'Book'
        db.delete_table('publication_book_author')

        # Removing M2M table for field category on 'Book'
        db.delete_table('publication_book_category')

        # Removing M2M table for field publisher on 'Book'
        db.delete_table('publication_book_publisher')

        # Deleting model 'Rank'
        db.delete_table(u'publication_rank')


    models = {
        u'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'publication.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['publication.Author']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['publication.Category']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['publication.Publisher']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'publication.category': {
            'Meta': {'object_name': 'Category'},
            'br_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'})
        },
        'publication.publisher': {
            'Meta': {'object_name': 'Publisher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'publication.rank': {
            'Meta': {'object_name': 'Rank'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publication.Book']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['publication']