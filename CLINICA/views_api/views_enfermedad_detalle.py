import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info



url = 'https://clinicamr.onrender.com/api/'
def eliminar_enfermedad_detalle(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'enfermedadDetalle/id/{idTemporal}')
            res = response.json()
            rsp_detalles = requests.get(url + 'enfermedadDetalle/') 
            if rsp_detalles.status_code == 200:
                data = rsp_detalles.json()
                detalles = data['detalles']
                logger = definir_log_info('eliminar_detalle_enfermedad','logs_detalle_enfermedad')
                logger.debug(f"Se elimino el registro:{id}")
            else:
                detalles = []
                logger = definir_log_info('eliminar_detalle_enfermedad','logs_detalle_enfermedad')
                logger.info(f"No se elimino el registro:{id}")
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje}
            return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)     
    except Exception as e:
        logger = definir_log_info('excepcion_detalle_enfermedad','logs_detalle_enfermedad')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_detalles = requests.get(url + 'enfermedadDetalle/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'error': mensaje}
        return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)     

def buscar_enfermedad_detalle(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'enfermedadDetalle/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    if detalles != []:   
                        logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                response = requests.get(url2 + f'nombre/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    if detalles != []:   
                        logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(Nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                        logger.info(f"No se obtuvieron los registros:Filtrado(Nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', context)   
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                    logger.info(f"No se obtuvieron los registros:Filtrado(Nombre){valor} - {mensaje}")
                    return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
   
        else:
            response = requests.get(url+'enfermedadDetalle/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']
                if detalles != []:   
                    logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
                logger = definir_log_info('buscar_detalle_enfermedad','logs_detalle_enfermedad')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'enfermedadDetalle/')
        if response.status_code == 200:
            data = response.json()
            detalles = data['detalles']
            mensaje = data['message']   
            return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
        else:
            detalles = []
            mensaje = 'No se encontrarón registros'
        return render(request, 'enfermedad_detalle/buscar_enfermedad_detalle.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_enfermedad(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
    