# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 05:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartTrack',
        ),
        migrations.DeleteModel(
            name='Top100Track',
        ),
    ]