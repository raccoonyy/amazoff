# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Book.pages'
        db.alter_column(u'publication_book', 'pages', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

    def backwards(self, orm):

        # Changing field 'Book.pages'
        db.alter_column(u'publication_book', 'pages', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True))

    models = {
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['publication.Category']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'unique': 'True', 'null': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['publication.Rank']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'publication.category': {
            'Meta': {'object_name': 'Category'},
            'br_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'})
        },
        u'publication.rank': {
            'Meta': {'object_name': 'Rank'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'unique': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['publication']