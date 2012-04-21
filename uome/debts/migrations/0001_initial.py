# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('debts_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('debts', ['Person'])

        # Adding model 'UserProxy'
        db.create_table('debts_userproxy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auth_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proxies', to=orm['auth.User'])),
            ('virtual_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proxies', null=True, to=orm['debts.Person'])),
        ))
        db.send_create_signal('debts', ['UserProxy'])

        # Adding unique constraint on 'UserProxy', fields ['auth_user', 'virtual_user']
        db.create_unique('debts_userproxy', ['auth_user_id', 'virtual_user_id'])

        # Adding model 'MoneyDebt'
        db.create_table('debts_moneydebt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owes_moneydebt', to=orm['debts.UserProxy'])),
            ('owed_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owed_moneydebt', to=orm['debts.UserProxy'])),
            ('given_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('expected_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('returned_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('motive', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('debts', ['MoneyDebt'])

        # Adding model 'ObjectDebt'
        db.create_table('debts_objectdebt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owes_objectdebt', to=orm['debts.UserProxy'])),
            ('owed_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owed_objectdebt', to=orm['debts.UserProxy'])),
            ('given_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('expected_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('returned_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('what', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('debts', ['ObjectDebt'])

    def backwards(self, orm):
        # Removing unique constraint on 'UserProxy', fields ['auth_user', 'virtual_user']
        db.delete_unique('debts_userproxy', ['auth_user_id', 'virtual_user_id'])

        # Deleting model 'Person'
        db.delete_table('debts_person')

        # Deleting model 'UserProxy'
        db.delete_table('debts_userproxy')

        # Deleting model 'MoneyDebt'
        db.delete_table('debts_moneydebt')

        # Deleting model 'ObjectDebt'
        db.delete_table('debts_objectdebt')

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
        'debts.moneydebt': {
            'Meta': {'object_name': 'MoneyDebt'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'expected_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'given_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motive': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owes_moneydebt'", 'to': "orm['debts.UserProxy']"}),
            'owed_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owed_moneydebt'", 'to': "orm['debts.UserProxy']"}),
            'returned_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'debts.objectdebt': {
            'Meta': {'object_name': 'ObjectDebt'},
            'expected_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'given_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owes_objectdebt'", 'to': "orm['debts.UserProxy']"}),
            'owed_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owed_objectdebt'", 'to': "orm['debts.UserProxy']"}),
            'returned_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'what': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'debts.person': {
            'Meta': {'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'debts.userproxy': {
            'Meta': {'unique_together': "(('auth_user', 'virtual_user'),)", 'object_name': 'UserProxy'},
            'auth_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proxies'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'virtual_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proxies'", 'null': 'True', 'to': "orm['debts.Person']"})
        }
    }

    complete_apps = ['debts']