# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Friend'
        db.create_table('debts_friend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('friend_of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friends', to=orm['accounts.Account'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('debts', ['Friend'])

        # Adding unique constraint on 'Friend', fields ['friend_of', 'nickname']
        db.create_unique('debts_friend', ['friend_of_id', 'nickname'])

        # Adding model 'Debt'
        db.create_table('debts_debt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='debt', to=orm['accounts.Account'])),
            ('friend', self.gf('django.db.models.fields.related.ForeignKey')(related_name='debt', to=orm['debts.Friend'])),
            ('direction', self.gf('django.db.models.fields.CharField')(default='FRIEND_OWES_USER', max_length=20)),
            ('motive', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('given_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('expected_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('returned_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('debts', ['Debt'])

    def backwards(self, orm):
        # Removing unique constraint on 'Friend', fields ['friend_of', 'nickname']
        db.delete_unique('debts_friend', ['friend_of_id', 'nickname'])

        # Deleting model 'Friend'
        db.delete_table('debts_friend')

        # Deleting model 'Debt'
        db.delete_table('debts_debt')

    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'account'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
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
        'debts.debt': {
            'Meta': {'object_name': 'Debt'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'debt'", 'to': "orm['accounts.Account']"}),
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'default': "'FRIEND_OWES_USER'", 'max_length': '20'}),
            'expected_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'debt'", 'to': "orm['debts.Friend']"}),
            'given_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motive': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'returned_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'debts.friend': {
            'Meta': {'unique_together': "(('friend_of', 'nickname'),)", 'object_name': 'Friend'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'friend_of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['accounts.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['debts']