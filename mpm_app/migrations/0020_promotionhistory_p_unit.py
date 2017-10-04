# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-03 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mpm_app', '0019_auto_20171003_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionhistory',
            name='p_unit',
            field=models.ForeignKey(default='C99FLU', on_delete=django.db.models.deletion.CASCADE, to='mpm_app.Unit', verbose_name='On-Roll Unit'),
            preserve_default=False,
        ),
    ]