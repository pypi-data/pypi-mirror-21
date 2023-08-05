# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 01:23
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import openslides.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_number', models.CharField(blank=True, max_length=255)),
                ('comment', models.TextField(blank=True, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('type', models.IntegerField(choices=[(1, 'Agenda item'), (2, 'Hidden item')], default=2)),
                ('duration', models.CharField(blank=True, max_length=5, null=True)),
                ('weight', models.IntegerField(default=10000)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('speaker_list_closed', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('parent', models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='agenda.Item')),
            ],
            options={
                'permissions': (
                    ('can_see', 'Can see agenda'),
                    ('can_manage', 'Can manage agenda'),
                    ('can_see_hidden_items', 'Can see hidden items and time scheduling of agenda')),
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='agenda.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_be_speaker', 'Can put oneself on the list of speakers'),),
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
