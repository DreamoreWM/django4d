from django.db import models
import os
from django.contrib.auth.models import User

class TypeIntervention(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Order(models.Model):
    ETAT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    numero = models.CharField(max_length=20, unique=True)
    type_prestation = models.ForeignKey(TypeIntervention, on_delete=models.CASCADE)
    date_emission = models.DateField()
    date_max_realisation = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    adresse_intervention = models.TextField()
    adresse_bailleur = models.TextField()
    nom_bailleur = models.CharField(max_length=100)
    nom_prenom_locataire = models.CharField(max_length=100)
    commentaire = models.TextField(blank=True)
    nombre_passages = models.PositiveIntegerField()
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='en_cours')
    def __str__(self):
        return self.numero
    
def signature_upload_to(instance, filename):
    # Générer un nom de fichier unique basé sur l'ID de l'intervention
    return os.path.join('signatures', f'intervention_{instance.id}_signature.png')

def rapport_pdf_upload_to(instance, filename):
    # Générer un nom de fichier unique basé sur l'ID de l'intervention
    return os.path.join('rapports', f'intervention_{instance.id}_rapport.pdf')

class Intervention(models.Model):
    ETAT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
    ]
    date_execution = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    bon_de_commande = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='interventions')
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='en_attente')
    signature = models.ImageField(upload_to=signature_upload_to, null=True, blank=True)
    rapport_pdf = models.FileField(upload_to=rapport_pdf_upload_to, blank=True, null=True)
    def __str__(self):
        return f"Intervention {self.id} pour {self.bon_de_commande.numero}"
    
    def save(self, *args, **kwargs):
        # Si un fichier existant est remplacé, supprimer l'ancien fichier du stockage
        if self.pk:  # Si l'instance existe déjà (mise à jour)
            old_instance = Intervention.objects.get(pk=self.pk)
            if old_instance.signature and self.signature and old_instance.signature != self.signature:
                old_instance.signature.delete(save=False)  # Supprimer l'ancien fichier signature
            if old_instance.rapport_pdf and self.rapport_pdf and old_instance.rapport_pdf != self.rapport_pdf:
                old_instance.rapport_pdf.delete(save=False)  # Supprimer l'ancien fichier PDF
        super().save(*args, **kwargs)   

class Photo(models.Model):
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    def __str__(self):
        return f"Photo pour intervention {self.intervention.id}"