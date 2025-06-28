from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=255)
    tva = models.CharField("Numéro de TVA", max_length=20, blank=True)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nom
