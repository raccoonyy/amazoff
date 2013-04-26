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
            ('br_id', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True)),
        ))
        db.send_create_signal(u'publication', ['Category'])

        # Adding model 'Rank'
        db.create_table(u'publication_rank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'publication', ['Rank'])

        # Adding field 'Book.img'
        db.add_column(u'publication_book', 'img',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Book.pages'
        db.add_column(u'publication_book', 'pages',
                      self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True),
                      keep_default=False)

        # Adding field 'Book.rank'
        db.add_column(u'publication_book', 'rank',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publication.Rank'], null=True),
                      keep_default=False)

        # Adding M2M table for field category on 'Book'
        db.create_table(u'publication_book_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['publication.book'], null=False)),
            ('category', models.ForeignKey(orm[u'publication.category'], null=False))
        ))
        db.create_unique(u'publication_book_category', ['book_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'publication_category')

        # Deleting model 'Rank'
        db.delete_table(u'publication_rank')

        # Deleting field 'Book.img'
        db.delete_column(u'publication_book', 'img')

        # Deleting field 'Book.pages'
        db.delete_column(u'publication_book', 'pages')

        # Deleting field 'Book.rank'
        db.delete_column(u'publication_book', 'rank_id')

        # Removing M2M table for field category on 'Book'
        db.delete_table('publication_book_category')


    models = {
        'publication.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['publication.Category']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['publication.Rank']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'publication.category': {
            'Meta': {'object_name': 'Category'},
            'br_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'})
        },
        u'publication.rank': {
            'Meta': {'object_name': 'Rank'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['publication']