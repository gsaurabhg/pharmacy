# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0002_auto_20160802_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='noOfTablets',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='freeArticles',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='Free tablets'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pack',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='No. of Tablets per Pack'),
        ),
        migrations.AlterField(
            model_name='post',
            name='quantity',
            field=models.PositiveSmallIntegerField(verbose_name='Enter the number of strips'),
        ),
        migrations.AlterField(
            model_name='post',
            name='vat1',
            field=models.PositiveSmallIntegerField(choices=[(12, 12), (4, 4)], default='4', verbose_name='Vat (%)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='vat2',
            field=models.PositiveSmallIntegerField(choices=[(12, 12), (4, 4)], default='4', verbose_name='Additional Vat (%)'),
        ),
    ]
