from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import OrganismoSectorial, PPDA, MedidaAvance, Indicador, Actividad, ReporteAnual
from .serializers import (
    OrganismoSectorialSerializer,
    PPDASerializer,
    MedidaAvanceSerializer,
    IndicadorSerializer,
    ActividadSerializer,
    ReporteAnualSerializer,
)
from .snifa_integration import obtener_datos_snifa
from .airecoo_integration import obtener_datos_airecoo
from rest_framework.decorators import api_view, permission_classes

class IsAdminPermission(BasePermission):
    """
    Permiso para usuarios del grupo 'admin'
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists()

class IsUserPermission(BasePermission):
    """
    Permiso para usuarios del grupo 'user'
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='user').exists()

class IsAuditorPermission(BasePermission):
    """
    Permiso para usuarios del grupo 'auditor'
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='auditor').exists()

class IsAdminOrUserPermission(BasePermission):
    """
    Permiso para usuarios de los grupos 'admin' o 'user'
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['admin', 'user']).exists()

class OrganismoSectorialViewSet(viewsets.ModelViewSet):
    serializer_class = OrganismoSectorialSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]
    
    def get_queryset(self):
        queryset = OrganismoSectorial.objects.all().order_by('nombre')
        nombre = self.request.query_params.get('nombre')
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class PPDAViewSet(viewsets.ModelViewSet):
    serializer_class = PPDASerializer
    permission_classes = [IsAuthenticated, IsAdminPermission,]
    
    def get_queryset(self):
        queryset = PPDA.objects.select_related('organismo').order_by('-fecha_creacion')
        organismo_id = self.request.query_params.get('organismo_id')
        if organismo_id:
            queryset = queryset.filter(organismo_id=organismo_id)
        return queryset
    
    @action(detail=True, methods=['get'])
    def medidas(self, request, pk=None):
        ppda = self.get_object()
        medidas = ppda.medida_set.all()
        serializer = MedidaAvanceSerializer(medidas, many=True)
        return Response(serializer.data)

class MedidaAvanceViewSet(viewsets.ModelViewSet):
    serializer_class = MedidaAvanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrUserPermission]
    
    def get_queryset(self):
        queryset = MedidaAvance.objects.select_related(
            'medida', 
            'medida__ppda'
        ).order_by('-fecha_actualizacion')
        
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
            
        avance_min = self.request.query_params.get('avance_min')
        if avance_min:
            queryset = queryset.filter(avance__gte=avance_min)
            
        return queryset
    
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.fecha_actualizacion = timezone.now()
        instance.save()

class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated, IsAdminOrUserPermission]
    
    def get_queryset(self):
        queryset = Actividad.objects.select_related(
            'organismo_responsable',
            'medida'
        ).order_by('-fecha_inicio')
        
        # Filtro por organismo del usuario
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                organismo_responsable=self.request.user.perfilusuario.organismo_responsable
            )
            
        # Filtros adicionales
        medida_id = self.request.query_params.get('medida_id')
        if medida_id:
            queryset = queryset.filter(medida_id=medida_id)
            
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
            
        return queryset

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'perfilusuario'):
            raise PermissionDenied("Usuario no tiene perfil asignado")
        if not self.request.user.perfilusuario.organismo_responsable:
            raise PermissionDenied("Usuario no tiene organismo asignado")
        serializer.save(organismo_responsable=self.request.user.perfilusuario.organismo_responsable)
        
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.fecha_actualizacion = timezone.now()
        instance.save()

class ReporteAnualViewSet(viewsets.ModelViewSet):
    serializer_class = ReporteAnualSerializer
    permission_classes = [IsAuthenticated, IsAdminOrUserPermission]
    
    def get_queryset(self):
        queryset = ReporteAnual.objects.select_related(
            'organismo_responsable',
            'medida'
        ).prefetch_related(
            'medida__medidaavance_set'
        ).order_by('-periodo')
        
        periodo = self.request.query_params.get('periodo')
        if periodo:
            queryset = queryset.filter(periodo=periodo)
            
        organismo_id = self.request.query_params.get('organismo_id')
        if organismo_id:
            queryset = queryset.filter(organismo_responsable_id=organismo_id)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(organismo_responsable=self.request.user.perfilusuario.organismo_responsable)
        
    @action(detail=False, methods=['get'])
    def resumen_anual(self, request):
        periodos = ReporteAnual.objects.values_list('periodo', flat=True).distinct()
        data = []
        for periodo in periodos:
            reportes = ReporteAnual.objects.filter(periodo=periodo)
            promedio = reportes.aggregate(Avg('cumplimiento'))['cumplimiento__avg']
            data.append({
                'periodo': periodo,
                'promedio_cumplimiento': round(promedio, 2) if promedio else 0
            })
        return Response(data)

def frontend_view(request):
    return render(request, 'reportes/index.html')

def guardar_datos_snifa(datos):
    if not isinstance(datos, list):
        raise ValueError("Los datos deben ser una lista")
        
    indicadores = []
    for dato in datos:
        if not all(key in dato for key in ['parametro', 'valor']):
            raise ValueError(f"Datos incompletos en SNIFA: {dato}")
            
        indicador = Indicador(
            nombre=dato['parametro'],
            valor=dato['valor'],
            unidad="µg/m³",
            organismo_sectorial_id=1,
            fuente="SNIFA"
        )
        indicadores.append(indicador)
    
    # Bulk create para mejor performance
    Indicador.objects.bulk_create(indicadores)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminPermission])
def integrar_snifa(request):
    try:
        datos_snifa = obtener_datos_snifa()
        if not datos_snifa:
            return JsonResponse({"error": "No se recibieron datos de SNIFA."}, status=500)
        guardar_datos_snifa(datos_snifa)
        return JsonResponse({"mensaje": "Datos de SNIFA integrados correctamente."})
    except ValueError as ve:
        return JsonResponse({"error": f"Error de validación: {str(ve)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error al integrar datos de SNIFA: {str(e)}"}, status=500)

def guardar_datos_airecoo(datos):
    if not isinstance(datos, list):
        raise ValueError("Los datos deben ser una lista")
        
    indicadores = []
    for dato in datos:
        if not all(key in dato for key in ['nombre', 'valor', 'unidad']):
            raise ValueError(f"Datos incompletos en Airecoo: {dato}")
            
        indicador = Indicador(
            nombre=dato['nombre'],
            valor=dato['valor'],
            unidad=dato['unidad'],
            organismo_sectorial_id=1,
            fuente="Airecoo"
        )
        indicadores.append(indicador)
    
    # Bulk create para mejor performance
    Indicador.objects.bulk_create(indicadores)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminPermission])
def integrar_airecoo(request):
    try:
        datos_airecoo = obtener_datos_airecoo()
        if not datos_airecoo:
            return JsonResponse({"error": "No se recibieron datos de Airecoo."}, status=500)
        guardar_datos_airecoo(datos_airecoo)
        return JsonResponse({"mensaje": "Datos de Airecoo integrados correctamente."})
    except ValueError as ve:
        return JsonResponse({"error": f"Error de validación: {str(ve)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error al integrar datos de Airecoo: {str(e)}"}, status=500)
