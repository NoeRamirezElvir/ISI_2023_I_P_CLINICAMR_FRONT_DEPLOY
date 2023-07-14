from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.shortcuts import render
from passlib.context import CryptContext
import requests
from django.shortcuts import redirect
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos

url = 'https://clinicamr.onrender.com/api/'
def iniciar_sesion(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            response = requests.post(url+'login/', json={'username': username, 'password': password})
            data = response.json()
            if data['mensaje'] == 'Inicio Exitoso':
                mensaje = data['mensaje']
                logger = definir_log_info('inisio_sesion_login','logs_login')
                logger.debug(f'Se ha iniciado sesion - Usuario:{username}')
                return render(request, 'inicio.html', {'mensaje': mensaje, 'datos_permisos':cargar_datos()})
            else:
                mensaje = data['mensaje']
                logger = definir_log_info('inisio_sesion_login','logs_login')
                logger.debug(f'Ha tratado de iniciar sesion - Usuario:{username}, {mensaje}')
                return render(request, 'presentacion/usuariologin.html', {'mensaje': mensaje})
        else:
            logger = definir_log_info('inisio_sesion_login','logs_login')
            logger.debug('Entrando a funcion iniciar sesion')
            return render(request, 'presentacion/usuariologin.html')
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_login','logs_login')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'presentacion/usuariologin.html')
    
def registrar_login(request):
    rsp_empleado = requests.get(url+'empleados/')
    if rsp_empleado.status_code == 200:
            data = rsp_empleado.json()
            empleado = data['empleados']
    else:
            response = requests.post(url+'empleados/', json={'nombre': 'administrador','apellidos': 'administrador','fechaNacimiento': '01/01/2000','idTipoDocumentos':None, 'idEspecialidadMedico':None, 'idCargoEmpleado':None, 'documento': 'N/A','telefono': 88888888,'email': 'admin.example@email.com','direccion': 'No Aplica','activo': 1 })
            rsp_empleado = requests.get(url+'empleados/')
            data = rsp_empleado.json()
            empleado = data['empleados']
    try:
        if request.method == 'POST':
            idEmpleado = int(request.POST['idEmpleadl'])
            nombreUsuario = request.POST['username']
            password = request.POST['password']
            passwordc = request.POST['passwordc']
            activo = 1
            bloqueado = 0
            if password == passwordc: 
                response = requests.post(url+'usuarios/', json={'idEmpleado':idEmpleado, 'nombreUsuario': nombreUsuario, 'password': password,'passwordc':passwordc, 'activo': activo, 'bloqueado': bloqueado})
                userdata={}
                if response.status_code == 200:
                    userdata = response.json()
                    mensaje = userdata['message']
                    if mensaje != 'Registro Exitoso.':
                        logger = definir_log_info('crear_login','logs_login')
                        logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                    else:
                        logger = definir_log_info('crear_login','logs_login')
                        logger.debug(f"Se ha realizado un registro")
                    return render(request, 'presentacion/usuariosignup.html', {'mensaje': mensaje,  'empleado': empleado})
                else:
                    mensaje = userdata['usuariosr']
                    logger = definir_log_info('crear_login','logs_login')
                    logger.warning("No se pudo realizar el registro" + mensaje)
                    return render(request, 'presentacion/usuariosignup.html', {'mensaje': mensaje,  'empleado': empleado})
            else:
                mensaje = 'Las contraseñas no coinciden'
                logger = definir_log_info('crear_login','logs_login')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'presentacion/usuariosignup.html', {'mensaje': mensaje,'empleado': empleado}) 
        else:
            logger = definir_log_info('crear_login','logs_login')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'presentacion/usuariosignup.html', { 'empleado': empleado})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_login','logs_login')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'presentacion/usuariosignup.html', { 'empleado': empleado})