# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-07 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0013_auto_20160908_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='patientID',
            field=models.CharField(blank=True, default='NA', max_length=50),
        ),
    ]
