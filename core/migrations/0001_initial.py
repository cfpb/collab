# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'App'
        db.create_table('core_app', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf(
                'django.db.models.fields.CharField')(max_length=255)),
            ('stub', self.gf(
                'django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf(
                'django.db.models.fields.CharField')(max_length=255)),
            ('path', self.gf(
                'django.db.models.fields.CharField')(max_length=32)),
            ('icon_file', self.gf('core.thumbs.ImageWithThumbsField')(
                default='app_icons/default.jpg', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['App'])

        # Adding model 'Person'
        db.create_table('core_person', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')
             (to=orm['auth.User'], unique=True)),
            ('stub', self.gf('django.db.models.fields.CharField')
             (max_length=128, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')
             (max_length=128, null=True, blank=True)),
            ('org_group', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.OrgGroup'], null=True, blank=True)),
            ('office_location', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.OfficeLocation'], null=True, blank=True)),
            ('desk_location', self.gf('django.db.models.fields.CharField')
             (max_length=128, null=True, blank=True)),
            ('office_phone', self.gf('django.db.models.fields.CharField')
             (max_length=32, null=True, blank=True)),
            ('mobile_phone', self.gf('django.db.models.fields.CharField')
             (max_length=32, null=True, blank=True)),
            ('home_phone', self.gf('django.db.models.fields.CharField')
             (max_length=32, null=True, blank=True)),
            ('photo_file', self.gf('core.thumbs.ImageWithThumbsField')
             (default='avatars/default.jpg', max_length=100)),
            ('what_i_do', self.gf(
                'django.db.models.fields.TextField')(null=True, blank=True)),
            ('current_projects', self.gf(
                'django.db.models.fields.TextField')(null=True, blank=True)),
            ('stuff_ive_done', self.gf(
                'django.db.models.fields.TextField')(null=True, blank=True)),
            ('things_im_good_at', self.gf(
                'django.db.models.fields.TextField')(null=True, blank=True)),
            ('schools_i_attended', self.gf(
                'django.db.models.fields.TextField')(null=True, blank=True)),
            ('allow_tagging', self.gf(
                'django.db.models.fields.BooleanField')(default=True)),
            ('email_notifications', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Person'])

        # Adding model 'OrgGroup'
        db.create_table('core_orggroup', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf(
                'django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf(
                'django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.OrgGroup'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['OrgGroup'])

        # Adding model 'OfficeLocation'
        db.create_table('core_officelocation', (
            ('id', self.gf('django.db.models.fields.CharField')
             (max_length=12, primary_key=True)),
            ('street', self.gf(
                'django.db.models.fields.CharField')(max_length=56)),
            ('suite', self.gf('django.db.models.fields.CharField')
             (max_length=56, null=True, blank=True)),
            ('city', self.gf(
                'django.db.models.fields.CharField')(max_length=56)),
            ('state', self.gf(
                'django.db.models.fields.CharField')(max_length=2)),
            ('zip', self.gf(
                'django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('core', ['OfficeLocation'])

        # Adding model 'Notification'
        db.create_table('core_notification', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')
             (auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')
             (related_name='+', to=orm['auth.User'])),
            ('uuid', self.gf(
                'django.db.models.fields.CharField')(max_length=255)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')
             (related_name='+', to=orm['auth.User'])),
            ('verb', self.gf(
                'django.db.models.fields.TextField')(max_length=255)),
            ('obj', self.gf('django.db.models.fields.TextField')()),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')
             (related_name='user_notifications', to=orm['auth.User'])),
            ('title', self.gf(
                'django.db.models.fields.TextField')(max_length=255)),
            ('viewed', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'WikiHighlight'
        db.create_table('core_wikihighlight', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf(
                'django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')
             (max_length=2048, blank=True)),
            ('url', self.gf(
                'django.db.models.fields.CharField')(max_length=2048)),
            ('posted_on', self.gf('django.db.models.fields.DateTimeField')
             (auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('core', ['WikiHighlight'])

        # Adding model 'Alert'
        db.create_table('core_alert', (
            ('id', self.gf(
                'django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf(
                'django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf(
                'django.db.models.fields.CharField')(max_length=255)),
            ('is_active', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')
             (auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('core', ['Alert'])

    def backwards(self, orm):
        # Deleting model 'App'
        db.delete_table('core_app')

        # Deleting model 'Person'
        db.delete_table('core_person')

        # Deleting model 'OrgGroup'
        db.delete_table('core_orggroup')

        # Deleting model 'OfficeLocation'
        db.delete_table('core_officelocation')

        # Deleting model 'Notification'
        db.delete_table('core_notification')

        # Deleting model 'WikiHighlight'
        db.delete_table('core_wikihighlight')

        # Deleting model 'Alert'
        db.delete_table('core_alert')

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
        'core.alert': {
            'Meta': {'object_name': 'Alert'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.app': {
            'Meta': {'object_name': 'App'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon_file': ('core.thumbs.ImageWithThumbsField', [], {'default': "'app_icons/default.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'stub': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_notifications'", 'to': "orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'verb': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.officelocation': {
            'Meta': {'object_name': 'OfficeLocation'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'suite': ('django.db.models.fields.CharField', [], {'max_length': '56', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'core.orggroup': {
            'Meta': {'object_name': 'OrgGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.OrgGroup']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'core.person': {
            'Meta': {'object_name': 'Person'},
            'allow_tagging': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_projects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desk_location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'office_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.OfficeLocation']", 'null': 'True', 'blank': 'True'}),
            'office_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'org_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.OrgGroup']", 'null': 'True', 'blank': 'True'}),
            'photo_file': ('core.thumbs.ImageWithThumbsField', [], {'default': "'avatars/default.jpg'", 'max_length': '100'}),
            'schools_i_attended': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'stub': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'stuff_ive_done': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'things_im_good_at': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'what_i_do': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.wikihighlight': {
            'Meta': {'object_name': 'WikiHighlight'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
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

    complete_apps = ['core']
