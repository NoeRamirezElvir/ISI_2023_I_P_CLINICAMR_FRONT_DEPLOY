from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def listar_autorizacion(request):
    response = requests.get(url+'autorizar/')
    if response.status_code == 200:
        data = response.json()
        autorizar = data['autorizar']
    else:
        autorizar = []
    context = {'autorizar': autorizar}
    return render(request, 'Autorizacion/Autorizar.html', context)

def crear_autorizacion(request):
    try:
        if request.method == 'POST':
            motivos = request.POST['motivos']        
            confirmacion = int(request.POST['payment_method'])

            registro_temp={'motivos': motivos, 'confirmacion': confirmacion}
            response = requests.post(url+'autorizar/', json={'motivos': motivos,  'confirmacion': confirmacion})
            data={}
            data = response.json()
            if response.status_code == 200:
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('error_crear','logs_autorizacion')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear','logs_autorizacion')
                    logger.debug(f"Se ha registrado un autorizacion: Motivos={motivos}")
                return render(request, 'Autorizacion/Autorizar.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_crear','logs_autorizacion')
                logger.warning("No se pudo crear el autorizacion: " + mensaje)
                return render(request, 'Autorizacion/Autorizar.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_autorizacion','logs_autorizacion')
            logger.debug('Entrando a la funcion crear autorizacion')
            return render(request, 'Autorizacion/Autorizar.html',{'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_autorizacion','logs_autorizacion')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Autorizacion/Autorizar.html',{'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def abrir_actualizar_autorizacion(request):
    try: 
        if request.method == 'POST':
            resp = requests.get(url+'autorizar/busqueda/id/'+str(request.POST['id_autorizar']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                autorizar = data['autorizar']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('error_abrir_actualizar','logs_autorizacion')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar','logs_autorizacion')
                    logger.debug("Se obtuvo el autorizacion correspondiente a la actualizacion: " + mensaje)
            else:
                autorizar = []
                logger = definir_log_info('error_abrir_actualizar','logs_autorizacion')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
            context = {'autorizar': autorizar, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            mensaje = data['message']
            return render(request, 'Autorizacion/Autorizaractualizar.html', context)
    except Exception as e:
        logger = definir_log_info('excepcion_autorizacion','logs_autorizacion')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'autorizar': autorizar, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'Autorizacion/Autorizaractualizar.html', context)


def actualizar_autorizacion(request, id):
    try:  
        if id == '':
            raise Exception("ID: esta vacio")       
        if request.method == 'POST':
            idTemporal = id
            motivos = request.POST['motivos']
            confirmacion = int(request.POST['payment_method'])
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'autorizar/id/{idTemporal}', json={'motivos': motivos,  'confirmacion': confirmacion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el autorizacion relacionado con el id
            res = requests.get(url+f'autorizar/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            autorizar = data['autorizar']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar','logs_autorizacion')
                logger.debug("Actualizacion correcta de la autorizacion: " + mensaje)
                return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar ,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                logger = definir_log_info('error_actualizar','logs_autorizacion')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'autorizar/busqueda/id/{idTemporal}')
            data = response.json()
            if response.status_code == 200:
                autorizar = data['autorizar']
                mensaje = data['message']
                logger = definir_log_info('actualizar','logs_autorizacion')
                logger.debug("Obteniendo informacion del autorizacion: " + mensaje)
                return render(request, 'Autorizacion/Autorizaractualizar.html', {'autorizar': autorizar,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_actualizar','logs_autorizacion')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})

    except Exception as e:
        logger = definir_log_info('excepcion_autorizacion','logs_autorizacion')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    


def eliminar_autorizacion(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'autorizar/id/{idTemporal}')
            res = response.json()
            rsp_autorizar = requests.get(url + 'autorizar/') 
            if rsp_autorizar.status_code == 200:
                data = rsp_autorizar.json()
                autorizar = data['autorizar']
                logger = definir_log_info('eliminar_autorizacion','logs_autorizacion')
                logger.info("autorizacion eliminado correctamente")
            else:
                autorizar = []
                logger = definir_log_info('error_eliminar_autorizacion','logs_autorizacion')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'autorizar': autorizar, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'Autorizacion/buscarAutorizar.html', context)
    except Exception as e:     
        rsp_autorizar = requests.get(url + 'autorizar/') 
        if rsp_autorizar.status_code == 200:
            data = rsp_autorizar.json()
            autorizar = data['autorizar']
        else:
            autorizar = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        logger = definir_log_info('excepcion_autorizacion','logs_autorizacion')
        logger.exception("Ocurrio una excepcion:" + str(mensaje))
        context = {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'Autorizacion/buscarAutorizar.html', context)     
    
def buscar_autorizacion(request):
    try:    
        
        valor = request.GET.get('buscador', None)
        url2 = url + 'autorizar/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    autorizar = {}
                    autorizar = data['autorizar']
                    logger = definir_log_info('buscar_autorizacion','logs_autorizacion')
                    logger.debug("Se obtuvo el autorizacion especifico(filtrado por ID): " + mensaje)
                    context = {'autorizar': autorizar, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'Autorizacion/buscarAutorizar.html', context)
                else:
                    autorizar = []
                    mensaje = 'No se encontraron Autorizaciones de pacientes'
                    logger = definir_log_info('error_buscar_autorizacion','logs_autorizacion')
                    logger.debug("No se obtuvo el autorizacion especifico(filtrado por ID): " + mensaje)
                    return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})    
            else:
                response = requests.get(url2+'motivos/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    autorizar = {}
                    autorizar = data['autorizar']
                    logger = definir_log_info('buscar_autorizacion','logs_autorizacion')
                    logger.debug("Se obtuvo el autorizacion especifico(filtrado por nombre): " + mensaje)
                    context = {'autorizar': autorizar, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'Autorizacion/buscarAutorizar.html', context)
                else:
                    autorizar = []
                    mensaje = 'No se encontraron Autorizaciones de pacientes'
                    logger = definir_log_info('error_buscar_autorizacion','logs_autorizacion')
                    logger.debug("No se obtuvo el autorizacion especifico(filtrado por ID): " + mensaje)
                    return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})    
        else:
            response = requests.get(url+'autorizar/')
            if response.status_code == 200:
                data = response.json()
                autorizar = data['autorizar']
                mensaje = data['message'] 
                logger = definir_log_info('buscar_autorizacion','logs_autorizacion')
                logger.debug("Se obtuvieron todos los autorizacions: " + mensaje )  
                return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                autorizar = []
                logger = definir_log_info('error_buscar_autorizacion','logs_autorizacion')
                logger.debug("No se obtuvo el autorizacion especifico(filtrado por ID): " + mensaje)
                mensaje = 'No se encontraron Autorizaciones de pacientes'
            return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
    except Exception as e:
        logger = definir_log_info('excepcion_autorizacion','logs_autorizacion')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'autorizacions/')
        if response.status_code == 200:
            data = response.json()
            autorizar = data['autorizar']
            mensaje = data['message']  
            logger = definir_log_info('buscar_autorizacion','logs_autorizacion')
            logger.debug("Se obtuvieron todos los autorizacions: " + mensaje ) 
            return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            autorizar = []
            mensaje = 'No se encontraron autorizacions'
            logger = definir_log_info('error_buscar_autorizacion','logs_autorizacion')
            logger.debug("No se pudo obtener informacion de autorizacions: " + mensaje)
        return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_autorizacion(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    