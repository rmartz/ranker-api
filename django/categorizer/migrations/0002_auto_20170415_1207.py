# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-15 12:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categorizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contests', to='categorizer.Topic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='topicoption',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicoption', to='categorizer.Option'),
        ),
        migrations.AlterField(
            model_name='topicoption',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicoption', to='categorizer.Topic'),
        ),
    ]
