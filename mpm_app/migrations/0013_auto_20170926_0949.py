# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-26 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpm_app', '0012_auto_20170925_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='desg',
            name='d_gcode',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='e_join',
            field=models.CharField(choices=[('A_NA', 'NA'), ('A_Land_Losers', 'Appt of Land Losers'), ('A_Fresh_Recruitment', 'Fresh Recruitment'), ('A_Death', 'In lieu of Death'), ('A_Disability', 'In lieu of perm Disability'), ('A_Female_VRS', 'Female VRS'), ('A_Reinstt_Rejoin', 'Reinstt/Rejoin'), ('A_Other_tranfer', 'Other reason(Inter Co transfer)')], default='NA', max_length=20, verbose_name='Service Join Type'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='e_termi',
            field=models.CharField(choices=[('T_NA', 'NA'), ('T_Retirement', 'Retirement'), ('T_Resignation', 'Resignation'), ('T_Unfit', 'Medically Unfit'), ('T_Death', 'Death'), ('T_Female_VRS', 'Female VRS'), ('T_VRS_BPE', 'VRS BPE'), ('T_Dismissal', 'Dismissal/Termination'), ('T_Other_reason', 'Other reason(Inter Co transfer)')], default='NA', max_length=20, verbose_name='Service Termination Type'),
        ),
    ]
