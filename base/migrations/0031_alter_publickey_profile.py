# Generated by Django 5.0.4 on 2024-04-23 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_remove_publickey_user_publickey_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publickey',
            name='profile',
            field=models.ForeignKey(default='Janek', on_delete=django.db.models.deletion.CASCADE, related_name='public_keys', to='base.profile'),
        ),
    ]
