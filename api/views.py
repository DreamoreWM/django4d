from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import TypeIntervention, Order, Intervention, Photo
from .serializers import TypeInterventionSerializer, OrderSerializer, InterventionSerializer, PhotoSerializer, UserSerializer
from .permissions import IsResponsable, CanUpdateIntervention
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from weasyprint import HTML
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    groups = [group.name for group in user.groups.all()]
    return Response({
        'id': user.id,
        'username': user.username,
        'groups': groups,
    })

class TypeInterventionViewSet(viewsets.ModelViewSet):
    queryset = TypeIntervention.objects.all()
    serializer_class = TypeInterventionSerializer
    permission_classes = [IsResponsable]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsResponsable()]
        return [permissions.IsAuthenticated()]

class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all() # Ajuste
    serializer_class = InterventionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date_execution', 'etat']
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Pour gérer les fichiers

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Responsable').exists():
            return Intervention.objects.all()
        elif user.groups.filter(name='Employé').exists():
            return Intervention.objects.filter(employee=user)
        return Intervention.objects.none()

    def update(self, request, *args, **kwargs):
        print("Données reçues :", request.data) 
        partial = kwargs.pop('partial', True)  # Autorise les mises à jour partielles
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Pour gérer les fichiers

    def get_queryset(self):
        return Photo.objects.filter(intervention_id=self.kwargs['intervention_pk'])

    def create(self, request, *args, **kwargs):
        intervention_id = kwargs.get('intervention_pk')
        intervention = Intervention.objects.get(id=intervention_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(intervention=intervention)
        return Response(serializer.data)

class EmployeListView(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Employé')
    serializer_class = UserSerializer
    permission_classes = [IsResponsable]


def generate_pdf(intervention):
    html = f"""
    <html><body>
    <h1>Rapport d'intervention</h1>
    <p>Date: {intervention.date_execution}</p>
    <p>Description: {intervention.description}</p>
    {''.join([f'<img src="{photo.image.path}" />' for photo in intervention.photos.all()])}
    <p>Signature: <img src="{intervention.signature.path}" /></p>
    </body></html>
    """
    pdf = HTML(string=html).write_pdf()
    return pdf