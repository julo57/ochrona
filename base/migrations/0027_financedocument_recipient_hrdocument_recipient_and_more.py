# Generated by Django 5.0.4 on 2024-04-22 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_alter_profile_department_financedocument_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financedocument',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_documents_FINANCE', to='base.profile'),
        ),
        migrations.AddField(
            model_name='hrdocument',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_documents_HR', to='base.profile'),
        ),
        migrations.AddField(
            model_name='itdocument',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_documents_IT', to='base.profile'),
        ),
        migrations.AddField(
            model_name='logisticsdocument',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_documents_LOGISTIC', to='base.profile'),
        ),
        migrations.AddField(
            model_name='salesdocument',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_documents_SALES', to='base.profile'),
        ),
    ]
