from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=255)
    numero_tva = models.CharField("Numéro de TVA", max_length=20, blank=True)
    rue = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nom

    def adresse_complete(self):
        return [
            self.rue,
            f"{self.code_postal} {self.ville}",
            self.pays
        ]