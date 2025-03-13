from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TypeInterventionViewSet, OrderViewSet, InterventionViewSet, PhotoViewSet, EmployeListView
from .views import get_user
from django.conf import settings
from django.conf.urls.static import static

# Créez une instance du router
router = DefaultRouter()

# Enregistrez les ViewSets avec un basename explicite
router.register(r'typeinterventions', TypeInterventionViewSet, basename='typeintervention')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'interventions', InterventionViewSet, basename='intervention')
router.register(r'photos', PhotoViewSet, basename='photo')

# Incluez les URLs générées par le router
urlpatterns = [
    path('user/', get_user, name='get_user'),
    path('', include(router.urls)),
    path('employes/', EmployeListView.as_view(), name='employe-list'),
    path('interventions/<int:intervention_pk>/photos/', PhotoViewSet.as_view({'post': 'create'}), name='intervention-photos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)