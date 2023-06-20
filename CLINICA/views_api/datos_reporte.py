import requests

url = 'https://clinicamr.onrender.com/api/'
class DatosReportes():
    def cargar_lista_autorizacion():
        response = requests.get(url+'autorizar/')
        if response.status_code == 200:
            data = response.json()
            lista = data['autorizar']
        else:
            lista  = []
        return lista
    
    def cargar_lista_cargos():
        response = requests.get(url+'cargos/')
        if response.status_code == 200:
            data = response.json()
            lista = data['cargos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_citas():
        response = requests.get(url+'citas/')
        if response.status_code == 200:
            data = response.json()
            lista = data['citas']
        else:
            lista  = []
        return lista
    
    def cargar_lista_pacientes():
        response = requests.get(url+'pacientes/')
        if response.status_code == 200:
            data = response.json()
            lista = data['pacientes']
        else:
            lista  = []
        return lista
    
    def cargar_lista_autorizacion1():
        response = requests.get(url+'autorizar/')
        if response.status_code == 200:
            data = response.json()
            lista = data['autorizar']
        else:
            lista  = []
        return lista

    def cargar_usuario():
        response = requests.get(url+'usuarios/busqueda/sesion/1')
        if response.status_code == 200:
            data = response.json()
            usuario = data['usuariosr']
            nombre = usuario[0]['nombreUsuario']
        else:
            nombre  = ''
        return nombre