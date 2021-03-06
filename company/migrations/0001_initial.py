# Generated by Django 2.2.6 on 2019-12-30 02:58

from django.conf import settings
import django.contrib.auth.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_customuser_wallet_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('users.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=50), size=None)),
                ('minBounty', models.FloatField()),
                ('maxBounty', models.FloatField()),
                ('notice', models.CharField(max_length=250, null=True)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
            ],
        ),
    ]
