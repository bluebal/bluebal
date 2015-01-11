# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0003_auto_20141209_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='hammeritem',
            name='status',
            field=models.CharField(default=b'idle', max_length=100),
            preserve_default=True,
        ),
    ]
