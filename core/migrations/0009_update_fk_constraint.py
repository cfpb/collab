# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models, connection, DatabaseError

def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()


class Migration(SchemaMigration):

    def forwards(self, orm):

        db.alter_column(u'core_person', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.CollabUser'], unique=True))

        # Update tables not normally handled by south
        db.alter_column(u'django_admin_log', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CollabUser']))
        db.alter_column(u'django_comments', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['core.CollabUser']))
        try:
            db.alter_column(u'django_comment_flags', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CollabUser']))
        except DatabaseError:
            pass
        try:
            if db_table_exists(u'reversion_revision'):
                db.alter_column(u'reversion_revision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['core.CollabUser']))
        except DatabaseError:
            pass

    def backwards(self, orm):

        db.alter_column(u'core_person', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True))

        # Update tables not normally handled by south
        db.alter_column(u'django_admin_log', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        db.alter_column(u'django_comments', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))
        try:
            db.alter_column(u'django_comment_flags', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        except DatabaseError:
            pass
        try:
            if db_table_exists(u'reversion_revision'):
                db.alter_column(u'reversion_revision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))
        except DatabaseError:
            pass

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.alert': {
            'Meta': {'object_name': 'Alert'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.app': {
            'Meta': {'object_name': 'App'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon_file': ('core.thumbs.ImageWithThumbsField', [], {'default': "'app_icons/default.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'stub': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.collabuser': {
            'Meta': {'object_name': 'CollabUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        u'core.officelocation': {
            'Meta': {'object_name': 'OfficeLocation'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'suite': ('django.db.models.fields.CharField', [], {'max_length': '56', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'core.orggroup': {
            'Meta': {'object_name': 'OrgGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.OrgGroup']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'allow_tagging': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_projects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desk_location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'office_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.OfficeLocation']", 'null': 'True', 'blank': 'True'}),
            'office_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'org_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.OrgGroup']", 'null': 'True', 'blank': 'True'}),
            'photo_file': ('core.thumbs.ImageWithThumbsField', [], {'default': "'avatars/default.jpg'", 'max_length': '100'}),
            'schools_i_attended': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'stub': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'stuff_ive_done': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'things_im_good_at': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.CollabUser']", 'unique': 'True'}),
            'what_i_do': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.tagcategory': {
            'Meta': {'object_name': 'TagCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            'create_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"}),
            'tag_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taggit.TagCategory']", 'null': 'True'}),
            'tag_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_related'", 'null': 'True', 'to': u"orm['core.CollabUser']"})
        }
    }

    complete_apps = ['core']
