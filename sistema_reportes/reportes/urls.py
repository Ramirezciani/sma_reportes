from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganismoSectorialViewSet, PPDAViewSet, MedidaAvanceViewSet, frontend_view, integrar_snifa, integrar_airecoo

router = DefaultRouter()
router.register(r'organismos-sectoriales', OrganismoSectorialViewSet, basename='organismo-sectorial')
router.register(r'planes-ppda', PPDAViewSet, basename='ppda')
router.register(r'medidas-avance', MedidaAvanceViewSet, basename='medida-avance')
router.register(r'indicadores', MedidaAvanceViewSet, basename='indicadores')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('frontend/', frontend_view, name='frontend'),  # Nueva ruta para el frontend
    path('integrar-snifa/', integrar_snifa, name='integrar_snifa'),
    path('integrar-airecoo/', integrar_airecoo, name='integrar_airecoo'),



]
