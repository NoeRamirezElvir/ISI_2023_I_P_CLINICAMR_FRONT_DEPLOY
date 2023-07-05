from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_examenes(request):
    response = requests.get(url+'examen/')
    if response.status_code == 200:
        data = response.json()
        examenes = data['examenes']
    else:
        examenes = []
    context = {'examenes': examenes}
    return render(request, 'examen/buscar_examen.html', context)

def crear_examenes(request):
    muestras_list = list_muestras()
    tipo_list = list_tipos()
    laboratorios_list = list_laboratorios()

    try:
        if request.method == 'POST':
            idMuestra = int(request.POST['idMuestra'])
            idTipo = int(request.POST['idTipo'])
            fechaProgramada = request.POST['fechaProgramada']
            observacion = request.POST['observacion']
            idLaboratorio = int(request.POST['idLaboratorio'])
            registro_temp = {'idMuestra': idMuestra, 'idTipo': idTipo, 'fechaProgramada': fechaProgramada, 'observacion':observacion, 'idLaboratorio':idLaboratorio}
            response = requests.post(url+'examen/', json={'idMuestra': idMuestra, 'idTipo': idTipo, 'fechaProgramada': fechaProgramada, 'observacion':observacion, 'idLaboratorio':idLaboratorio})
            data = response.json()
            if response.status_code == 200:
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_examen','logs_examen')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_examen','logs_examen')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'examen/examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_examen','logs_examen')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'examen/examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
        else:
            logger = definir_log_info('crear_examen','logs_examen')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'examen/examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_examen','logs_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'examen/examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
   
def abrir_actualizar_examenes(request):
    muestras_list = list_muestras()
    tipo_list = list_tipos()
    laboratorios_list = list_laboratorios()
    try:
        if request.method == 'POST':
            resp = requests.get(url+'examen/busqueda/id/'+str(request.POST['id_examenes']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                examenes = data['examenes']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_examen','logs_examen')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_examen','logs_examen')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                examenes = []
                logger = definir_log_info('abrir_actualizar_examen','logs_examen')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje':mensaje,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list}
            mensaje = data['message']
            return render(request, 'examen/actualizar_examen.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_examen','logs_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        examenes = []
        context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje':mensaje,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list}
        return render(request, 'examen/actualizar_examen.html', context)

def actualizar_examenes(request, id):
    muestras_list = list_muestras()
    tipo_list = list_tipos()
    laboratorios_list = list_laboratorios()
    try:
        if request.method == 'POST':
            idTemporal = id
            idMuestra = int(request.POST['idMuestra'])
            idTipo = int(request.POST['idTipo'])
            fechaProgramada = request.POST['fechaProgramada']
            observacion = request.POST['observacion']
            idLaboratorio = int(request.POST['idLaboratorio'])
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'examen/id/{idTemporal}', json={'idMuestra': idMuestra, 'idTipo': idTipo, 'fechaProgramada': fechaProgramada, 'observacion':observacion, 'idLaboratorio':idLaboratorio})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'examen/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            examenes = data['examenes']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_examen','logs_examen')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'examen/actualizar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'examenes':examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
            else:
                mensaje = rsp['message']  
                logger = definir_log_info('actualizar_examen','logs_examen')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                          #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'examen/actualizar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'examenes':examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'examen/busqueda/id/{idTemporal}')
            data = response.json()
            if response.status_code == 200:
                examenes = data['examenes']
                mensaje = data['message']
                logger = definir_log_info('actualizar_examen','logs_examen')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'examen/actualizar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_examen','logs_examen')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'examen/actualizar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'examenes':examenes, 'muestras_list':muestras_list, 'tipo_list':tipo_list})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_examen','logs_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'examen/busqueda/id/{idTemporal}')
        data = response.json()
        if response.status_code == 200:
            examenes = data['examenes']
            mensaje = data['message']
            return render(request, 'examen/actualizar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
        else:
            mensaje = data['message']
            return render(request, 'examen/actualizar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'examenes':examenes, 'muestras_list':muestras_list, 'tipo_list':tipo_list})
    

def eliminar_examenes(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'examen/id/{idTemporal}')
            res = response.json()
            rsp_examenes = requests.get(url + 'examen/') 
            if rsp_examenes.status_code == 200:
                data = rsp_examenes.json()
                examenes = data['examenes']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_examen','logs_examen')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_examen','logs_examen')
                    logger.info("No se ha podido eliminar el registro")
            else:
                examenes = []
                logger = definir_log_info('eliminar_examen','logs_examen')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje': mensaje}
            return render(request, 'examen/buscar_examen.html', context) 
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_examen','logs_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_examenes = requests.get(url + 'examen/') 
        if rsp_examenes.status_code == 200:
            data = rsp_examenes.json()
            examenes = data['examenes']
        else:
            examenes = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'error': mensaje}
        return render(request, 'examen/buscar_examen.html', context) 

    
def buscar_examenes(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'examen/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['examenes']:
                    data = response.json()
                    mensaje = data['message']
                    examenes = {}
                    examenes = data['examenes']
                    if examenes != []:   
                        logger = definir_log_info('buscar_examen','logs_examen')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_examen','logs_examen')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje':mensaje}
                    return render(request, 'examen/buscar_examen.html', context)
                else:        
                    response = requests.get(url2+'documento/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        examenes = {}
                        examenes = data['examenes']
                        if examenes != []:   
                            logger = definir_log_info('buscar_examen','logs_examen')
                            logger.debug(f"Se obtuvieron los registros:Filtrado(documento){valor} - {mensaje}")
                        else:
                            logger = definir_log_info('buscar_examen','logs_examen')
                            logger.info(f"No se obtuvieron los registros:Filtrado(documento){valor} - {mensaje}")
                        context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje':mensaje}
                        return render(request, 'examen/buscar_examen.html', context)
                    else:
                        examenes = []
                        mensaje = 'No se encontraron muestras'
                        logger = definir_log_info('buscar_examen','logs_examen')
                        logger.info(f"No se obtuvieron los registros:Filtrado(documento){valor} - {mensaje}")
                        return render(request, 'examen/buscar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje': mensaje})
            else:
                response = requests.get(url2+'documento/'+valor)
                data = response.json()
                if data['examenes']:
                    data = response.json()
                    mensaje = data['message']
                    examenes = {}
                    examenes = data['examenes']
                    if examenes != []:   
                        logger = definir_log_info('buscar_examen','logs_examen')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(documento){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_examen','logs_examen')
                        logger.info(f"No se obtuvieron los registros:Filtrado(documento){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje':mensaje}
                    return render(request, 'examen/buscar_examen.html', context)
                else:        
                    response = requests.get(url2+'nombre/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        examenes = {}
                        examenes = data['examenes']
                        if examenes != []:   
                            logger = definir_log_info('buscar_examen','logs_examen')
                            logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                        else:
                            logger = definir_log_info('buscar_examen','logs_examen')
                            logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                            context = {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje':mensaje}
                        return render(request, 'examen/buscar_examen.html', context)
                    else:
                        examenes = []
                        mensaje = 'No se encontraron muestras'
                        logger = definir_log_info('buscar_examen','logs_examen')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                        return render(request, 'examen/buscar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje': mensaje})
        else:
            response = requests.get(url+'examen/')
            if response.status_code == 200:
                data = response.json()
                examenes = data['examenes']
                mensaje = data['message']   
                if examenes != []:   
                    logger = definir_log_info('buscar_examen','logs_examen')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_examen','logs_examen')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'examen/buscar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje': mensaje})
            else:
                examenes = []
                mensaje = 'No se encontraron muestras'
                logger = definir_log_info('buscar_examen','logs_examen')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'examen/buscar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_examen','logs_examen')
        logger.exception("Ocurrio una excepcion:" + str(e))
        examenes = []
        return render(request, 'examen/buscar_examen.html', {'reportes_lista':DatosReportes.cargar_lista_examen(),'reportes_usuarios':DatosReportes.cargar_usuario(),'examenes': examenes, 'mensaje': mensaje})
   

def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/examen')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list

def list_muestras():
    rsp_muestra= requests.get(url+'muestras/')
    if rsp_muestra.status_code == 200:
        data = rsp_muestra.json()
        muestras_list = data['muestras']
        return muestras_list
    else:
        muestras_list = []
        return muestras_list
    
def list_laboratorios():
    rsp_laboratorios= requests.get(url+'laboratorios/')
    if rsp_laboratorios.status_code == 200:
        data = rsp_laboratorios.json()
        laboratorios_list = data['laboratorios']
        return laboratorios_list
    else:
        laboratorios_list = []
        return laboratorios_list