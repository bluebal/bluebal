# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0012_userpreference_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='date_format',
            field=models.CharField(default=b'%B %d, %Y', max_length=40),
            preserve_default=True,
        ),
    ]
