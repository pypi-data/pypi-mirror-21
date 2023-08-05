# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 11:08
from __future__ import unicode_literals

from django.db import migrations, models


def convert_duration(apps, schema_editor):
    """
    Converts the values of the old duration CharField to new duration
    IntegerField. It uses the temporary field for proper renaming the field
    in the end.
    """
    Item = apps.get_model('agenda', 'Item')
    for item in Item.objects.all():
        duration = item.duration
        item.duration_tmp = None
        if is_int(duration):
            # Assuming that these are minutes.
            item.duration_tmp = int(duration)
        elif isinstance(duration, str):
            # Assuming format (h)h:(m)m. If not, new value is None.
            split = duration.split(':')
            if len(split) == 2 and is_int(split[0]) and is_int(split[1]):
                # Calculate new duration: hours * 60 + minutes.
                item.duration_tmp = int(split[0]) * 60 + int(split[1])
        item.save(skip_autoupdate=True)


def is_int(s):
    """
    Short helper for duration conversion.
    """
    try:
        int(s)
    except (ValueError, TypeError):
        return False
    else:
        return True


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='duration_tmp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(
            convert_duration
        ),
        migrations.RemoveField(
            model_name='item',
            name='duration',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='duration_tmp',
            new_name='duration',
        ),
    ]
