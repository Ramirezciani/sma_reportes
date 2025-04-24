from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo PerfilUsuario
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=50, db_index=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['rol']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

# Validación de fechas
def validate_fecha_inicio_termino(fecha_inicio, fecha_termino):
    if fecha_inicio > fecha_termino:
        raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de término.")
    if fecha_inicio < timezone.now().date():
        raise ValidationError("La fecha de inicio no puede ser en el pasado.")

# Modelo OrganismoSectorial
class OrganismoSectorial(models.Model):
    TIPOS_ORGANISMO = [
        ('SEA', 'Servicio de Evaluación Ambiental'),
        ('SEC', 'Superintendencia de Electricidad y Combustible'),
        ('IRV', 'Intendencia Regional de Valparaíso'),
        ('DGTM', 'Dirección General del Territorio Marítimo y de Marina Mercante'),
        ('CONAF', 'Corporación Nacional Forestal'),
        ('SAG', 'Servicio Agrícola y Ganadero'),
    ]
    nombre = models.CharField(max_length=5, choices=TIPOS_ORGANISMO, unique=True, db_index=True)
    contacto = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return self.get_nombre_display()

# Modelo PPDA
class PPDA(models.Model):
    nombre = models.CharField(max_length=200, db_index=True)
    descripcion = models.TextField(blank=True, default='')
    fecha_inicio = models.DateField(db_index=True)
    fecha_termino = models.DateField(db_index=True)
    organismo = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE, related_name='ppdas', null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['fecha_inicio', 'fecha_termino']),
        ]

    def clean(self):
        validate_fecha_inicio_termino(self.fecha_inicio, self.fecha_termino)

    def __str__(self):
        return self.nombre

# Prioridades
PRIORIDADES = [
    ('alta', 'Alta'),
    ('media', 'Media'),
    ('baja', 'Baja'),
]

# Modelo Medida
class Medida(models.Model):
    TIPOS_MEDIDA = [
        ('regulatoria', 'Regulatoria'),
        ('no_regulatoria', 'No Regulatoria'),
    ]
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPOS_MEDIDA)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media')
    organismo_responsable = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

# Modelo MedidaAvance
class MedidaAvance(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('E', 'En progreso'),
        ('C', 'Completado'),
        ('R', 'Retrasado'),
    ]
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='avances')
    descripcion = models.TextField()
    fecha_limite = models.DateField()
    avance = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    observaciones = models.TextField(blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medida.nombre} - {self.descripcion[:50]}"

    class Meta:
        verbose_name = 'Medida de Avance'
        verbose_name_plural = 'Medidas de Avance'

# Modelo Indicador
class Indicador(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    valor = models.FloatField()
    unidad = models.CharField(max_length=50, blank=True)  # Ejemplo: "µg/m³"
    fecha_registro = models.DateField(auto_now_add=True)
    organismo_sectorial = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE)
    ppda = models.ForeignKey(PPDA, on_delete=models.CASCADE, null=True, blank=True)
    medio_verificacion = models.FileField(upload_to='medios_verificacion/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.valor} {self.unidad}"

# Modelo AlertaCritica
class AlertaCritica(models.Model):
    descripcion = models.TextField()
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('resuelta', 'Resuelta')])
    organismo_sectorial = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE)
    ppda = models.ForeignKey(PPDA, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.descripcion

# Modelo ReporteAnual
class ReporteAnual(models.Model):
    organismo_responsable = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE)
    periodo = models.DateField()
    medida = models.ForeignKey(MedidaAvance, on_delete=models.CASCADE)
    cumplimiento = models.FloatField(help_text="Porcentaje de cumplimiento")
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reporte {self.periodo} - {self.organismo_responsable}"

# Modelo ReporteConsolidado
class ReporteConsolidado(models.Model):
    organismo_responsable = models.ForeignKey(OrganismoSectorial, on_delete=models.CASCADE)
    periodo = models.DateField()
    resumen_actividades = models.TextField()
    archivo_reporte = models.FileField(upload_to='reportes_anuales/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ppda = models.ForeignKey(PPDA, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Reporte Consolidado {self.periodo} - {self.organismo_responsable}"
    
class Actividad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    medida = models.ForeignKey('Medida', on_delete=models.CASCADE, related_name='actividades')
    organismo_responsable = models.ForeignKey('OrganismoSectorial', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
