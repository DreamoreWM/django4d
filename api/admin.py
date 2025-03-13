from django.contrib import admin
from .models import Intervention, Order, TypeIntervention, Photo
from django import forms
from unfold.admin import ModelAdmin

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # Nombre de champs vides à afficher

@admin.register(Intervention)
class InterventionAdmin(ModelAdmin):
    inlines = [PhotoInline]
    list_display = ('id', 'date_execution', 'heure_debut', 'bon_de_commande', 'employee', 'etat')  # Champs à afficher dans le tableau
    list_filter = ('date_execution', 'etat', 'bon_de_commande')  # Filtres latéraux
    search_fields = ('description', 'bon_de_commande__adresse_intervention', 'bon_de_commande__type_prestation__name')  # Champs recherchables
    date_hierarchy = 'date_execution'  # Navigation par date

    # Personnaliser l’affichage du champ bon_de_commande pour montrer plus d’infos
    def bon_de_commande(self, obj):
        return f"{obj.bon_de_commande.numero} - {obj.bon_de_commande.adresse_intervention} ({obj.bon_de_commande.type_prestation.name})"
    bon_de_commande.short_description = 'Bon de commande'

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('numero', 'type_prestation', 'adresse_intervention', 'date_emission', 'etat')  # Champs à afficher
    list_filter = ('etat', 'type_prestation', 'date_emission')  # Filtres latéraux
    search_fields = ('numero', 'adresse_intervention', 'nom_bailleur', 'nom_prenom_locataire')  # Champs recherchables
    date_hierarchy = 'date_emission'  # Navigation par date

    # Personnaliser l’affichage de type_prestation pour montrer le name
    def type_prestation(self, obj):
        return obj.type_prestation.name if obj.type_prestation else "Non défini"
    type_prestation.short_description = 'Type de prestation'  # Nom affiché dans l’en-tête

    class Media:
        css = {
            'all': ('https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css',),
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js',
            '/static/admin/js/adresse_autocomplete.js',  # Fichier JavaScript personnalisé
        )

@admin.register(TypeIntervention)
class TypeInterventionAdmin(ModelAdmin):
    list_display = ('name',)  # Champs à afficher (simpleté, car TypeIntervention est basique)
    search_fields = ('name',)  # Champs recherchables

admin.site.site_header = "SENI 4D"
admin.site.site_title = "SENI 4D portail"
admin.site.index_title = "Bienvenue sur le portail SENI 4D"