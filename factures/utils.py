import json
import os
from decimal import Decimal

from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

def charger_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_invoice(data, config, filename="facture.pdf"):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors

    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    elements = []

    # --- Coordonnées entreprise et client côte à côte ---
    entreprise = config["entreprise"]
    client = data["client"]

    entreprise_info = [
        f"<b>{entreprise['nom']}</b>",
        *entreprise["adresse"],
        f"TVA : {entreprise['tva']}",
        f"Tél : {entreprise['telephone']}",
        f"Email : {entreprise['email']}",
        f"Site : {entreprise['site_web']}"
    ]
    client_info = [
        "<b>Facturé à :</b>",
        *client["nom_et_adresse"]
    ]

    entreprise_para = [Paragraph(line, styles["Normal"]) for line in entreprise_info]
    client_para = [Paragraph(line, styles["Normal"]) for line in client_info]

    coord_table = Table([
        [entreprise_para, client_para]
    ], colWidths=[9 * cm, 7 * cm])

    coord_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(coord_table)
    elements.append(Spacer(1, 1 * cm))

    # Infos facture
    elements.append(Paragraph(f"<b>Facture n°:</b> {data['facture_num']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {data['date']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # En-tête du tableau + données
    styles = getSampleStyleSheet()

    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        alignment=1,  # 0=left, 1=center, 2=right
        fontName="Helvetica-Bold",
        fontSize=9,
        spaceAfter=6,
    )

    headers = [
        Paragraph("Description", style_table_header),
        Paragraph("Quantité", style_table_header),
        Paragraph("PU HTVA", style_table_header),
        Paragraph("TVA %", style_table_header),
        Paragraph("TVAC", style_table_header)
    ]

    table_data = [headers]  # ← première ligne : les titres
    total_htva = total_tva = total_tvac = 0

    for item in data["lignes"]:
        htva = item["prix_unitaire"]
        quantite = item["quantite"]
        pu = item["prix_unitaire_unitaire"]
        tva = htva * item["tva"] / 100
        tvac = htva + tva

        total_htva += htva
        total_tva += tva
        total_tvac += tvac

        table_data.append([
            item["description"],
            str(quantite),
            f"{pu:.2f} €",
            f"{item['tva']} %",
            f"{tvac:.2f} €"
        ])

    # Totaux
    table_data.append(["", "", f"{total_htva:.2f} €", f"{total_tva:.2f} €", f"{total_tvac:.2f} €"])

    table = Table(table_data, colWidths=[7*cm, 2*cm, 3*cm, 2*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 24))

    # Pied de page
    elements.append(Paragraph(
        "En vous souhaitant bonne réception de cette facture, veuillez agréer nos salutations distinguées.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "<i>Cette facture est soumise à nos conditions générales de vente.</i>",
        styles['Normal']
    ))

    doc.build(elements)
    return filename

def generer_pdf_facture(facture, output_path="media/factures"):
    config = charger_config()
    client = facture.client

    data = {
        "client": {
            "nom_et_adresse": [
                client.nom,
                *client.adresse_complete(),
                f"Tél : {client.telephone}",
                f"Email : {client.email}",
            ]
        },
        "facture_num": str(facture.pk).zfill(4),
        "date": facture.date.strftime("%d/%m/%Y"),
        "lignes": [
            {
                "description": ligne.prestation.description,
                "quantite": ligne.quantite,
                "prix_unitaire_unitaire": ligne.prix_unitaire,
                "prix_unitaire": ligne.prix_unitaire * ligne.quantite,
                "tva": Decimal(ligne.tva),
            }
            for ligne in facture.lignes.all()
        ]
    }

    if output_path is None:
        output_path = "."

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = os.path.join(output_path, f"facture_{facture.pk}.pdf")
    return create_invoice(data, config, filename)
