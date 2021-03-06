# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 10:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='addTax',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='Additional Taxes (%)'),
        ),
        migrations.AddField(
            model_name='post',
            name='freeArticles',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='Enter the quantity of free samples'),
        ),
        migrations.AddField(
            model_name='post',
            name='mrp',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='Maximum Retail Price'),
        ),
        migrations.AddField(
            model_name='post',
            name='pack',
            field=models.PositiveSmallIntegerField(default='0', verbose_name='Enter the number of pieces per Pack'),
        ),
        migrations.AddField(
            model_name='post',
            name='vat1',
            field=models.PositiveSmallIntegerField(choices=[('12', '12%'), ('4', '4%')], default='0', verbose_name='Vat (%)'),
        ),
        migrations.AddField(
            model_name='post',
            name='vat2',
            field=models.PositiveSmallIntegerField(choices=[('12', '12%'), ('4', '4%')], default='0', verbose_name='Additional Vat (%)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='batchNo',
            field=models.CharField(max_length=50, verbose_name='Enter the Batch Number'),
        ),
        migrations.AlterField(
            model_name='post',
            name='dateOfPurchase',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date Of Purchase'),
        ),
        migrations.AlterField(
            model_name='post',
            name='expiryDate',
            field=models.DateField(verbose_name='Expiry Date - dd/mm/yyyy format'),
        ),
        migrations.AlterField(
            model_name='post',
            name='medicineName',
            field=models.CharField(max_length=48, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pricePerPiece',
            field=models.PositiveSmallIntegerField(verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='post',
            name='quantity',
            field=models.PositiveSmallIntegerField(verbose_name='Enter the number of Packs'),
        ),
    ]
