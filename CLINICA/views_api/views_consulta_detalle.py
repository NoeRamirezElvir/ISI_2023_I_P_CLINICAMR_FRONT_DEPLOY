import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes

from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def eliminar_detalle_consulta(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'consultaDetalle/id/{idTemporal}')
            res = response.json()
            rsp_detalles = requests.get(url + 'consultaDetalle/') 
            if rsp_detalles.status_code == 200:
                data = rsp_detalles.json()
                detalles = data['detalles']
                logger = definir_log_info('eliminar_detalle_consulta','logs_detalle_consulta')
                logger.info(f"Se elimino un detalle de consulta: ID {id}")
            else:
                detalles = []
                logger = definir_log_info('eliminar_detalle_consulta','logs_detalle_consulta')
                logger.info(f"No se pudo eliminar un detalle de consulta: ID {id}")
            mensaje = res['message']
            context = {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'detalle_consulta/buscar_detalle_consulta.html', context)     
    except Exception as e:
        rsp_detalles = requests.get(url + 'consultaDetalle/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'detalles': detalles, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        logger = definir_log_info('excepcion_detalle_consulta','logs_detalle_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'detalle_consulta/buscar_detalle_consulta.html', context)

def buscar_detalle_consulta(request):
    try: 
        valor = request.GET.get('buscador', None)
        url2 = url + 'consultaDetalle/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    logger = definir_log_info('buscar_detalle_consulta','logs_detalle_consulta')
                    logger.info(f"Se obtuvo el registro especifico(Filtrado por ID): {valor}")
                    context = {'detalles': detalles, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'detalle_consulta/buscar_detalle_consulta.html', context)
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_detalle_consulta','logs_detalle_consulta')
                    logger.info(f"No se encontro registro: {valor}, {mensaje}")
                    return render(request, 'detalle_consulta/buscar_detalle_consulta.html', {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})  
            else:
                response = requests.get(url2 + f'nombre/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    logger = definir_log_info('buscar_detalle_consulta','logs_detalle_consulta')
                    logger.info(f"Se obtuvo el registro especifico(Filtrado por Documento): {valor}")
                    context = {'detalles': detalles, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'detalle_consulta/buscar_detalle_consulta.html', context)   
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_detalle_consulta','logs_detalle_consulta')
                    logger.info(f"No se encontro registro: {valor}, {mensaje}")
                    return render(request, 'detalle_consulta/buscar_detalle_consulta.html', {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})  
        else:
            response = requests.get(url+'consultaDetalle/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']
                logger = definir_log_info('buscar_detalle_consulta','logs_detalle_consulta')
                logger.debug(f"Se obtuvieron los registros")  
                return render(request, 'detalle_consulta/buscar_detalle_consulta.html', {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
                logger = definir_log_info('buscar_detalle_consulta','logs_detalle_consulta')
                logger.info(f"Se obtuvieron los registros: {mensaje}")  
            return render(request, 'detalle_consulta/buscar_detalle_consulta.html', {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Error'
        logger = definir_log_info('excepcion_consulta','logs_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'consultaDetalle/')
        if response.status_code == 200:
            data = response.json()
            detalles = data['detalles']
            mensaje = data['message']   
            return render(request, 'detalle_consulta/buscar_detalle_consulta.html', {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            detalles = []
            mensaje = 'No se encontrarón registros'
        return render(request, 'detalle_consulta/buscar_detalle_consulta.html', {'detalles': detalles, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_detalle_consulta(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
