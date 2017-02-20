# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Issuer', '0003_auto_20170219_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='transaction_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_trans', to='Issuer.Transaction'),
        ),
    ]