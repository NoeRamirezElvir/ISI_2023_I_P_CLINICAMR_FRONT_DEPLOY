from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_resultados(request):
    response = requests.get(url+'resultados/')
    if response.status_code == 200:
        data = response.json()
        resultados = data['resultados']
    else:
        resultados = []
    context = {'resultados': resultados}
    return render(request, 'Resultados/BuscarResultados.html', context)

def crear_resultados(request):
    tratamiento_list = list_tratamiento()
    try:
        if request.method == 'POST':
            idTratamiento = int(request.POST['idTratamiento'])      
            fecha = request.POST['fecha']
            observacion = request.POST['observacion']       
            registro_temp = {'idTratamiento': idTratamiento, 'fecha': fecha, 'observacion': observacion}
            response = requests.post(url+'resultados/', json={'idTratamiento': idTratamiento, 'fecha': fecha, 'observacion': observacion})
            data = response.json()      
            if response.status_code == 200:
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_resultados','logs_resultados')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_resultados','logs_resultados')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp,'tratamiento_list':tratamiento_list})
                
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_resultados','logs_resultados')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'tratamiento_list':tratamiento_list})
        else:
            logger = definir_log_info('crear_resultados','logs_resultados')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tratamiento_list':tratamiento_list})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_resultados','logs_resultados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tratamiento_list':tratamiento_list})
   

def abrir_actualizar_resultados(request):
    tratamiento_list = list_tratamiento()
    try:
        if request.method == 'POST':
            print(request.POST['id_resultados'])
            resp = requests.get(url+'resultados/busqueda/id/'+str(request.POST['id_resultados']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                resultados = data['resultados']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_resultados','logs_resultados')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_resultados','logs_resultados')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                resultados = []
                logger = definir_log_info('abrir_actualizar_resultados','logs_resultados')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje,'tratamiento_list':tratamiento_list}
            mensaje = data['message']
            return render(request, 'Resultados/ActualizarResultados.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_resultados','logs_resultados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        resultados = []
        context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje,'tratamiento_list':tratamiento_list}
        return render(request, 'Resultados/ActualizarResultados.html', context)
    

def actualizar_resultados(request, id):
    tratamiento_list = list_tratamiento()
    try:
        if request.method == 'POST':
            idTemporal = id
            idTratamiento = int(request.POST['idTratamiento'])
            
            fecha = request.POST['fecha']
            observacion = request.POST['observacion']
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'resultados/id/{idTemporal}', json={'idTratamiento': idTratamiento,'fecha': fecha, 'observacion':observacion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'resultados/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            resultados = data['resultados']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_resultados','logs_resultados')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':resultados,'tratamiento_list':tratamiento_list})
            else:
                mensaje = rsp['message']
                logger = definir_log_info('actualizar_resultados','logs_resultados')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':resultados,'tratamiento_list':tratamiento_list})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'resultados/busqueda/id/{idTemporal}')
            data = response.json()
            if response.status_code == 200:
                resultados = data['resultados']
                mensaje = data['message']
                logger = definir_log_info('actualizar_resultados','logs_resultados')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados,'tratamiento_list':tratamiento_list})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_resultados','logs_resultados')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':resultados, 'tratamiento_list':tratamiento_list})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_resultados','logs_resultados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        mensaje = data['message']
        return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':[], 'tratamiento_list':tratamiento_list})
    


def eliminar_resultados(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'resultados/id/{idTemporal}')
            res = response.json()
            rsp_resultados = requests.get(url + 'resultados/') 
            if rsp_resultados.status_code == 200:
                data = rsp_resultados.json()
                resultados = data['resultados']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_resultados','logs_resultados')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_resultados','logs_resultados')
                    logger.info("No se ha podido eliminar el registro")
            else:
                resultados = []
                logger = definir_log_info('eliminar_resultados','logs_resultados')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje}
            return render(request, 'Resultados/BuscarResultados.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_resultados','logs_resultados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_resultados = requests.get(url + 'resultados/') 
        if rsp_resultados.status_code == 200:
            data = rsp_resultados.json()
            resultados = data['resultados']
        else:
            resultados = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'error': mensaje}
        return render(request, 'Resultados/BuscarResultados.html', context)     
   
def buscar_resultados(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'resultados/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['resultados']:
                    data = response.json()
                    mensaje = data['message']
                    resultados = {}
                    resultados = data['resultados']
                    if resultados != []:   
                        logger = definir_log_info('buscar_resultados','logs_resultados')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_resultados','logs_resultados')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje}
                    return render(request, 'Resultados/BuscarResultados.html', context) 
                else:
                    resultados = []
                    mensaje = 'No se encontraron resultados'
                    logger = definir_log_info('buscar_resultados','logs_resultados')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})

                
            else:        
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    resultados = {}
                    resultados = data['resultados']
                    if resultados != []:   
                        logger = definir_log_info('buscar_resultados','logs_resultados')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_resultados','logs_resultados')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje}
                    return render(request, 'Resultados/BuscarResultados.html', context)
                else:
                    resultados = []
                    mensaje = 'No se encontraron resultados'
                    logger = definir_log_info('buscar_resultados','logs_resultados')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})

        else:
            response = requests.get(url+'resultados/')
            if response.status_code == 200:
                data = response.json()
                resultados = data['resultados']
                mensaje = data['message']   
                if resultados != []:   
                    logger = definir_log_info('buscar_resultados','logs_resultados')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_resultados','logs_resultados')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})
            else:
                resultados = []
                mensaje = 'No se encontraron resultados'
                logger = definir_log_info('buscar_resultados','logs_resultados')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_resultados','logs_resultados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        resultados = []
        return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})
   

def list_tratamiento():
    rsp_tratamientos = requests.get(url+'tratamientos/')
    if rsp_tratamientos.status_code == 200:
        data = rsp_tratamientos.json()
        tratamientos_list = data['tratamientos']
        return tratamientos_list
    else:
        tratamientos_list = []
        return tratamientos_list


    
