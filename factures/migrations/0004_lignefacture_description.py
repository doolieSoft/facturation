# Generated by Django 5.2.3 on 2025-06-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factures', '0003_facture_pdf_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignefacture',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
