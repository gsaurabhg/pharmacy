# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-24 13:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0015_auto_20160908_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdetail',
            name='patientDateOfBirth',
        ),
        migrations.AlterField(
            model_name='patientdetail',
            name='patientID',
            field=models.CharField(blank=True, max_length=50, verbose_name='Patient ID'),
        ),
        migrations.AlterField(
            model_name='patientdetail',
            name='patientName',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='post',
            name='dateOfPurchase',
            field=models.DateField(default=datetime.datetime(2016, 9, 24, 13, 43, 1, 815366, tzinfo=utc), verbose_name='Date Of Purchase'),
        ),
        migrations.AlterField(
            model_name='post',
            name='expiryDate',
            field=models.DateField(verbose_name='Expiry Date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='freeArticles',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='Free Strips'),
        ),
        migrations.AlterField(
            model_name='post',
            name='vat1',
            field=models.PositiveSmallIntegerField(choices=[(0, 0), (4, 4), (12, 12)], default='4', verbose_name='Vat (%)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='vat2',
            field=models.PositiveSmallIntegerField(choices=[(0, 0), (4, 4), (12, 12)], default='0', verbose_name='Additional Vat (%)'),
        ),
    ]