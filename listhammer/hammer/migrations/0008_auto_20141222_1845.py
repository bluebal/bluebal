# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0007_auto_20141222_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hammercheckin',
            name='checkin',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
