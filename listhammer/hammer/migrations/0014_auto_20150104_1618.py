# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0013_auto_20141230_0421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hammerdata',
            name='h',
        ),
        migrations.RemoveField(
            model_name='hammerdata',
            name='w',
        ),
        migrations.RemoveField(
            model_name='hammerdata',
            name='x',
        ),
        migrations.RemoveField(
            model_name='hammerdata',
            name='y',
        ),
        migrations.RemoveField(
            model_name='hammerdata',
            name='z',
        ),
    ]
