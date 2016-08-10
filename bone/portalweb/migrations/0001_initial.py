# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boneweb', '0007_resident_alumni'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tinder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.CharField(blank=True, max_length=20)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('bio', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('resident', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='boneweb.Resident')),
            ],
        ),
    ]