# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Rank', fields ['date', 'book']
        db.create_unique(u'publication_rank', ['date', 'book_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Rank', fields ['date', 'book']
        db.delete_unique(u'publication_rank', ['date', 'book_id'])


    models = {
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['publication.Category']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'publication.category': {
            'Meta': {'object_name': 'Category'},
            'br_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'})
        },
        'publication.rank': {
            'Meta': {'unique_together': "(('date', 'book'),)", 'object_name': 'Rank'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publication.Book']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['publication']