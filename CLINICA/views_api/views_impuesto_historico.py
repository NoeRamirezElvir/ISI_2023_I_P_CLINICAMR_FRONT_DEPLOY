import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info


url = 'https://clinicamr.onrender.com/api/'
def eliminar_impuesto_historico(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'impuestoHistorico/id/{idTemporal}')
            res = response.json()
            rsp_pacientes = requests.get(url + 'impuestoHistorico/') 
            if rsp_pacientes.status_code == 200:
                data = rsp_pacientes.json()
                historicos = data['historicos']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_historico_impuesto','logs_historico_impuesto')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_historico_impuesto','logs_historico_impuesto')
                    logger.info("No se ha podido eliminar el registro")
            else:
                historicos = []
            mensaje = res['message']
            logger = definir_log_info('eliminar_historico_impuesto','logs_historico_impuesto')
            logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje}
            return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_historico_impuesto','logs_historico_impuesto')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_pacientes = requests.get(url + 'impuestoHistorico/') 
        if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            historicos = data['historicos']
        else:
            historicos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'error': mensaje}
        return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)     
   
def buscar_impuesto_historico(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'impuestoHistorico/busqueda/'

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
                        logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón citas'
                    logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
              
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    if historicos != []:   
                        logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón citas'
                    logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
        else:
            response = requests.get(url+'impuestoHistorico/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                if historicos != []:   
                    logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón citas'
                logger = definir_log_info('buscar_historico_impuesto','logs_historico_impuesto')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_historico_impuesto','logs_historico_impuesto')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'impuestoHistorico/')
        if response.status_code == 200:
            data = response.json()
            historicos = data['historicos']
            mensaje = data['message']   
            return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
        else:
            historicos = []
            mensaje = 'No se encontrarón citas'
        return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'reportes_lista':DatosReportes.cargar_lista_historico_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'historicos': historicos, 'mensaje': mensaje})
    