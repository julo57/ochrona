# Generated by Django 5.0.1 on 2024-03-09 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_user_profile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='host',
        ),
        migrations.RemoveField(
            model_name='room',
            name='topic',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='password1',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='password2',
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]