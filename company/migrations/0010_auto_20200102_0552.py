# Generated by Django 2.2.6 on 2020-01-02 05:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20200102_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='abi',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
    ]
