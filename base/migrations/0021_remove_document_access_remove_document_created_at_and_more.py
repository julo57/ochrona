# Generated by Django 5.0.3 on 2024-04-07 01:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_document_access_document_folder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='access',
        ),
        migrations.RemoveField(
            model_name='document',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='document',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='document',
            name='updated_at',
        ),
    ]
