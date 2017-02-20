# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Issuer', '0002_auto_20170219_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='transaction_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Issuer.Transaction'),
        ),
    ]