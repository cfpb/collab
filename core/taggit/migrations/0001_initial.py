# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('taggit_tag', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf(
                'django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')
             (unique=True, max_length=100)),
        ))
        db.send_create_signal('taggit', ['Tag'])

        # Adding model 'TagCategory'
        db.create_table('taggit_tagcategory', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')
             (unique=True, max_length=255)),
        ))
        db.send_create_signal('taggit', ['TagCategory'])

        # Adding model 'TaggedItem'
        db.create_table('taggit_taggeditem', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='taggit_taggeditem_items', to=orm['taggit.Tag'])),
            ('object_id', self.gf(
                'django.db.models.fields.IntegerField')(db_index=True)),
            ('tag_creator', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='taggit_taggeditem_related', null=True, to=orm['auth.User'])),
            ('create_timestamp', self.gf(
                'django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('tag_category', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['taggit.TagCategory'], null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='taggit_taggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('taggit', ['TaggedItem'])

    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('taggit_tag')

        # Deleting model 'TagCategory'
        db.delete_table('taggit_tagcategory')

        # Deleting model 'TaggedItem'
        db.delete_table('taggit_taggeditem')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.tagcategory': {
            'Meta': {'object_name': 'TagCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'create_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"}),
            'tag_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taggit.TagCategory']", 'null': 'True'}),
            'tag_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_related'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['taggit']
