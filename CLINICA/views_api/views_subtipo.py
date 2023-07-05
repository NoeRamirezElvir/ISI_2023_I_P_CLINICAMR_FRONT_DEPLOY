from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_subtipo(request):
    response = requests.get(url+'subtipo/')
    if response.status_code == 200:
        data = response.json()
        subtipo = data['subtipo']
    else:
        subtipo = []
    context = {'subtipo': subtipo}
    return render(request, 'SubTipo/subtipo.html', context)

def crear_subtipo(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            activo = int(request.POST['payment_method'])

            registro_temp={'nombre': nombre,  'activo': activo}
            response = requests.post(url+'subtipo/', json={'nombre': nombre,  'activo': activo})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_subtipo','logs_subtipo')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_subtipo','logs_subtipo')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'SubTipo/subtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_subtipo','logs_subtipo')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'SubTipo/subtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_subtipo','logs_subtipo')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'SubTipo/subtipo.html',{'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_subtipo','logs_subtipo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'SubTipo/subtipo.html',{'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    

def abrir_actualizar_subtipo(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'subtipo/busqueda/id/'+str(request.POST['id_subtipo']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                subtipo = data['subtipo']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_subtipo','logs_subtipo')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_subtipo','logs_subtipo')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                subtipo = []
                logger = definir_log_info('abrir_actualizar_subtipo','logs_subtipo')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'SubTipo/subtipoActualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_subtipo','logs_subtipo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        subtipo = []
        context = {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje':mensaje}
        return render(request, 'SubTipo/subtipoActualizar.html', context)
    
def actualizar_subtipo(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            
            activo = int(request.POST['payment_method'])
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'subtipo/id/{idTemporal}', json={'nombre': nombre,  'activo': activo})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el subtipo relacionado con el id
            res = requests.get(url+f'subtipo/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            subtipo = data['subtipo']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_subtipo','logs_subtipo')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'SubTipo/subtipoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'subtipo':subtipo })
            else:
                mensaje = rsp['message']   
                logger = definir_log_info('actualizar_subtipo','logs_subtipo')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                         #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'SubTipo/subtipoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'subtipo':subtipo})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'subtipo/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                subtipo = data['subtipo']
                mensaje = data['message']
                logger = definir_log_info('actualizar_subtipo','logs_subtipo')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'SubTipo/subtipoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_subtipo','logs_subtipo')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'SubTipo/subtipoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'subtipo':subtipo})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_subtipo','logs_subtipo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        mensaje = data['message']
        return render(request, 'SubTipo/subtipoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'subtipo':{}})
    

def eliminar_subtipo(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'subtipo/id/{idTemporal}')
            res = response.json()
            rsp_subtipo = requests.get(url + 'subtipo/') 
            if rsp_subtipo.status_code == 200:
                data = rsp_subtipo.json()
                subtipo = data['subtipo']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_subtipo','logs_subtipo')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_subtipo','logs_subtipo')
                    logger.info("No se ha podido eliminar el registro")
            else:
                subtipo = []
                logger = definir_log_info('eliminar_subtipo','logs_subtipo')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje': mensaje}
            return render(request, 'SubTipo/buscarsubtipo.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_subtipo','logs_subtipo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_subtipo = requests.get(url + 'subtipo/') 
        if rsp_subtipo.status_code == 200:
            data = rsp_subtipo.json()
            subtipo = data['subtipo']
        else:
            subtipo = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'error': mensaje}
        return render(request, 'SubTipo/buscarsubtipo.html', context)     
       
def buscar_subtipo(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'subtipo/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    subtipo = {}
                    subtipo = data['subtipo']
                    if subtipo != []:   
                        logger = definir_log_info('buscar_subtipo','logs_subtipo')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_subtipo','logs_subtipo')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje':mensaje}
                    return render(request, 'SubTipo/buscarsubtipo.html', context)
                else:
                    subtipo = []
                    mensaje = 'No se encontraron subtipo'
                    logger = definir_log_info('buscar_subtipo','logs_subtipo')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'SubTipo/buscarsubtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje': mensaje})
           
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    subtipo = {}
                    subtipo = data['subtipo']
                    if subtipo != []:   
                        logger = definir_log_info('buscar_subtipo','logs_subtipo')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_subtipo','logs_subtipo')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje':mensaje}
                    return render(request, 'SubTipo/buscarsubtipo.html', context)
                else:
                    subtipo = []
                    mensaje = 'No se encontraron subtipo'
                    logger = definir_log_info('buscar_subtipo','logs_subtipo')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'SubTipo/buscarsubtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'subtipo/')
            if response.status_code == 200:
                data = response.json()
                subtipo = data['subtipo']
                mensaje = data['message']   
                if subtipo != []:   
                    logger = definir_log_info('buscar_subtipo','logs_subtipo')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_subtipo','logs_subtipo')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'SubTipo/buscarsubtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje': mensaje})
            else:
                subtipo = []
                mensaje = 'No se encontraron subtipo'
                logger = definir_log_info('buscar_subtipo','logs_subtipo')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'SubTipo/buscarsubtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_subtipo','logs_subtipo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        subtipo = []
        return render(request, 'SubTipo/buscarsubtipo.html', {'reportes_lista':DatosReportes.cargar_lista_subtipo(),'reportes_usuarios':DatosReportes.cargar_usuario(),'subtipo': subtipo, 'mensaje': mensaje})
    