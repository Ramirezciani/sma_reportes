from celery import shared_task
from .snifa_integration import obtener_datos_snifa
from .airecoo_integration import obtener_datos_airecoo
from .views import guardar_datos_snifa, guardar_datos_airecoo

@shared_task
def tarea_integrar_snifa():
    datos_snifa = obtener_datos_snifa()
    if datos_snifa:
        guardar_datos_snifa(datos_snifa)

@shared_task
def tarea_integrar_airecoo():
    datos_airecoo = obtener_datos_airecoo()
    if datos_airecoo:
        guardar_datos_airecoo(datos_airecoo)