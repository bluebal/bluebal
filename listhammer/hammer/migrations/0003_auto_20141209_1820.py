# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0002_auto_20141209_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hammeritem',
            name='title',
            field=models.CharField(default=b'ITEM', max_length=100),
            preserve_default=True,
        ),
    ]
