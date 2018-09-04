from south.v2 import DataMigration
from django.core.management import call_command


class Migration(DataMigration):

    def forwards(self, orm):
        call_command("collectstatic", interactive=False)

    def backwards(self, orm):
        pass

    symmetrical = False
