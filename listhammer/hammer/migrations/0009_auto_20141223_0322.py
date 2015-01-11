# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0008_auto_20141222_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='hammer',
            name='cxr',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hammer',
            name='theme',
            field=models.CharField(default=b'default', max_length=25),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hammershare',
            name='theme',
            field=models.CharField(default=b'default', max_length=25),
            preserve_default=True,
        ),
    ]
