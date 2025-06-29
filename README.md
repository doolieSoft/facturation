# 🧾 Gestion de Facturation - Django + HTMX + PDF

Ce projet permet de créer des factures clients à partir de prestations définies, avec calcul de prix, gestion de marge, et génération automatique de factures PDF.

## 🔧 Fonctionnalités principales

- Création de factures via une interface Django.
- Ajout dynamique de prestations avec HTMX (quantité, coût unitaire, prix unitaire).
- Calcul automatique de la marge avec alerte si celle-ci est nulle ou négative.
- Génération de fichiers PDF au format professionnel.
- Export des factures PDF dans un dossier configurable.

---

## 🏗 Structure du projet

- `models.py` : modèles `Client`, `Prestation`, `Facture`, `LigneFacture`.
- `views.py` :
  - `FactureCreateView` : création de facture avec lignes dynamiques.
  - `FactureAjouterPrestationView` : ajout HTMX d’une ligne de facture.
- `templates/factures/` :
  - `facture_form.html` : formulaire principal.
  - `partials/ligne_prestation.html` : ligne HTML insérée dynamiquement.
- `utils/pdf.py` : fonction `generer_pdf_facture(facture, output_path)`.

---

## 📄 Exemple d’utilisation de `generer_pdf_facture`

```python
from utils.pdf import generer_pdf_facture

facture = Facture.objects.get(pk=1)
generer_pdf_facture(facture, output_path="exports/factures")
```

Si le dossier "exports/factures" n'existe pas, il sera automatiquement créé. Le fichier sera nommé facture_0001.pdf

## ⚠️ Avertissement marge

Lors de la sélection d’une prestation, le champ Coût unitaire est prérempli. Si le coût unitaire est supérieur ou égal au prix unitaire, un message d’alerte s’affiche pour signaler une marge nulle ou négative.

## 📦 Installation

Cloner le projet :
```bash
git clone https://github.com/dooliesoft/facturation.git
```

```bash
cd facturation
```

Créer un environnement virtuel :
```bash
python -m venv env
source env/bin/activate
```

Installer les dépendances :
```bash
pip install -r requirements.txt
```

Appliquer les migrations :
```bash
python manage.py migrate
```

Lancer le serveur :
```bash
python manage.py runserver
```
