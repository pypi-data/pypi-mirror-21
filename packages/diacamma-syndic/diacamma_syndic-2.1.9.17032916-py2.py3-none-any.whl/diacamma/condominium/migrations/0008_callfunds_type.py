# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-22 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominium', '0007_callfunds_supporting'),
    ]

    operations = [
        migrations.AddField(
            model_name='callfunds',
            name='type_call',
            field=models.IntegerField(choices=[(0, 'current'), (1, 'exceptional'), (2, 'cash advance')],
                                      db_index=True, default=0, verbose_name='type of call'),
        ),
    ]
