# Generated by Django 1.10.4 on 2016-12-17 10:58
from __future__ import unicode_literals

from django.db import migrations


def remove_session_content_type(apps, schema_editor):
    """
    Remove session content_type because we want to delete the session model in
    the next step.
    """
    # We get the model from the versioned app registry;
    # if we directly import it, it will be the wrong version.
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Session = apps.get_model('core', 'Session')
    ContentType.objects.get_for_model(Session).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_misc_features'),
    ]

    operations = [
        migrations.RunPython(
            remove_session_content_type
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
