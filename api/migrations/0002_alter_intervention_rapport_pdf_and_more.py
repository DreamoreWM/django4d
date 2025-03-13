# Generated by Django 5.1.6 on 2025-03-13 16:37

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervention',
            name='rapport_pdf',
            field=models.FileField(blank=True, null=True, upload_to=api.models.rapport_pdf_upload_to),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.signature_upload_to),
        ),
    ]
