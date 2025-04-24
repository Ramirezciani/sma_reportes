from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import OrganismoSectorial, PPDA, Medida, Indicador, MedidaAvance, ReporteAnual, Actividad, PerfilUsuario

# Organización del admin por grupos lógicos
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20

# Registra los modelos en el panel de administración agrupados por categorías
@admin.register(OrganismoSectorial)
class OrganismoSectorialAdmin(BaseAdmin):
    list_display = ('nombre', 'contacto', 'telefono')
    search_fields = ('nombre',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'contacto', 'telefono')
        }),
    )

@admin.register(PPDA)
class PPDAAdmin(BaseAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_inicio', 'fecha_termino', 'organismo')
    list_filter = ('organismo',)
    search_fields = ('nombre', 'descripcion')
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'organismo')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_termino')
        }),
    )

@admin.register(Medida)
class MedidaAdmin(BaseAdmin):
    list_display = ('nombre', 'tipo', 'prioridad', 'organismo_responsable')
    list_filter = ('tipo', 'prioridad', 'organismo_responsable')
    search_fields = ('nombre',)
    fieldsets = (
        ('Identificación', {
            'fields': ('nombre', 'tipo', 'prioridad')
        }),
        ('Responsabilidad', {
            'fields': ('organismo_responsable',)
        }),
    )

@admin.register(Indicador)
class IndicadorAdmin(BaseAdmin):
    list_display = ('nombre', 'valor', 'unidad', 'organismo_sectorial', 'ppda')
    search_fields = ('nombre', 'unidad')
    list_filter = ('organismo_sectorial', 'ppda')
    fieldsets = (
        ('Datos Básicos', {
            'fields': ('nombre', 'valor', 'unidad')
        }),
        ('Relaciones', {
            'fields': ('organismo_sectorial', 'ppda')
        }),
    )

@admin.register(MedidaAvance)
class MedidaAvanceAdmin(BaseAdmin):
    list_display = ('medida', 'descripcion', 'avance', 'estado', 'fecha_limite')
    list_filter = ('estado', 'medida')
    search_fields = ('descripcion',)
    fieldsets = (
        ('Seguimiento', {
            'fields': ('medida', 'descripcion', 'fecha_limite')
        }),
        ('Progreso', {
            'fields': ('avance', 'estado')
        }),
    )

@admin.register(ReporteAnual)
class ReporteAnualAdmin(BaseAdmin):
    list_display = ('organismo_responsable', 'periodo', 'cumplimiento', 'medida')
    list_filter = ('periodo', 'organismo_responsable')
    search_fields = ('observaciones',)
    fieldsets = (
        ('Información General', {
            'fields': ('organismo_responsable', 'periodo')
        }),
        ('Resultados', {
            'fields': ('cumplimiento', 'observaciones')
        }),
    )

@admin.register(Actividad)
class ActividadAdmin(BaseAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_termino', 'organismo_responsable', 'medida')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('organismo_responsable',)
    fieldsets = (
        ('Planificación', {
            'fields': ('nombre', 'descripcion', 'organismo_responsable', 'medida')
        }),
        ('Temporalidad', {
            'fields': ('fecha_inicio', 'fecha_termino')
        }),
    )

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(BaseAdmin):
    list_display = ('user', 'rol', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('user__username', 'rol')
    list_filter = ('rol',)
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('user',)
        }),
        ('Roles y Permisos', {
            'fields': ('rol',)
        }),
    )

# Extender el UserAdmin para incluir el perfil
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    list_select_related = ('perfil',)

    def get_rol(self, obj):
        return obj.perfil.rol if hasattr(obj, 'perfil') else ''
    get_rol.short_description = 'Rol'

# Desregistrar el UserAdmin por defecto y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
