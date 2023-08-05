# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-23 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('djadmin', '0002_auto_20170128_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sortable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_array', models.TextField(verbose_name='Model Sortable Array')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Sortable Model',
                'verbose_name_plural': 'Sortable Models',
            },
        ),
        migrations.AddField(
            model_name='djadminmodelsetting',
            name='actions_on_bottom',
            field=models.BooleanField(default=False, verbose_name='Actions on Bottom'),
        ),
        migrations.AddField(
            model_name='djadminmodelsetting',
            name='actions_on_top',
            field=models.BooleanField(default=True, help_text='Controls where on the page the actions bar appears', verbose_name='Actions on Top'),
        ),
        migrations.AddField(
            model_name='djadminmodelsetting',
            name='has_add_permission',
            field=models.BooleanField(default=True, verbose_name='Has Add Permission?'),
        ),
        migrations.AddField(
            model_name='djadminmodelsetting',
            name='has_change_permission',
            field=models.BooleanField(default=True, verbose_name='Has Change Permission?'),
        ),
        migrations.AddField(
            model_name='djadminmodelsetting',
            name='has_delete_permission',
            field=models.BooleanField(default=True, verbose_name='Has Delete Permission?'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sessions.Session', verbose_name='Session'),
        ),
    ]
