import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
def eliminar_precio_historico_examen(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'precioHistoricoExamen/id/{idTemporal}')
            res = response.json()
            rsp_historicos = requests.get(url + 'precioHistoricoExamen/') 
            if rsp_historicos.status_code == 200:
                data = rsp_historicos.json()
                historicos = data['historicos']
                logger = definir_log_info('eliminar_precio_historico_examen','logs_precio_historico_examen')
                logger.debug(f"Se obtuvieron los registros") 
            else:
                historicos = []
                logger = definir_log_info('eliminar_precio_historico_examen','logs_precio_historico_examen')
                logger.debug(f"No se obtuvieron los registros") 
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje}
            return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)     
    except Exception as e:
        logger = definir_log_info('excepcion_eliminar_precio_historico_examen','logs_precio_historico_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_historicos = requests.get(url + 'precioHistoricoExamen/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
            logger = definir_log_info('eliminar_precio_historico_examen','logs_precio_historico_examen')
            logger.debug(f"Se obtuvieron los registros") 
        else:
            historicos = []
            logger = definir_log_info('eliminar_precio_historico_examen','logs_precio_historico_examen')
            logger.debug(f"No se obtuvieron los registros") 
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'error': mensaje}
        return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)     
    
def buscar_precio_historico_examen(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'precioHistoricoExamen/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
                    logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}") 
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)       
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de examenes'
                    logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
                    logger.debug(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}") 
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})

            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
                    logger.debug(f"Se obtuvieron los registros:Filtrado(Nombre){valor} - {mensaje}") 
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de examenes'
                    logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
                    logger.debug(f"No se obtuvieron los registros:Filtrado(Nombre){valor} - {mensaje}") 
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'precioHistoricoExamen/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
                logger.debug(f"Se obtuvieron los registros - {mensaje}") 
                return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón historicos de examenes'
                logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
                logger.debug(f"No se obtuvieron los registros: {mensaje}") 
            return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_buscar_precio_historico_examen','logs_precio_historico_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'precioHistoricoExamen/')
        if response.status_code == 200:
            data = response.json()
            historicos = data['historicos']
            mensaje = data['message']   
            return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
        else:
            historicos = []
            mensaje = 'No se encontrarón historicos de examenes'
            logger = definir_log_info('buscar_precio_historico_examen','logs_precio_historico_examen')
            logger.debug(f"No se obtuvieron los registros: {mensaje}") 
        return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'reportes_lista':DatosReportes.cargar_lista_historico_precio_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})