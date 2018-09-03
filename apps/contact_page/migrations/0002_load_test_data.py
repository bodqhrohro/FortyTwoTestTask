from south.v2 import DataMigration
from django.core.management import call_command


class Migration(DataMigration):

    dependencies = [
        ('contact_page', '0001_initial'),
    ]

    def forwards(self, orm):
        call_command("loaddata", "contact_page_test_data.json")

    def backwards(self, orm):
        pass

    complete_apps = ['contact_page']
    symmetrical = False
