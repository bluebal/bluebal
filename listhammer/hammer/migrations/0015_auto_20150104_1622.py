# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hammer', '0014_auto_20150104_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='HammerDataDefault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('theme', models.CharField(default=b'default', max_length=50)),
                ('numbered', models.BooleanField(default=True)),
                ('user', models.ForeignKey(related_name='default_data', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hammerdata',
            name='numbered',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
