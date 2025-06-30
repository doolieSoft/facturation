# [🧾 Gestion de Facturation - Django + HTMX + PDF](https://dooliesoft.github.io/facturation/)

Ce projet permet de gérer facilement la facturation et les devis clients à partir de prestations configurables. Il inclut le calcul de marges, la gestion de la TVA, ainsi que la génération automatique de fichiers PDF professionnels.

[Site documentation github pages](https://dooliesoft.github.io/facturation/)

[Vidéo démo](./descriptions.md)

[Live démo](https://cimeclean.pythonanywhere.com/)

## 💼 Factures
Création de factures via une interface Django ergonomique.

Ajout dynamique de lignes de prestations (HTMX).

Calcul automatique de la marge par ligne.

Avertissement visuel en cas de marge nulle ou négative.

Génération automatique de fichiers PDF professionnels.

Export configurable des fichiers PDF.

## 📝 Devis
Création de devis à partir des prestations enregistrées.

Suivi de l’envoi au client (marquage comme envoyé / non envoyé).

Conversion d’un devis en facture en un clic.

Historique des devis pour chaque client.

## 📚 Prestations
Gestion centralisée des types de prestations.

Définition du coût unitaire, du prix unitaire et du taux de TVA.

Utilisation simplifiée lors de la création de factures ou de devis.

---

## 🏗 Structure du projet
Applications principales
- factures/ : gestion des factures.
- devis/ : gestion des devis.
- prestations/ : gestion des prestations disponibles.

Fichiers clés
- models.py :

  - Client, Prestation, Facture, LigneFacture, Devis, LigneDevis

- views.py :

  - FactureCreateView, FactureAjouterPrestationView
  - DevisCreateView, DevisToFactureView, MarquerDevisEnvoyeView

- templates/ :

  - factures/, devis/, prestations/

- utils/pdf.py :

  -generer_pdf_facture(facture, output_path)

  - generer_pdf_devis(devis, output_path)


---

## 📄 Exemple d’utilisation : generer_pdf_facture
```python
from utils.pdf import generer_pdf_facture

facture = Facture.objects.get(pk=1)
generer_pdf_facture(facture, output_path="exports/factures")
```

Le fichier sera généré dans exports/factures/ (créé automatiquement si besoin), avec un nom du type facture_0001.pdf.

## ⚠️ Avertissement marge

Lors de la sélection d’une prestation, le champ Coût unitaire est prérempli. Si le coût unitaire est supérieur ou égal au prix unitaire, un message d’alerte s’affiche pour signaler une marge nulle ou négative.

## 📦 Installation

Cloner le projet :
```bash
git clone https://github.com/dooliesoft/facturation.git
cd facturation
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## ✅ Prochaines améliorations possibles
- Signature électronique de devis/factures.

- Tableau de bord avec statistiques de vente.

- Export CSV/Excel des données.

- Intégration emailing pour l'envoi automatique de documents.
