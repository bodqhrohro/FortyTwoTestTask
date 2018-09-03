# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeneralInfo'
        db.create_table('contact_page_generalinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=65536)),
        ))
        db.send_create_signal('contact_page', ['GeneralInfo'])

        # Adding model 'Contact'
        db.create_table('contact_page_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('contact_page', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'GeneralInfo'
        db.delete_table('contact_page_generalinfo')

        # Deleting model 'Contact'
        db.delete_table('contact_page_contact')


    models = {
        'contact_page.contact': {
            'Meta': {'object_name': 'Contact'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'contact_page.generalinfo': {
            'Meta': {'object_name': 'GeneralInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '65536'})
        }
    }

    complete_apps = ['contact_page']