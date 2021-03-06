# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacyapp', '0005_auto_20160806_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billNo', models.CharField(max_length=50)),
                ('billDate', models.DateField(default=django.utils.timezone.now, verbose_name='Date Of Purchase')),
                ('noOfTabletsOrdered', models.PositiveSmallIntegerField(default='0')),
                ('pricePerTablet', models.DecimalField(decimal_places=2, default='0', max_digits=5)),
                ('totalPrice', models.PositiveSmallIntegerField(default='0')),
                ('medicineName', models.ManyToManyField(to='pharmacyapp.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PatientDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.CharField(max_length=50, verbose_name='Enter the Patient ID')),
                ('patientName', models.CharField(max_length=50, verbose_name='Patient Name')),
                ('patientPhoneNo', models.PositiveSmallIntegerField(verbose_name='Phone Number')),
                ('patientDateOfBirth', models.DateField(default=django.utils.timezone.now, verbose_name='Date Of Birth')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='patientID',
            field=models.ManyToManyField(to='pharmacyapp.PatientDetails'),
        ),
    ]
