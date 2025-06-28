from django.db import models

# core/models.py

from django.db import models


class Prestation(models.Model):
    description = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    tva = models.PositiveIntegerField(default=21)

    def __str__(self):
        return self.description