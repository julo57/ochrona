# Generated by Django 5.0.1 on 2024-03-12 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('manager', 'Manager'), ('employee', 'Pracownik'), ('guest', 'Gość')], default='guest', max_length=20),
        ),
    ]
