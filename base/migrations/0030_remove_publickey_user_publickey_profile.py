# Generated by Django 5.0.4 on 2024-04-23 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_publickey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publickey',
            name='user',
        ),
        migrations.AddField(
            model_name='publickey',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='public_keys', to='base.profile'),
        ),
    ]
