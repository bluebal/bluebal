# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hammer', '0004_hammeritem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='hammershare',
            name='can_share',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hammershare',
            name='hammer',
            field=models.ForeignKey(related_name='shares', to='hammer.Hammer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hammershare',
            name='sharee',
            field=models.ForeignKey(related_name='shares', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
