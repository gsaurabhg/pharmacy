# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0028_auto_20161004_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='netPurchasePrice',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=5),
        ),
    ]
