# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SuggestedSearchResult'
        db.create_table(u'search_suggestedsearchresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_term', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('suggested_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'search', ['SuggestedSearchResult'])


    def backwards(self, orm):
        # Deleting model 'SuggestedSearchResult'
        db.delete_table(u'search_suggestedsearchresult')


    models = {
        u'search.searchabletool': {
            'Meta': {'object_name': 'SearchableTool'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'search.suggestedsearchresult': {
            'Meta': {'object_name': 'SuggestedSearchResult'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suggested_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['search']
