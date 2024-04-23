# Generated by Django 5.0.4 on 2024-04-23 03:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_alter_publickey_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='financedocument',
            name='public_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.publickey'),
        ),
        migrations.AddField(
            model_name='hrdocument',
            name='public_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.publickey'),
        ),
        migrations.AddField(
            model_name='itdocument',
            name='public_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.publickey'),
        ),
        migrations.AddField(
            model_name='logisticsdocument',
            name='public_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.publickey'),
        ),
        migrations.AddField(
            model_name='salesdocument',
            name='public_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.publickey'),
        ),
    ]