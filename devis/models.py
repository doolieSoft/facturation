from datetime import timedelta
from decimal import Decimal

from django.db import models

from clients.models import Client
from prestations.models import Prestation


class Devis(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    validite_jours = models.PositiveIntegerField(default=90)
    remarques = models.TextField(blank=True)
    fichier_pdf = models.FileField(upload_to="devis/", blank=True, null=True)
    facture_associee = models.OneToOneField("factures.Facture", null=True, blank=True, on_delete=models.SET_NULL)

    def date_expiration(self):
        return self.date + timedelta(days=self.validite_jours)

    def __str__(self):
        return f"Devis {self.pk:04d} - {self.client.nom}"

    def total_htva(self):
        return sum(l.montant_htva() for l in self.lignes.all())

    def total_tva(self):
        return sum(l.montant_tva() for l in self.lignes.all())

    def total_tvac(self):
        return self.total_htva() + self.total_tva()


class LigneDevis(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name="lignes")
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tva = models.DecimalField(max_digits=4, decimal_places=2, default=21)

    def montant_htva(self):
        return self.prix_unitaire * self.quantite

    def montant_tva(self):
        return self.montant_htva() * self.tva / 100

    def montant_tvac(self):
        return self.montant_htva() + self.montant_tva()
