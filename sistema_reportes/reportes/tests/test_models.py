from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from reportes.models import (
    PerfilUsuario,
    OrganismoSectorial,
    PPDA,
    Medida,
    MedidaAvance,
    Indicador,
    AlertaCritica,
    ReporteAnual,
    ReporteConsolidado,
    Actividad
)
from django.utils import timezone
import datetime

User = get_user_model()

class ModelFixturesMixin:
    @classmethod
    def setUpTestData(cls):
        # Crear usuario base
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Crear perfil de usuario
        cls.perfil = PerfilUsuario.objects.create(
            user=cls.user,
            rol='admin'
        )
        
        # Crear organismo sectorial
        cls.organismo = OrganismoSectorial.objects.create(
            nombre='SEA',
            contacto='contacto@sea.cl',
            telefono='+56223456789'
        )
        
        # Crear PPDA
        hoy = timezone.now().date()
        cls.ppda = PPDA.objects.create(
            nombre='PPDA 2023-2025',
            descripcion='Plan de prevención y descontaminación atmosférica',
            fecha_inicio=hoy,
            fecha_termino=hoy + datetime.timedelta(days=365*2),
            organismo=cls.organismo,
            creado_por=cls.user
        )

class PerfilUsuarioModelTest(ModelFixturesMixin, TestCase):
    def test_perfil_creacion(self):
        self.assertEqual(self.perfil.rol, 'admin')
        self.assertEqual(self.perfil.user.username, 'testuser')
        self.assertIsNotNone(self.perfil.fecha_creacion)
        self.assertIsNotNone(self.perfil.fecha_actualizacion)

    def test_perfil_str_representation(self):
        self.assertEqual(str(self.perfil), 'testuser - admin')

    def test_perfil_user_one_to_one_relation(self):
        self.assertEqual(self.user.perfil, self.perfil)

class OrganismoSectorialModelTest(ModelFixturesMixin, TestCase):
    def test_organismo_creacion(self):
        self.assertEqual(self.organismo.nombre, 'SEA')
        self.assertEqual(self.organismo.contacto, 'contacto@sea.cl')
        self.assertEqual(self.organismo.telefono, '+56223456789')
        self.assertIsNotNone(self.organismo.fecha_creacion)
        self.assertIsNotNone(self.organismo.fecha_actualizacion)

    def test_organismo_str_representation(self):
        self.assertEqual(str(self.organismo), 'Servicio de Evaluación Ambiental')

    def test_organismo_nombre_unique(self):
        with self.assertRaises(ValidationError):
            OrganismoSectorial.objects.create(
                nombre='SEA',
                contacto='otro@sea.cl'
            )

class PPDAModelTest(ModelFixturesMixin, TestCase):
    def test_ppda_creacion(self):
        self.assertEqual(self.ppda.nombre, 'PPDA 2023-2025')
        self.assertEqual(self.ppda.organismo, self.organismo)
        self.assertEqual(self.ppda.creado_por, self.user)
        self.assertIsNotNone(self.ppda.fecha_creacion)
        self.assertIsNotNone(self.ppda.fecha_actualizacion)

    def test_ppda_str_representation(self):
        self.assertEqual(str(self.ppda), 'PPDA 2023-2025')

    def test_ppda_fecha_validation(self):
        # Fecha inicio posterior a término
        ppda = PPDA(
            nombre='PPDA Inválido',
            fecha_inicio=timezone.now().date() + datetime.timedelta(days=1),
            fecha_termino=timezone.now().date(),
            organismo=self.organismo
        )
        with self.assertRaises(ValidationError):
            ppda.clean()

        # Fecha inicio en pasado
        ppda.fecha_inicio = timezone.now().date() - datetime.timedelta(days=1)
        with self.assertRaises(ValidationError):
            ppda.clean()

class MedidaModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.medida = Medida.objects.create(
            nombre='Reducción emisiones industriales',
            tipo='regulatoria',
            descripcion='Medida para reducir emisiones en un 30%',
            fecha_inicio=timezone.now().date(),
            fecha_termino=timezone.now().date() + datetime.timedelta(days=180),
            prioridad='alta',
            organismo_responsable=cls.organismo
        )

    def test_medida_creacion(self):
        self.assertEqual(self.medida.nombre, 'Reducción emisiones industriales')
        self.assertEqual(self.medida.tipo, 'regulatoria')
        self.assertEqual(self.medida.prioridad, 'alta')
        self.assertEqual(self.medida.organismo_responsable, self.organismo)

    def test_medida_str_representation(self):
        self.assertEqual(str(self.medida), 'Reducción emisiones industriales (Regulatoria)')

class MedidaAvanceModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.medida = Medida.objects.create(
            nombre='Control emisiones vehiculares',
            tipo='regulatoria',
            descripcion='Reducción de emisiones en transporte',
            fecha_inicio=timezone.now().date(),
            fecha_termino=timezone.now().date() + datetime.timedelta(days=180),
            organismo_responsable=cls.organismo
        )
        cls.avance = MedidaAvance.objects.create(
            medida=cls.medida,
            descripcion='Implementación de normativa EURO VI',
            fecha_limite=timezone.now().date() + datetime.timedelta(days=60),
            avance=30,
            estado='E'
        )

    def test_avance_creacion(self):
        self.assertEqual(self.avance.medida, self.medida)
        self.assertEqual(self.avance.descripcion, 'Implementación de normativa EURO VI')
        self.assertEqual(self.avance.avance, 30)
        self.assertEqual(self.avance.estado, 'E')
        self.assertIsNotNone(self.avance.fecha_actualizacion)

    def test_avance_str_representation(self):
        expected_str = f"{self.medida.nombre} - Implementación de normativa EURO VI"
        self.assertEqual(str(self.avance), expected_str[:50])

    def test_avance_porcentaje_validation(self):
        # Avance mayor a 100
        with self.assertRaises(ValidationError):
            MedidaAvance.objects.create(
                medida=self.medida,
                descripcion='Avance inválido',
                fecha_limite=timezone.now().date(),
                avance=110,
                estado='E'
            )

        # Avance menor a 0
        with self.assertRaises(ValidationError):
            MedidaAvance.objects.create(
                medida=self.medida,
                descripcion='Avance inválido',
                fecha_limite=timezone.now().date(),
                avance=-10,
                estado='E'
            )

class IndicadorModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.indicador = Indicador.objects.create(
            nombre='Concentración PM2.5',
            descripcion='Material particulado fino',
            valor=25.4,
            unidad='µg/m³',
            organismo_sectorial=cls.organismo,
            ppda=cls.ppda
        )

    def test_indicador_creacion(self):
        self.assertEqual(self.indicador.nombre, 'Concentración PM2.5')
        self.assertEqual(self.indicador.valor, 25.4)
        self.assertEqual(self.indicador.unidad, 'µg/m³')
        self.assertEqual(self.indicador.organismo_sectorial, self.organismo)
        self.assertEqual(self.indicador.ppda, self.ppda)

    def test_indicador_str_representation(self):
        expected_str = 'Concentración PM2.5 - 25.4 µg/m³'
        self.assertEqual(str(self.indicador), expected_str)

class AlertaCriticaModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.alerta = AlertaCritica.objects.create(
            descripcion='Nivel crítico de contaminación en sector norte',
            estado='pendiente',
            organismo_sectorial=cls.organismo,
            ppda=cls.ppda
        )

    def test_alerta_creacion(self):
        self.assertEqual(self.alerta.descripcion, 'Nivel crítico de contaminación en sector norte')
        self.assertEqual(self.alerta.estado, 'pendiente')
        self.assertEqual(self.alerta.organismo_sectorial, self.organismo)
        self.assertEqual(self.alerta.ppda, self.ppda)
        self.assertIsNotNone(self.alerta.fecha_alerta)

    def test_alerta_str_representation(self):
        self.assertEqual(str(self.alerta), 'Nivel crítico de contaminación en sector norte')

    def test_alerta_estado_choices(self):
        with self.assertRaises(ValidationError):
            AlertaCritica.objects.create(
                descripcion='Alerta inválida',
                estado='invalido',
                organismo_sectorial=self.organismo
            )

class ReporteAnualModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.medida = Medida.objects.create(
            nombre='Control de emisiones',
            tipo='regulatoria',
            organismo_responsable=cls.organismo
        )
        cls.avance = MedidaAvance.objects.create(
            medida=cls.medida,
            descripcion='Avance anual',
            fecha_limite=timezone.now().date()
        )
        cls.reporte = ReporteAnual.objects.create(
            organismo_responsable=cls.organismo,
            periodo=timezone.now().date(),
            medida=cls.avance,
            cumplimiento=85.5
        )

    def test_reporte_creacion(self):
        self.assertEqual(self.reporte.organismo_responsable, self.organismo)
        self.assertEqual(self.reporte.medida, self.avance)
        self.assertEqual(self.reporte.cumplimiento, 85.5)
        self.assertIsNotNone(self.reporte.periodo)

    def test_reporte_str_representation(self):
        expected_str = f"Reporte {self.reporte.periodo} - {self.organismo}"
        self.assertEqual(str(self.reporte), expected_str)

    def test_reporte_cumplimiento_range(self):
        # Cumplimiento mayor a 100
        with self.assertRaises(ValidationError):
            ReporteAnual.objects.create(
                organismo_responsable=self.organismo,
                periodo=timezone.now().date(),
                medida=self.avance,
                cumplimiento=105
            )

        # Cumplimiento menor a 0
        with self.assertRaises(ValidationError):
            ReporteAnual.objects.create(
                organismo_responsable=self.organismo,
                periodo=timezone.now().date(),
                medida=self.avance,
                cumplimiento=-5
            )

class ReporteConsolidadoModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.medida = Medida.objects.create(
            nombre='Control emisiones',
            tipo='regulatoria',
            organismo_responsable=cls.organismo
        )
        cls.avance = MedidaAvance.objects.create(
            medida=cls.medida,
            descripcion='Avance consolidado',
            fecha_limite=timezone.now().date()
        )
        cls.reporte_anual = ReporteAnual.objects.create(
            organismo_responsable=cls.organismo,
            periodo=timezone.now().date(),
            medida=cls.avance,
            cumplimiento=75.0
        )
        cls.reporte = ReporteConsolidado.objects.create(
            ppda=cls.ppda,
            periodo=timezone.now().date(),
            cumplimiento_general=82.5,
            estado='aprobado'
        )
        cls.reporte.reportes_anuales.add(cls.reporte_anual)

    def test_reporte_creacion(self):
        self.assertEqual(self.reporte.ppda, self.ppda)
        self.assertEqual(self.reporte.cumplimiento_general, 82.5)
        self.assertEqual(self.reporte.estado, 'aprobado')
        self.assertEqual(self.reporte.reportes_anuales.count(), 1)
        self.assertEqual(self.reporte.reportes_anuales.first(), self.reporte_anual)

    def test_reporte_str_representation(self):
        expected_str = f"Consolidado {self.reporte.periodo} - PPDA 2023-2025"
        self.assertEqual(str(self.reporte), expected_str)

    def test_reporte_estado_choices(self):
        with self.assertRaises(ValidationError):
            ReporteConsolidado.objects.create(
                ppda=self.ppda,
                periodo=timezone.now().date(),
                cumplimiento_general=90,
                estado='invalido'
            )

class ActividadModelTest(ModelFixturesMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actividad = Actividad.objects.create(
            nombre='Reunión de coordinación',
            descripcion='Revisión de avances PPDA',
            fecha=timezone.now().date(),
            hora_inicio=datetime.time(10, 0),
            hora_termino=datetime.time(12, 0),
            responsable=cls.user,
            organismo=cls.organismo
        )

    def test_actividad_creacion(self):
        self.assertEqual(self.actividad.nombre, 'Reunión de coordinación')
        self.assertEqual(self.actividad.responsable, self.user)
        self.assertEqual(self.actividad.organismo, self.organismo)
        self.assertEqual(self.actividad.hora_inicio, datetime.time(10, 0))
        self.assertEqual(self.actividad.hora_termino, datetime.time(12, 0))

    def test_actividad_str_representation(self):
        expected_str = f"Reunión de coordinación - {self.actividad.fecha}"
        self.assertEqual(str(self.actividad), expected_str)

    def test_actividad_hora_validation(self):
        # Hora término antes que hora inicio
        with self.assertRaises(ValidationError):
            Actividad.objects.create(
                nombre='Actividad inválida',
                fecha=timezone.now().date(),
                hora_inicio=datetime.time(14, 0),
                hora_termino=datetime.time(12, 0),
                responsable=self.user
            )
