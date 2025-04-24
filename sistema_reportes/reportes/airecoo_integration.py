import requests

def obtener_datos_airecoo():
    """
    Obtiene datos desde la API de Airecoo.
    """
    url = "http://www.airecoo.mma.gob.cl/api/calidad-aire"  # URL ficticia, reemplazar por la API real
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Retorna los datos en formato JSON
        else:
            print(f"Error al obtener datos de Airecoo: {response.status_code}")
            return None
    except Exception as e:
        print(f"Excepción al conectar con Airecoo: {e}")
        return None