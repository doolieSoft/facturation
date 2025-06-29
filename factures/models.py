# factures/models.py

from django.db import models

from clients.models import Client
from prestations.models import Prestation


class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    pdf_filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Facture {self.id} - {self.client.nom}"

    def total_htva(self):
        return sum(l.montant_htva() for l in self.lignes.all())

    def total_tva(self):
        return sum(l.montant_tva() for l in self.lignes.all())

    def total_tvac(self):
        return self.total_htva() + self.total_tva()


class LigneFacture(models.Model):
    facture = models.ForeignKey("Facture", related_name="lignes", on_delete=models.CASCADE)
    prestation = models.ForeignKey("prestations.Prestation", on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)  # Prix HTVA figé
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # coût réel
    tva = models.DecimalField(max_digits=4, decimal_places=2, default=21.0)  # TVA en pourcentage

    def montant_htva(self):
        return self.prix_unitaire * self.quantite

    def montant_tva(self):
        return self.montant_htva() * self.tva / 100

    @property
    def montant_tvac(self):
        base = self.prix_unitaire * self.quantite
        return base * (1 + self.tva / 100)

    def marge(self):
        if self.cout_unitaire is not None:
            return (self.prix_unitaire - self.cout_unitaire) * self.quantite
        return None

    def marge_pourcent(self):
        if self.cout_unitaire:
            return (self.prix_unitaire - self.cout_unitaire) / self.cout_unitaire * 100
        return None
