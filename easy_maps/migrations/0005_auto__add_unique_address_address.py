# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Removing index on 'Address', fields ['address']
        if db.backend_name != 'sqlite3':
            # South forgets indexes when altering tables in sqlite,
            # see http://south.aeracode.org/ticket/757 .
            # This means delete_index will raise an exception with sqlite
            # because the index is 'forgotten' in previous migrations.
            db.delete_index('easy_maps_address', ['address'])

        # Adding unique constraint on 'Address', fields ['address']
        db.create_unique('easy_maps_address', ['address'])


    def backwards(self, orm):
        # Removing unique constraint on 'Address', fields ['address']
        db.delete_unique('easy_maps_address', ['address'])

        # Adding index on 'Address', fields ['address']
        db.create_index('easy_maps_address', ['address'])


    models = {
        'easy_maps.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'computed_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geocode_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['easy_maps']
