# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hammer',
            name='creator',
            field=models.ForeignKey(related_name='hammers', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
