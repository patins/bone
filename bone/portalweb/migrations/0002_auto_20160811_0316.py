# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 03:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portalweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tinder',
            options={'permissions': (('view_all', 'Can view all Tinders and bulk output'),)},
        ),
    ]