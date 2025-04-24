from rest_framework import serializers
from .models import OrganismoSectorial, PPDA, MedidaAvance, Medida, Indicador, Actividad, ReporteAnual
from django.core.exceptions import ValidationError
from django.utils import timezone

class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = ['id', 'nombre', 'contacto', 'telefono']
        read_only_fields = ['id']

class PPDASerializer(serializers.ModelSerializer):
    organismo_nombre = serializers.CharField(source='organismo.get_nombre_display', read_only=True)
    
    class Meta:
        model = PPDA
        fields = [
            'id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_termino',
            'organismo', 'organismo_nombre', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'organismo_nombre']
        extra_kwargs = {
            'organismo': {'write_only': True}
        }

    def validate_fecha_inicio(self, value):
        if value < timezone.now().date():
            raise ValidationError("La fecha de inicio no puede ser en el pasado.")
        return value

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_termino = data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino and fecha_inicio > fecha_termino:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de término.")
        return data

class MedidaAvanceSerializer(serializers.ModelSerializer):
    medida_nombre = serializers.CharField(source='medida.nombre', read_only=True)
    medida_tipo = serializers.CharField(source='medida.get_tipo_display', read_only=True)
    
    class Meta:
        model = MedidaAvance
        fields = [
            'id', 'medida', 'medida_nombre', 'medida_tipo', 'descripcion',
            'fecha_limite', 'avance', 'estado', 'observaciones', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'medida_nombre', 'medida_tipo', 'fecha_actualizacion']
        extra_kwargs = {
            'medida': {'write_only': True}
        }

    def validate_avance(self, value):
        if value < 0 or value > 100:
            raise ValidationError("El avance debe estar entre 0 y 100.")
        return value


class IndicadorSerializer(serializers.ModelSerializer):
    organismo_nombre = serializers.CharField(source='organismo_sectorial.get_nombre_display', read_only=True)
    ppda_nombre = serializers.CharField(source='ppda.nombre', read_only=True)
    
    class Meta:
        model = Indicador
        fields = [
            'id', 'nombre', 'descripcion', 'valor', 'unidad',
            'organismo_sectorial', 'organismo_nombre', 'ppda', 'ppda_nombre',
            'fecha_registro', 'medio_verificacion'
        ]
        read_only_fields = ['id', 'organismo_nombre', 'ppda_nombre', 'fecha_registro']
        extra_kwargs = {
            'organismo_sectorial': {'write_only': True},
            'ppda': {'write_only': True}
        }

    def validate_valor(self, value):
        if value < 0:
            raise ValidationError("El valor no puede ser negativo.")
        return value
        
        
class ReporteAnualSerializer(serializers.ModelSerializer):
    organismo_nombre = serializers.CharField(source='organismo_responsable.get_nombre_display', read_only=True)
    medida_nombre = serializers.CharField(source='medida.medida.nombre', read_only=True)
    
    class Meta:
        model = ReporteAnual
        fields = [
            'id', 'organismo_responsable', 'organismo_nombre', 'periodo',
            'medida', 'medida_nombre', 'cumplimiento', 'observaciones'
        ]
        read_only_fields = ['id', 'organismo_nombre', 'medida_nombre']
        extra_kwargs = {
            'organismo_responsable': {'write_only': True},
            'medida': {'write_only': True}
        }

    def validate_cumplimiento(self, value):
        if value < 0 or value > 100:
            raise ValidationError("El cumplimiento debe estar entre 0 y 100.")
        return value
        
        
class ActividadSerializer(serializers.ModelSerializer):
    organismo_nombre = serializers.CharField(source='organismo_responsable.get_nombre_display', read_only=True)
    medida_nombre = serializers.CharField(source='medida.nombre', read_only=True)
    
    class Meta:
        model = Actividad
        fields = [
            'id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_termino',
            'medida', 'medida_nombre', 'organismo_responsable', 'organismo_nombre'
        ]
        read_only_fields = ['id', 'medida_nombre', 'organismo_nombre']
        extra_kwargs = {
            'medida': {'write_only': True},
            'organismo_responsable': {'write_only': True}
        }

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_termino = data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino and fecha_inicio > fecha_termino:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de término.")
        return data
