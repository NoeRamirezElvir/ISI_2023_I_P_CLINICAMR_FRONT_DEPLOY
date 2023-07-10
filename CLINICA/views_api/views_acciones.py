from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_acciones(request):
    response = requests.get(url+'acciones/')
    if response.status_code == 200:
        data = response.json()
        acciones = data['acciones']
        if not acciones:
            acciones = []
    else:
        acciones = []
    context = {'acciones': acciones}
    return render(request, 'acciones/Buscar_acciones.html', context)


def crear_acciones(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            registro_temp={'nombre': nombre, 'descripcion': descripcion}
            response = requests.post(url+'acciones/', json={'nombre': nombre, 'descripcion': descripcion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_acciones','logs_acciones')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_acciones','logs_acciones')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'acciones/acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_acciones','logs_acciones')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'acciones/acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_acciones','logs_acciones')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'acciones/acciones.html',{'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_acciones','logs_acciones')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'acciones/acciones.html',{'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje':mensaje})
    

def abrir_actualizar_acciones(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'acciones/busqueda/id/'+str(request.POST['id_acciones']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                acciones = data['acciones']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_acciones','logs_acciones')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_acciones','logs_acciones')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                acciones = []
                logger = definir_log_info('abrir_actualizar_acciones','logs_acciones')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'acciones/acciones_Actualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_acciones','logs_acciones')
        logger.exception("Ocurrio una excepcion:" + str(e))
        acciones = []
        context = {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje':mensaje}
        return render(request, 'acciones/acciones_Actualizar.html', context)

def actualizar_acciones(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'acciones/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'acciones/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            acciones = data['acciones']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_acciones','logs_acciones')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'acciones/acciones_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'acciones':acciones })
            else:
                mensaje = rsp['message']   
                logger = definir_log_info('actualizar_acciones','logs_acciones')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'acciones/acciones_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'acciones':acciones})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'acciones/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                usuario = data['acciones']
                mensaje = data['message']
                logger = definir_log_info('actualizar_acciones','logs_acciones')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'acciones/acciones_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_acciones','logs_acciones')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'acciones/acciones_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'acciones':acciones})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_acciones','logs_acciones')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'acciones/acciones_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'acciones':acciones})
       
def eliminar_acciones(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'acciones/id/{idTemporal}')
            res = response.json()
            rsp_acciones = requests.get(url + 'acciones/') 
            if rsp_acciones.status_code == 200:
                data = rsp_acciones.json()
                acciones = data['acciones']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_acciones','logs_acciones')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_acciones','logs_acciones')
                    logger.info("No se ha podido eliminar el registro")
            else:
                acciones = []
                logger = definir_log_info('eliminar_acciones','logs_acciones')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje': mensaje}
            return render(request, 'acciones/Buscar_acciones.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_acciones','logs_acciones')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_acciones = requests.get(url + 'acciones/') 
        if rsp_acciones.status_code == 200:
            data = rsp_acciones.json()
            acciones = data['acciones']
        else:
            acciones = []
        mensaje += ' No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'error': mensaje}
        return render(request, 'acciones/Buscar_acciones.html', context)     

def buscar_acciones(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'acciones/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    acciones = {}
                    acciones = data['acciones']
                    if acciones != []:   
                        logger = definir_log_info('buscar_acciones','logs_acciones')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_acciones','logs_acciones')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje':mensaje}
                    return render(request, 'acciones/Buscar_acciones.html', context)     
                else:
                    acciones = []
                    mensaje = 'No se encontraron acciones'
                    logger = definir_log_info('buscar_acciones','logs_acciones')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'acciones/Buscar_acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje': mensaje})  
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    acciones = {}
                    acciones = data['acciones']
                    if acciones != []:   
                        logger = definir_log_info('buscar_acciones','logs_acciones')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_acciones','logs_acciones')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje':mensaje}
                    return render(request, 'acciones/Buscar_acciones.html', context)
                else:
                    acciones = []
                    mensaje = 'No se encontraron acciones'
                    logger = definir_log_info('buscar_acciones','logs_acciones')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'acciones/Buscar_acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'acciones/')
            if response.status_code == 200:
                data = response.json()
                acciones = data['acciones']
                mensaje = data['message']   
                if acciones != []:   
                    logger = definir_log_info('buscar_acciones','logs_acciones')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_acciones','logs_acciones')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'acciones/Buscar_acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje': mensaje})
            else:
                acciones = []
                mensaje = 'No se encontraron acciones'
                logger = definir_log_info('buscar_acciones','logs_acciones')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'acciones/Buscar_acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_acciones','logs_acciones')
        logger.exception("Ocurrio una excepcion:" + str(e))
        acciones = []
        return render(request, 'acciones/Buscar_acciones.html', {'reportes_lista':DatosReportes.cargar_lista_acciones(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones': acciones, 'mensaje': mensaje})
   