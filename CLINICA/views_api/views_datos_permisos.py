import requests

url = 'https://clinicamr.onrender.com/api/'

def cargar_datos():
    response = requests.get(url+'datosPermisos/')
    if response.status_code == 200:
        data = response.json()
        permisos = data['permisos']
    else:
        permisos  = []
    return permisos