# Generated by Django 5.2.3 on 2025-06-29 13:06

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('factures', '0005_auto_20250629_0921'),
        ('prestations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('validite_jours', models.PositiveIntegerField(default=90)),
                ('remarques', models.TextField(blank=True)),
                ('fichier_pdf', models.FileField(blank=True, null=True, upload_to='devis/')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client')),
                ('facture_associee', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='factures.facture')),
            ],
        ),
        migrations.CreateModel(
            name='LigneDevis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('quantite', models.IntegerField(default=1)),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cout_unitaire', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('tva', models.DecimalField(decimal_places=2, default=21, max_digits=4)),
                ('devis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='devis.devis')),
                ('prestation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prestations.prestation')),
            ],
        ),
    ]
