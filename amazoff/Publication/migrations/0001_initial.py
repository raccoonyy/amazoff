# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table(u'publication_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=13, null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True)),
            ('mod_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('rate', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('publication', ['Book'])


    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table(u'publication_book')


    models = {
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'rate': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['publication']