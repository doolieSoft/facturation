import json
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os


def charger_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_invoice(data, config, filename="facture.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    entreprise = config["entreprise"]

    # Coordonnées entreprise
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, height - 2 * cm, entreprise["nom"])
    c.setFont("Helvetica", 10)
    y = height - 2.5 * cm
    for ligne in entreprise["adresse"]:
        c.drawString(2 * cm, y, ligne)
        y -= 0.4 * cm
    c.drawString(2 * cm, y, f"TVA : {entreprise['tva']}")
    y -= 0.4 * cm
    c.drawString(2 * cm, y, f"Tél : {entreprise['telephone']}")
    y -= 0.4 * cm
    c.drawString(2 * cm, y, f"Email : {entreprise['email']}")
    y -= 0.4 * cm
    c.drawString(2 * cm, y, f"Site : {entreprise['site_web']}")

    # Coordonnées client
    c.setFont("Helvetica-Bold", 12)
    c.drawString(12 * cm, height - 2 * cm, "Facturé à :")
    c.setFont("Helvetica", 10)
    y_client = height - 2.5 * cm
    for ligne in data["client"]["nom_et_adresse"]:
        c.drawString(12 * cm, y_client, ligne)
        y_client -= 0.4 * cm

    # Détails facture
    c.setFont("Helvetica-Bold", 12)
    y_position = min(y, y_client) - 1 * cm
    c.drawString(2 * cm, y_position, f"Facture n°: {data['facture_num']}")
    c.drawString(12 * cm, y_position, f"Date: {data['date']}")

    # En-tête du tableau
    y_position -= 2 * cm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y_position, "Description")
    c.drawString(10 * cm, y_position, "Prix HTVA")
    c.drawString(13 * cm, y_position, "TVA %")
    c.drawString(16 * cm, y_position, "TVAC")

    # Lignes
    y_position -= 0.5 * cm
    c.setFont("Helvetica", 10)
    total_htva = total_tva = total_tvac = 0

    for item in data["lignes"]:
        htva = item["prix_unitaire"]
        tva = htva * item["tva"] / 100
        tvac = htva + tva
        total_htva += htva
        total_tva += tva
        total_tvac += tvac

        c.drawString(2 * cm, y_position, item["description"])
        c.drawRightString(12 * cm, y_position, f"{htva:.2f} €")
        c.drawRightString(15 * cm, y_position, f"{item['tva']} %")
        c.drawRightString(19 * cm, y_position, f"{tvac:.2f} €")
        y_position -= 0.5 * cm

    # Totaux
    y_position -= 1 * cm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(12 * cm, y_position, "Total HTVA :")
    c.drawRightString(19 * cm, y_position, f"{total_htva:.2f} €")

    y_position -= 0.5 * cm
    c.drawRightString(12 * cm, y_position, "Total TVA :")
    c.drawRightString(19 * cm, y_position, f"{total_tva:.2f} €")

    y_position -= 0.5 * cm
    c.drawRightString(12 * cm, y_position, "Total TVAC :")
    c.drawRightString(19 * cm, y_position, f"{total_tvac:.2f} €")

    c.showPage()
    c.save()

    return filename  # <- utile pour FileResponse


def generer_pdf_facture(facture, output_path=None):
    """
    Génère un PDF pour une instance de modèle `Facture`.
    """
    config = charger_config()

    # Construire les données compatibles avec create_invoice()
    client = facture.client
    data = {
        "client": {
            "nom_et_adresse": [
                client.nom,
                client.adresse,
                f"Tél : {client.telephone}",
                f"Email : {client.email}",
            ]
        },
        "facture_num": str(facture.pk).zfill(4),
        "date": facture.date.strftime("%d/%m/%Y"),
        "lignes": [
            {
                "description": ligne.prestation.description,
                "prix_unitaire": ligne.prix_unitaire * ligne.quantite,
                "tva": float(ligne.tva),
            }
            for ligne in facture.lignes.all()
        ]
    }

    for ligne in facture.lignes.all():
        prestation = ligne.prestation
        data["lignes"].append({
            "description": prestation.description,
            "prix_unitaire": prestation.prix * ligne.quantite,
            "tva": 21  # ou prestation.tva si tu veux le rendre variable
        })

    filename = output_path or f"facture_{facture.pk}.pdf"
    return create_invoice(data, config, filename)
