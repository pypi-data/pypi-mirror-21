# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-29 18:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': (('phonebook_download', 'Download phonebook via. basic authentication.'),)},
        ),
    ]
