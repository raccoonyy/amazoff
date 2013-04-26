# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Book.rank'
        db.delete_column(u'publication_book', 'rank')

        # Deleting field 'Book.rate'
        db.delete_column(u'publication_book', 'rate')

        # Deleting field 'Book.pages'
        db.delete_column(u'publication_book', 'pages')


    def backwards(self, orm):
        # Adding field 'Book.rank'
        db.add_column(u'publication_book', 'rank',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)

        # Adding field 'Book.rate'
        db.add_column(u'publication_book', 'rate',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)

        # Adding field 'Book.pages'
        db.add_column(u'publication_book', 'pages',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)


    models = {
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['publication']