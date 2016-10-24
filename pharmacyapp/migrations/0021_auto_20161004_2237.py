# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0020_auto_20160930_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='pricePerPiece',
        ),
        migrations.AddField(
            model_name='post',
            name='netPurchasePrice',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='pricePerStrip',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientdetail',
            name='patientPhoneNo',
            field=models.PositiveSmallIntegerField(blank=True, default='0', verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='post',
            name='mrp',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='quantity',
            field=models.PositiveSmallIntegerField(verbose_name='Enter the number of strips Purchased'),
        ),
    ]