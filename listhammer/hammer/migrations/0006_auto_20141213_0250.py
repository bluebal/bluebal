# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hammer', '0005_auto_20141212_0337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hammershare',
            name='can_delete',
        ),
        migrations.AddField(
            model_name='hammeritem',
            name='creator',
            field=models.ForeignKey(related_name='items', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
