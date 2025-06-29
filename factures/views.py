# factures/views.py
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView
from django.shortcuts import redirect, render

from prestations.models import Prestation
from .forms import FactureForm, LigneFactureFormSet
from django.views.generic import DetailView
from .models import Facture, LigneFacture
from .utils import generer_pdf_facture


class FactureDetailView(DetailView):
    model = Facture
    template_name = "factures/facture_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facture = self.object
        lignes = facture.lignes.all()

        # Calcul marges totales
        total_marge = sum((l.marge() or 0) for l in lignes)
        context["total_marge"] = total_marge
        context["lignes"] = lignes
        return context

class FactureCreateView(CreateView):
    model = Facture
    form_class = FactureForm
    template_name = "factures/facture_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = LigneFactureFormSet()
        prestations = Prestation.objects.all()

        return render(request, self.template_name,
                      {'form': form,
                       'formset': formset,
                       'prestations': prestations})

    def post(self, request, *args, **kwargs):
        form = FactureForm(request.POST)

        if not form.is_valid():
            prestations = Prestation.objects.all()
            return render(request, "factures/facture_form.html", {
                "form": form,
                "prestations": prestations,
            })

        # 1. Enregistrer la facture
        facture = form.save()

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
                    LigneFacture.objects.create(
                        facture=facture,
                        prestation=prestation,
                        quantite=int(quantite),
                        prix_unitaire=prix_unitaire,
                        cout_unitaire=cout_unitaire,
                        tva=prestation.tva  # assuming prestation has a 'tva' field
                    )
                except Prestation.DoesNotExist:
                    pass  # ou log si tu veux

        # 3. Redirection vers la page de détail
        return redirect(reverse("facture_detail", args=[facture.pk]))


class FactureAjouterPrestationView(View):
    def post(self, request, *args, **kwargs):
        prestation_id = request.POST.get("prestation_id")
        quantite = int(request.POST.get("quantite", 1))
        cout_unitaire = request.POST.get("cout_unitaire")
        prix_unitaire = request.POST.get("prix_unitaire")

        prestation = Prestation.objects.get(pk=prestation_id)

        # Préparer la ligne à afficher dans la liste (sans sauvegarder la facture encore)
        context = {
            "prestation": prestation,
            "cout_unitaire": cout_unitaire,
            "prix_unitaire": prix_unitaire,
            "quantite": quantite,
            "index": request.POST.get("index", 0),  # optionnel, si besoin d'un index unique
        }

        ligne_html = render_to_string("factures/partials/ligne_prestation.html", context, request=request)
        return HttpResponse(ligne_html)


class FactureListView(ListView):
    model = Facture
    template_name = "factures/facture_list.html"
    context_object_name = "factures"
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related("client")
        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(client__nom__icontains=search)

        return queryset


def generer_pdf(request, pk):
    facture = Facture.objects.get(pk=pk)
    pdf_path = generer_pdf_facture(facture, output_path="factures_generees")
    return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=f"facture_{pk}.pdf")
