from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from devis.forms import DevisForm, LigneDevisFormSet
from devis.models import Devis, LigneDevis
from factures.models import Facture, LigneFacture
from factures.utils import generer_pdf_facture
from prestations.models import Prestation


class ConvertirDevisEnFactureView(View):
    def post(self, request, devis_id):
        devis = get_object_or_404(Devis, pk=devis_id)

        if devis.facture_associee:
            # Déjà converti
            return redirect("facture_detail", devis.facture_associee.pk)

        # Création de la facture
        facture = Facture.objects.create(client=devis.client)

        for ligne in devis.lignes.all():
            LigneFacture.objects.create(
                facture=facture,
                prestation=ligne.prestation,
                quantite=ligne.quantite,
                description=ligne.description,
                prix_unitaire=ligne.prix_unitaire,
                cout_unitaire=0,  # ou autre si tu le gères
                tva=ligne.tva,
            )

        # Lier la facture au devis
        devis.facture_associee = facture
        devis.save()

        # Génération de la facture PDF
        filename = generer_pdf_facture(facture)
        facture.pdf_filename = filename
        facture.save()

        return redirect("facture_detail", facture.pk)


class DevisDetailView(DetailView):
    model = Devis
    template_name = "devis/devis_detail.html"
    context_object_name = "devis"


class DevisListView(ListView):
    model = Devis
    template_name = "devis/devis_list.html"
    context_object_name = "devis_list"
    ordering = ['-date']  # plus récents en premier


class DevisCreateView(View):
    def get(self, request):
        form = DevisForm()
        formset = LigneDevisFormSet()
        prestations = Prestation.objects.all()
        return render(request, "devis/devis_form.html", {
            "form": form,
            "formset": formset,
            "prestations": prestations
        })

    def post(self, request):
        form = DevisForm(request.POST)
        formset = LigneDevisFormSet(request.POST)

        if not form.is_valid():
            prestations = Prestation.objects.all()
            return render(request, "devis/devis_form.html", {
                "form": form,
                "prestations": prestations,
            })

        # 1. Enregistrer la facture
        devis = form.save()

        # 2. Traiter les prestations ajoutées dynamiquement
        total_lignes = int(request.POST.get("total_lignes", 0))

        for i in range(total_lignes):
            prestation_id = request.POST.get(f"lignes-{i}-prestation_id")
            quantite = request.POST.get(f"lignes-{i}-quantite")
            cout_unitaire = request.POST.get(f"lignes-{i}-cout_unitaire")
            prix_unitaire = request.POST.get(f"lignes-{i}-prix_unitaire")

            if prestation_id and quantite:
                try:
                    prestation = Prestation.objects.get(pk=prestation_id)
                    LigneDevis.objects.create(
                        devis=devis,
                        prestation=prestation,
                        description=prestation.description,
                        quantite=int(quantite),
                        prix_unitaire=prix_unitaire,
                        cout_unitaire=cout_unitaire,
                        tva=prestation.tva  # assuming prestation has a 'tva' field
                    )
                except Prestation.DoesNotExist:
                    pass  # ou log si tu veux

        #pdf_filename = generer_pdf_devis(devis)
        #devis.pdf_filename = pdf_filename
        devis.save()

        # 3. Redirection vers la page de détail
        return redirect(reverse("devis_detail", args=[devis.pk]))


class DevisAjouterPrestationView(View):
    def post(self, request):
        prestation_id = request.POST.get("prestation_id")
        quantite = request.POST.get("quantite", 1)
        cout_unitaire = request.POST.get("cout_unitaire", "0")
        prix_unitaire = request.POST.get("prix_unitaire", "0")
        index = request.POST.get("index", "0")

        try:
            prestation = Prestation.objects.get(pk=prestation_id)
        except Prestation.DoesNotExist:
            return HttpResponseBadRequest("Prestation invalide")

        context = {
            "prestation": prestation,
            "quantite": quantite,
            "cout_unitaire": cout_unitaire,
            "prix_unitaire": prix_unitaire,
            "index": index,
        }
        return render(request, "devis/partials/ligne_prestation.html", context)
