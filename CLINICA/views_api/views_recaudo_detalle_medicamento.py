import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def eliminar_recaudo_detalle_medicamento(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'recaudoDetalleMedicamento/id/{idTemporal}')
            res = response.json()
            rsp_detalles = requests.get(url + 'recaudoDetalleMedicamento/') 
            if rsp_detalles.status_code == 200:
                data = rsp_detalles.json()
                detalles = data['detalles']
                logger = definir_log_info('eliminar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                logger.debug(f"Se elimino el registro:{id}")
            else:
                detalles = []
                logger = definir_log_info('eliminar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                logger.debug(f"No se elimino el registro:{id}")
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje}
            return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', context)     
    except Exception as e: 
        logger = definir_log_info('excepcion_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_detalles = requests.get(url + 'recaudoDetalleMedicamento/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'error': mensaje}
        return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', context)     

    
def buscar_recaudo_detalle_medicamento(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'recaudoDetalleMedicamento/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit() and len(valor)<4:
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    if detalles != []:   
                        logger = definir_log_info('buscar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                        logger.debug(f"Se obtuvieron los registros:{mensaje}")
                    else:
                        logger = definir_log_info('buscar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                        logger.debug(f"No se obtuvieron los registros:{mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', context)
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                    logger.debug(f"No se obtuvieron los registros:{mensaje}")
                    return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})

            else:
                response = requests.get(url2 + f'numeroFactura/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    if detalles != []:   
                        logger = definir_log_info('buscar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                        logger.debug(f"Se obtuvieron los registros:{mensaje}")
                    else:
                        logger = definir_log_info('buscar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                        logger.debug(f"No se obtuvieron los registros:{mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', context)      
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
                    logger.debug(f"No se obtuvieron los registros:{mensaje}")
                    return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})

        else:
            response = requests.get(url+'recaudoDetalleMedicamento/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']   
                return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
            return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_recaudo_detalle_medicamento','logs_recaudo_detalle_medicamento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'recaudoDetalleMedicamento/')
        if response.status_code == 200:
            data = response.json()
            detalles = data['detalles']
            mensaje = data['message']   
            return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
        else:
            detalles = []
            mensaje = 'No se encontrarón registros'
        return render(request, 'recaudo_detalle_medicamento/buscar_recaudo_detalle_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
    