# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SearchableTool'
        db.create_table('search_searchabletool', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (unique=True, max_length=255)),
            ('link', self.gf(
                'django.db.models.fields.CharField')(max_length=2048)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')
             (auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('search', ['SearchableTool'])

    def backwards(self, orm):
        # Deleting model 'SearchableTool'
        db.delete_table('search_searchabletool')

    models = {
        'core.search.searchabletool': {
            'Meta': {'object_name': 'SearchableTool'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['search']
