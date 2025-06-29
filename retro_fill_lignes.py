import django
import os

# Adapte ce chemin à ton projet Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facturation.settings")
django.setup()

from factures.models import LigneFacture

def retro_fill():
    lignes = LigneFacture.objects.all()

    for ligne in lignes:
        if ligne.prestation:
            ligne.description = ligne.prestation.description
            ligne.prix_unitaire = ligne.prestation.prix
            ligne.tva = ligne.prestation.tva
            ligne.save()
            print(f"Ligne {ligne.id} mise à jour")
        else:
            print(f"⚠️ Ligne {ligne.id} sans prestation")

if __name__ == "__main__":
    retro_fill()
