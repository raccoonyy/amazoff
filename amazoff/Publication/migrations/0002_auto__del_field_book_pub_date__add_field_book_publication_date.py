# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Book.pub_date'
        db.delete_column(u'publication_book', 'pub_date')

        # Adding field 'Book.publication_date'
        db.add_column(u'publication_book', 'publication_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Book.pub_date'
        db.add_column(u'publication_book', 'pub_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Deleting field 'Book.publication_date'
        db.delete_column(u'publication_book', 'publication_date')


    models = {
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'rate': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['publication']