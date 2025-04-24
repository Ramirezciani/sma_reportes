import requests

def obtener_datos_snifa():
    """
    Obtiene datos desde la API de SNIFA.
    """
    url = "https://snifa.sma.gob.cl/api/datos"  # URL ficticia, reemplazar por la API real si existe
    headers = {
        "Authorization": "Bearer TU_TOKEN_DE_AUTENTICACION",  # Reemplaza con un token válido si es necesario
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Retorna los datos en formato JSON
        else:
            print(f"Error al obtener datos de SNIFA: {response.status_code}")
            return None
    except Exception as e:
        print(f"Excepción al conectar con SNIFA: {e}")
        return None