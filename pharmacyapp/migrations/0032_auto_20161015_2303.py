# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0031_auto_20161006_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='returnSalesBillDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date Of Return'),
        ),
        migrations.AddField(
            model_name='bill',
            name='returnSalesNoOfTablets',
            field=models.PositiveSmallIntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='post',
            name='netPurchasePrice',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='returnbill',
            name='returnSalesBillDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date Of Return'),
        ),
    ]