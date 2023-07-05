import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
def eliminar_precio_historico_tratamiento(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'precioHistoricoTratamiento/id/{idTemporal}')
            res = response.json()
            rsp_historicos = requests.get(url + 'precioHistoricoTratamiento/') 
            if rsp_historicos.status_code == 200:
                data = rsp_historicos.json()
                historicos = data['historicos']
                logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                logger.debug(f"Se obtuvieron los registros") 

            else:
                historicos = []
                logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                logger.info(f"No se obtuvieron los registros")
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje}
            return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', context)     
    except Exception as e:
        logger = definir_log_info('excepcion_eliminar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
        logger.exception("Ocurrio una excepcion:" + str(e))

        rsp_historicos = requests.get(url + 'precioHistoricoTratamiento/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
            logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
            logger.debug(f"Se obtuvieron los registros")
        else:
            historicos = []
            logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
            logger.info(f"No se obtuvieron los registros")
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'error': mensaje}
        return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', context)     
    
def buscar_precio_historico_tratamiento(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'precioHistoricoTratamiento/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    if historicos != []:
                        logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                        logger.debug(f"Se obtuvieron los registros: Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                        logger.info(f"No se obtuvieron los registros: Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', context)       
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de tratamiento'
                    logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                    logger.info(f"No se obtuvieron los registros: Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})

            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de tratamiento'
                    logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                    return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'precioHistoricoTratamiento/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']  
                logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                logger.debug(f"Se obtuvieron los registros") 
                return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón historicos de tratamiento'
                logger = definir_log_info('buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
                logger.info(f"No se obtuvieron los registros")
            return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
        logger.exception("Ocurrio una excepcion:" + str(e))

        response = requests.get(url+'precioHistoricoTratamiento/')
        if response.status_code == 200:
            data = response.json()
            historicos = data['historicos']
            mensaje = data['message']   
            logger = definir_log_info('excepcion_buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
            logger.info(f"Se obtuvieron los registros:{mensaje}")
            return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
        else:
            historicos = []
            mensaje = 'No se encontrarón historicos de tratamiento'
            logger = definir_log_info('excepcion_buscar_precio_historico_tratamiento','logs_precio_historico_tratamiento')
            logger.info(f"No se obtuvieron los registros:{mensaje}")
        return render(request, 'precio_historico_tratamiento/buscar_precio_historico_tratamiento.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_tratamiento(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
