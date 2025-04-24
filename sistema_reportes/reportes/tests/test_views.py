from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from reportes.models import Reporte

User = get_user_model()

class ReporteViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            is_staff=True
        )
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='user@example.com'
        )
        cls.reporte = Reporte.objects.create(
            titulo='Reporte inicial',
            descripcion='Descripción inicial',
            creado_por=cls.user
        )

    def test_list_reporte_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('reporte-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_reporte_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'titulo': 'Nuevo reporte',
            'descripcion': 'Nueva descripción'
        }
        response = self.client.post(reverse('reporte-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reporte.objects.count(), 2)

    def test_update_reporte_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {'titulo': 'Título actualizado'}
        response = self.client.patch(
            reverse('reporte-detail', args=[self.reporte.id]),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reporte.refresh_from_db()
        self.assertEqual(self.reporte.titulo, 'Título actualizado')

    def test_delete_reporte_admin_only(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(
            reverse('reporte-detail', args=[self.reporte.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reporte.objects.count(), 0)
