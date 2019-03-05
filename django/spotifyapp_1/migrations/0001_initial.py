# Generated by Django 2.1.7 on 2019-03-05 02:02

import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('spotify_user', models.CharField(max_length=50)),
                ('genres', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
    ]
