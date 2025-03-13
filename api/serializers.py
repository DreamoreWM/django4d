from rest_framework import serializers
from .models import TypeIntervention, Order, Intervention, Photo
from django.contrib.auth.models import User
# from .serializers import InterventionSerializer, PhotoSerializer  # Add PhotoSerializer here

class TypeInterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeIntervention
        fields = ['id', 'name']

class OrderSerializer(serializers.ModelSerializer):
    type_prestation = TypeInterventionSerializer()
    class Meta:
        model = Order
        fields = ['id', 'numero', 'type_prestation', 'date_emission', 'date_max_realisation', 'montant', 'adresse_intervention', 'adresse_bailleur', 'nom_bailleur', 'nom_prenom_locataire', 'commentaire', 'nombre_passages', 'etat']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'intervention', 'image']
        read_only_fields = ['intervention']  # Intervention est défini dans la vue

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class InterventionSerializer(serializers.ModelSerializer):
    bon_de_commande = OrderSerializer()
    photos = PhotoSerializer(many=True, read_only=True)  # Lister les photos existantes
    signature = serializers.ImageField(required=False, allow_null=True)
    rapport_pdf = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Intervention
        fields = '__all__'

    def create(self, validated_data):
        return Intervention.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date_execution = validated_data.get('date_execution', instance.date_execution)
        instance.heure_debut = validated_data.get('heure_debut', instance.heure_debut)
        instance.heure_fin = validated_data.get('heure_fin', instance.heure_fin)
        instance.etat = validated_data.get('etat', instance.etat)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.description = validated_data.get('description', instance.description)
        instance.signature = validated_data.get('signature', instance.signature)
        instance.rapport_pdf = validated_data.get('rapport_pdf', instance.rapport_pdf)
        instance.save()
        return instance
    
