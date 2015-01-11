# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hammer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, blank=True)),
                ('creator', models.ForeignKey(related_name='hammers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HammerItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'ITEM', max_length=175)),
                ('raw', models.TextField(null=True, blank=True)),
                ('index', models.IntegerField(default=0)),
                ('hammer', models.ForeignKey(related_name='items', to='hammer.Hammer')),
            ],
            options={
                'ordering': ('index',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HammerShare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('can_add', models.BooleanField(default=True)),
                ('can_remove', models.BooleanField(default=True)),
                ('can_change', models.BooleanField(default=True)),
                ('can_delete', models.BooleanField(default=False)),
                ('hammer', models.ForeignKey(to='hammer.Hammer')),
                ('sharee', models.ForeignKey(related_name='hammer_shares', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
