# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpm_app', '0003_auto_20170911_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desg',
            name='d_promo',
            field=models.CharField(max_length=2, null=True),
        ),
    ]