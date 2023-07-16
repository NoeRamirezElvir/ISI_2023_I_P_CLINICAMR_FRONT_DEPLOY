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
def eliminar_costo_historico_medicamento(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'costoHistoricoMedicamento/id/{idTemporal}')
            res = response.json()
            rsp_historicos = requests.get(url + 'costoHistoricoMedicamento/') 
            if rsp_historicos.status_code == 200:
                data = rsp_historicos.json()
                historicos = data['historicos']
                logger = definir_log_info('eliminar_costo_historico_medicamento','logs_costo_historico_medicamento')
                logger.debug(f"Se elimino el registro: {id}") 
            else:
                historicos = []
                logger = definir_log_info('eliminar_costo_historico_medicamento','logs_costo_historico_medicamento')
                logger.info(f"No se elimino el registro: {id}") 
            mensaje = res['message']
            context = {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()}
            return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)     
    except:
        rsp_historicos = requests.get(url + 'costoHistoricoMedicamento/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
            logger = definir_log_info('eliminar_costo_historico_medicamento','logs_costo_historico_medicamento')
            logger.info(f"Se obtuvo la lista de registros") 
        else:
            historicos = []
            logger = definir_log_info('eliminar_costo_historico_medicamento','logs_costo_historico_medicamento')
            logger.info(f"No se obtuvo la lista de registros") 
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'historicos': historicos, 'error': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()}
        return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)     
    

def buscar_costo_historico_medicamento(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'costoHistoricoMedicamento/busqueda/'
        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
                    logger.debug(f"Se obtuvo la lista de registros: Filtrado(ID) {mensaje}")  
                    context = {'historicos': historicos, 'mensaje':mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()}
                    return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)       
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos'
                    logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
                    logger.info(f"No se obtuvo la lista de registros: {mensaje}")  
                    return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()})

            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
                    logger.debug(f"Se obtuvo la lista de registros: Filtrado(Nombre) {mensaje}")  
                    context = {'historicos': historicos, 'mensaje':mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()}
                    return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos'
                    logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
                    logger.info(f"No se obtuvo la lista de registros: {mensaje}")  
                    return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()})

        else:
            response = requests.get(url+'costoHistoricoMedicamento/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message'] 
                logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
                logger.debug(f"Se obtuvo la lista de registros: {mensaje}")  
                return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()})
            else:
                historicos = []
                mensaje = 'No se encontrarón historicos'
                logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
                logger.info(f"No se obtuvo la lista de registros: {mensaje}") 
            return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()})
    except Exception as e:
        logger = definir_log_info('buscar_costo_historico_medicamento','logs_costo_historico_medicamento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'costoHistoricoMedicamento/')
        if response.status_code == 200:
            data = response.json()
            historicos = data['historicos']
            mensaje = data['message']   
            return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()})
        else:
            historicos = []
            mensaje = 'No se encontrarón historicos'
        return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje,'reportes_usuarios':DatosReportes.cargar_usuario(),'datos_permisos':cargar_datos(),'reportes_lista':DatosReportes.cargar_lista_costo_historico_medicamento()})
     