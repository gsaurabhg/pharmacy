# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0027_post_netpurchaseprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mrp',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='netPurchasePrice',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='pricePerStrip',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
