import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def eliminar_recaudo_detalle_examen(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'recaudoDetalleExamen/id/{idTemporal}')
            res = response.json()
            rsp_detalles = requests.get(url + 'recaudoDetalleExamen/') 
            if rsp_detalles.status_code == 200:
                data = rsp_detalles.json()
                detalles = data['detalles']
                logger = definir_log_info('eliminar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                logger.debug(f"Se elimino el registro:{id}")
            else:
                detalles = []
                logger = definir_log_info('eliminar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                logger.debug(f"No se elimino el registro:{id}")
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje}
            return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)     
    except Exception as e:
        logger = definir_log_info('excepcion_recaudo_detalle_examen','logs_recaudo_detalle_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))

        rsp_detalles = requests.get(url + 'recaudoDetalleExamen/') 
        if rsp_detalles.status_code == 200:
            data = rsp_detalles.json()
            detalles = data['detalles']
        else:
            detalles = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'error': mensaje}
        return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)     
    

def buscar_recaudo_detalle_examen(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'recaudoDetalleExamen/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                response = requests.get(url2 + f'id/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    if detalles != []:   
                        logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                        logger.debug(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                    logger.debug(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})

            else:
                response = requests.get(url2 + f'numeroFactura/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    detalles = {}
                    detalles = data['detalles']
                    if detalles != []:   
                        logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(Numero de Factura){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                        logger.debug(f"No se obtuvieron los registros:Filtrado(Numero de Factura){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje':mensaje}
                    return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', context)      
                else:
                    detalles = []
                    mensaje = 'No se encontrarón registros'
                    logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                    logger.debug(f"No se obtuvieron los registros:Filtrado(Numero de Factura){valor} - {mensaje}")
                    return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})

        else:
            response = requests.get(url+'recaudoDetalleExamen/')
            if response.status_code == 200:
                data = response.json()
                detalles = data['detalles']
                mensaje = data['message']
                if detalles != []:   
                    logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                    logger.debug(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
            else:
                detalles = []
                mensaje = 'No se encontrarón registros'
                logger = definir_log_info('buscar_recaudo_detalle_examen','logs_recaudo_detalle_examen')
                logger.debug(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_recaudo_detalle_examen','logs_recaudo_detalle_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'recaudoDetalleExamen/')
        if response.status_code == 200:
            data = response.json()
            detalles = data['detalles']
            mensaje = data['message']   
            return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
        else:
            detalles = []
            mensaje = 'No se encontrarón registros'
        return render(request, 'recaudo_detalle_examen/buscar_recaudo_detalle_examen.html', {'reportes_lista':DatosReportes.cargar_lista_detalle_recaudo_examen(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'detalles': detalles, 'mensaje': mensaje})
    