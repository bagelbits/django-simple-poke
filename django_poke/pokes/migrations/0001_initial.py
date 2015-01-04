# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poke',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poke_date', models.DateTimeField(verbose_name=b'date poked')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='poke',
            name='receive_user',
            field=models.ForeignKey(related_name='pokee', to='pokes.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poke',
            name='send_user',
            field=models.ForeignKey(related_name='poker', to='pokes.User'),
            preserve_default=True,
        ),
    ]
