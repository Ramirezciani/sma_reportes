# Documentación del Proyecto Sistema de Reportes Ambientales

## 1. Creación del Proyecto Django
```bash
django-admin startproject sistema_reportes
cd sistema_reportes
```

## 2. Creación de la App Reportes
```bash
python manage.py startapp reportes
```

## 3. Instalación de Dependencias
```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install drf-yasg
```

## 4. Configuración de settings.py
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'reportes',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

## 5. Creación de Modelos
```python
# reportes/models.py
class OrganismoSectorial(models.Model):
    nombre = models.CharField(max_length=200)
    sigla = models.CharField(max_length=50)
    # ... otros campos

class PPDA(models.Model):
    nombre = models.CharField(max_length=200)
    organismo = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE)
    # ... otros campos

class MedidaAvance(models.Model):
    ppda = models.ForeignKey(PPDA, on_delete=models.CASCADE)
    fecha = models.DateField()
    avance = models.DecimalField(max_digits=5, decimal_places=2)
    # ... otros campos
```

## 6. Creación de Serializers
```python
# reportes/serializers.py
class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'

# ... otros serializers
```

## 7. Creación de Views
```python
# reportes/views.py
class OrganismoSectorialViewSet(viewsets.ModelViewSet):
    queryset = OrganismoSectorial.objects.all()
    serializer_class = OrganismoSectorialSerializer
    permission_classes = [IsAuthenticated]

# ... otras views
```

## 8. Configuración de URLs
```python
# reportes/urls.py
router = DefaultRouter()
router.register(r'organismos-sectoriales', OrganismoSectorialViewSet)
# ... otros endpoints

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
```

## 9. Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 10. Creación de Superusuario
```bash
python manage.py createsuperuser
```

## 11. Ejecución del Servidor
```bash
python manage.py runserver
```

## Endpoints Disponibles
- Panel de administración: http://127.0.0.1:8000/admin/
- Documentación API: http://127.0.0.1:8000/swagger/
- Autenticación: POST http://127.0.0.1:8000/api/token/
- Organismos Sectoriales: GET/POST http://127.0.0.1:8000/api/organismos-sectoriales/
- Planes PPDA: GET/POST http://127.0.0.1:8000/api/planes-ppda/
- Medidas de Avance: GET/POST http://127.0.0.1:8000/api/medidas-avance/
