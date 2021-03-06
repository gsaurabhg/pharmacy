# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 13:15
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0034_auto_20161019_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='vat1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='vat2',
        ),
        migrations.AddField(
            model_name='post',
            name='sat',
            field=models.PositiveSmallIntegerField(choices=[(0, 0), (4, 4), (5, 5), (12, 12)], default='0', verbose_name='Additional Vat (%)'),
        ),
        migrations.AddField(
            model_name='post',
            name='vat',
            field=models.PositiveSmallIntegerField(choices=[(0, 0), (4, 4), (5, 5), (12, 12)], default='4', verbose_name='Vat (%)'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='discountedPrice',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='pricePerTablet',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='returnDiscountedPrice',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='post',
            name='mrp',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='post',
            name='netPurchasePrice',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='post',
            name='pack',
            field=models.PositiveSmallIntegerField(default='1', verbose_name='No. of Tablets per Strip/Bottles'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pricePerStrip',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='post',
            name='pricePerTablet',
            field=models.DecimalField(decimal_places=2, default='0.01', max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='returnbill',
            name='originalPricePerTablet',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='returnbill',
            name='returnSalesDiscountedPricePerTablet',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='returnbill',
            name='totalReturnAmount',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
