# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentpoll',
            name='yesnoabstain',
        ),
        migrations.AddField(
            model_name='assignmentpoll',
            name='pollmethod',
            field=models.CharField(default='yna', max_length=5),
        ),
    ]
