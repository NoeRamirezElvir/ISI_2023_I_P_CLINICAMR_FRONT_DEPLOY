from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def listar_TipoMuestra(request):
    response = requests.get(url+'tmuestra/')
    if response.status_code == 200:
        data = response.json()
        tmuestra = data['tmuestra']
        if not tmuestra:
            tmuestra = []
    else:
        tmuestra = []
    context = {'tmuestra': tmuestra}
    return render(request, 'TipoMuestra/TMuestra.html ', context)


def crear_TipoMuestra(request):
    try:

        if request.method == 'POST':
            nombre = request.POST['nombre']
            metodoConservacion = request.POST['metodoConservacion']
            
            registro_temp={'nombre': nombre, 'metodoConservacion': metodoConservacion}
            response = requests.post(url+'tmuestra/', json={'nombre': nombre, 'metodoConservacion': metodoConservacion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_tipo_muestra','logs_tipo_muestra')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_tipo_muestra','logs_tipo_muestra')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'TipoMuestra/TMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_tipo_muestra','logs_tipo_muestra')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'TipoMuestra/TMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_tipo_muestra','logs_tipo_muestra')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'TipoMuestra/TMuestra.html',{'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_tipo_muestra','logs_tipo_muestra')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'TipoMuestra/TMuestra.html',{'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
            
def abrir_actualizar_TipoMuestra(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'tmuestra/busqueda/id/'+str(request.POST['id_tmuestra']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                tmuestra = data['tmuestra']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_tipo_muestra','logs_tipo_muestra')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_tipo_muestra','logs_tipo_muestra')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                tmuestra = []
                logger = definir_log_info('abrir_actualizar_tipo_muestra','logs_tipo_muestra')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'TipoMuestra/TMuestraActualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_tipo_muestra','logs_tipo_muestra')
        logger.exception("Ocurrio una excepcion:" + str(e))
        tmuestra = []
        context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
        return render(request, 'TipoMuestra/TMuestraActualizar.html', context)
   
def actualizar_TipoMuestra(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            metodoConservacion = request.POST['metodoConservacion']
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'tmuestra/id/{idTemporal}', json={'nombre': nombre, 'metodoConservacion': metodoConservacion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'tmuestra/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            tmuestra = data['tmuestra']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_tipo_muestra','logs_tipo_muestra')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':tmuestra })
            else:
                mensaje = rsp['message']   
                logger = definir_log_info('actualizar_tipo_muestra','logs_tipo_muestra')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                         #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':tmuestra})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'tmuestra/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                tmuestra = data['tmuestra']
                mensaje = data['message']
                logger = definir_log_info('actualizar_tipo_muestra','logs_tipo_muestra')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'TipoMuestra/TMuestraActualizar.html ', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_tipo_muestra','logs_tipo_muestra')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':tmuestra})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_tipo_muestra','logs_tipo_muestra')
        logger.exception("Ocurrio una excepcion:" + str(e))
        mensaje = data['message']
        return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':{}})
    
def eliminar_TipoMuestra(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'tmuestra/id/{idTemporal}')
            res = response.json()
            rsp_tmuestra = requests.get(url + 'tmuestra/') 
            if rsp_tmuestra.status_code == 200:
                data = rsp_tmuestra.json()
                tmuestra = data['tmuestra']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_tipo_muestra','logs_tipo_muestra')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_tipo_muestra','logs_tipo_muestra')
                    logger.info("No se ha podido eliminar el registro")
            else:
                tmuestra = []
                logger = definir_log_info('eliminar_tipo_muestra','logs_tipo_muestra')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje}
            return render(request, 'TipoMuestra/BuscarTMuestra.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_tipo_muestra','logs_tipo_muestra')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_tmuestra = requests.get(url + 'tmuestra/') 
        if rsp_tmuestra.status_code == 200:
            data = rsp_tmuestra.json()
            tmuestra = data['tmuestra']
        else:
            tmuestra = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'error': mensaje}
        return render(request, 'TipoMuestra/BuscarTMuestra.html', context)     
    
def buscar_TipoMuestra(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'tmuestra/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tmuestra = {}
                    tmuestra = data['tmuestra']
                    if tmuestra != []:   
                        logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', context) 
    
                else:
                    tmuestra = []
                    mensaje = 'No se encontraron Tipos de Muestra'
                    logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
    
                      
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tmuestra = {}
                    tmuestra = data['tmuestra']
                    if tmuestra != []:   
                        logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', context)
                else:
                    tmuestra = []
                    mensaje = 'No se encontraron Tipos de Muestra'
                    logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'tmuestra/')
            if response.status_code == 200:
                data = response.json()
                tmuestra = data['tmuestra']
                mensaje = data['message']  
                if tmuestra != []:   
                    logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                    logger.info(f"No se obtuvieron los registros:{mensaje}") 
                return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
            else:
                tmuestra = []
                mensaje = 'No se encontraron Tipos de Muestra'
                logger = definir_log_info('buscar_tipo_muestra','logs_tipo_muestra')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_tipo_muestra','logs_tipo_muestra')
        logger.exception("Ocurrio una excepcion:" + str(e))  
        tmuestra = []
        return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
   