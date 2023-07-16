import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos



url = 'https://clinicamr.onrender.com/api/'
#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
def eliminar_precio_historico_medicamento(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'precioHistoricoMedicamento/id/{idTemporal}')
            res = response.json()
            rsp_historicos = requests.get(url + 'precioHistoricoMedicamento/') 
            if rsp_historicos.status_code == 200:
                data = rsp_historicos.json()
                historicos = data['historicos']
                logger = definir_log_info('eliminar_precio_historico_medicamento','logs_precio_historico_medicamento')
                logger.info(f"Se elimino un registro: {id}") 
            else:
                historicos = []
                logger = definir_log_info('eliminar_precio_historico_medicamento','logs_precio_historico_medicamento')
                logger.info(f"No se elimino el registro: {id}") 
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje}
            return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', context)     
    except Exception as e:
        rsp_historicos = requests.get(url + 'precioHistoricoMedicamento/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
            logger = definir_log_info('eliminar_precio_historico_medicamento','logs_precio_historico_medicamento')
            logger.info(f"Se obtuvieron los registros")  
        else:
            historicos = []
            logger = definir_log_info('eliminar_precio_historico_medicamento','logs_precio_historico_medicamento')
            logger.info(f"No se obtuvieron los registros")  
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'error': mensaje}
        logger = definir_log_info('eliminar_precio_historico_medicamento','logs_precio_historico_medicamento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', context)     

def buscar_precio_historico_medicamento(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'precioHistoricoMedicamento/busqueda/'
        #raise Exception('Error')
        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
                    logger.debug(f"Se obtuvieron los registros: Filtrado(ID)({valor}) - {mensaje}") 
                    context = {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', context)       
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos'
                    logger = definir_log_info('buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
                    logger.info(f"No se obtuvieron los registros: {mensaje}")  
                    return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})

            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
                    logger.debug(f"Se obtuvieron los registros: Filtrado(Nombre):({valor}) - {mensaje}") 
                    context = {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos'
                    logger = definir_log_info('buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
                    logger.info(f"No se obtuvieron los registros: {mensaje}")  
                    return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'precioHistoricoMedicamento/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                logger = definir_log_info('buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
                logger.debug(f"Se obtuvieron los registros: {mensaje}") 
                return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón historicos'
                logger = definir_log_info('buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
                logger.info(f"No se obtuvieron los registros: {mensaje}")  
            return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_buscar_precio_historico_medicamento','logs_precio_historico_medicamento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'precioHistoricoMedicamento/')
        if response.status_code == 200:
            data = response.json()
            historicos = data['historicos']
            mensaje = data['message']   
            return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
        else:
            historicos = []
            mensaje = 'No se encontrarón historicos'     
        return render(request, 'precio_historico_medicamento/buscar_precio_historico_medicamento.html', {'reportes_lista':DatosReportes.cargar_lista_precio_historico_medicamento(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})