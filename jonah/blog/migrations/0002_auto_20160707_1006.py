# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
