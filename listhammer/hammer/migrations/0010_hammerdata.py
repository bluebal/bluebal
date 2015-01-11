# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hammer', '0009_auto_20141223_0322'),
    ]

    operations = [
        migrations.CreateModel(
            name='HammerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('h', models.IntegerField(default=300)),
                ('w', models.IntegerField(default=225)),
                ('x', models.IntegerField(default=1)),
                ('y', models.IntegerField(default=1)),
                ('z', models.IntegerField(default=0)),
                ('theme', models.CharField(default=b'default', max_length=50)),
                ('hammer', models.ForeignKey(related_name='data', to='hammer.Hammer')),
                ('user', models.ForeignKey(related_name='data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
