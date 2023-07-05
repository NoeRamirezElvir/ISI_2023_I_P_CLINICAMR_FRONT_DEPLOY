from django.http import HttpResponse
import json
from django.shortcuts import render
import requests

from ..views_api.datos_reporte import DatosReportes

from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_cargos(request):
    response = requests.get(url+'cargos/')
    if response.status_code == 200:
        data = response.json()
        cargos = data['cargos']
    else:
        cargos = []
    context = {'cargos': cargos}
    return render(request, 'cargos/buscarCargo.html', context)

def crear_cargo(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            activo = int(request.POST['payment_method'])

            #raise Exception('Error')
            registro_temp={'nombre': nombre, 'descripcion': descripcion, 'activo': activo}
            response = requests.post(url+'cargos/', json={'nombre': nombre, 'descripcion': descripcion, 'activo': activo})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('error_crear','logs_cargo')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear','logs_cargo')
                    logger.debug(f"Se ha registrado un cargo: Nombre={nombre}")
                return render(request, 'cargos/cargo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_crear','logs_cargo')
                logger.warning("No se pudo crear el cargo: " + mensaje)
                return render(request, 'cargos/cargo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_cargo','logs_cargo')
            logger.debug('Entrando a la funcion crear cargo')
            return render(request, 'cargos/cargo.html',{'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_cargo','logs_cargo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'cargos/cargo.html',{'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})

def abrir_actualizar_cargos(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'cargos/busqueda/id/'+str(request.POST['id_cargo']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                cargos = data['cargos']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('error_abrir_actualizar','logs_cargo')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar','logs_cargo')
                    logger.debug("Se obtuvo el cargo correspondiente a la actualizacion: " + mensaje)
            else:
                cargos = []
                logger = definir_log_info('error_abrir_actualizar','logs_cargo')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
            context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            mensaje = data['message']
            return render(request, 'cargos/cargoactualizar.html', context)
    except Exception as e:
        logger = definir_log_info('excepcion_cargo','logs_cargo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'cargos/cargoactualizar.html', context)
    
def actualizar_cargo(request, id):
    try:
        if id == '':
            raise Exception("ID: esta vacio")
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            activo = int(request.POST['payment_method'])
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'cargos/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion, 'activo': activo})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'cargos/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            cargos = data['cargos']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar','logs_cargo')
                logger.debug("Actualizacion correcta del cargo: " + mensaje)
                return render(request, 'cargos/cargoactualizar.html', {'mensaje': mensaje,'cargos':cargos ,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = rsp['message']                           
                logger = definir_log_info('error_actualizar','logs_cargo')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'cargos/cargoactualizar.html', {'mensaje': mensaje,'cargos':cargos,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'cargos/busqueda/id/{idTemporal}')
            data = response.json()
            if response.status_code == 200:  
                cargos = data['cargos']
                mensaje = data['message']
                logger = definir_log_info('actualizar','logs_cargo')
                logger.debug("Obteniendo informacion del cargo: " + mensaje)
                return render(request, 'cargos/cargoactualizar.html', {'cargos': cargos,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_actualizar','logs_cargo')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'cargos/cargoactualizar.html', {'mensaje': mensaje,'cargos':cargos,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_cargo','logs_cargo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'cargos/cargoactualizar.html', {'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
def eliminar_cargo(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'cargos/id/{idTemporal}')
            res = response.json()
            rsp_cargos = requests.get(url + 'cargos/') 
            if rsp_cargos.status_code == 200:
                data = rsp_cargos.json()
                cargos = data['cargos']
                logger = definir_log_info('eliminar_cargo','logs_cargo')
                logger.info("Cargo eliminado correctamente")
            else:
                cargos = []
                logger = definir_log_info('error_eliminar_cargo','logs_cargo')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'cargos/buscarCargo.html', context)
    except Exception as e:
        logger = definir_log_info('excepcion_cargo','logs_cargo')
        logger.exception("Ocurrio una excepcion:" + str(mensaje))
        rsp_cargos = requests.get(url + 'cargos/') 
        if rsp_cargos.status_code == 200:
            data = rsp_cargos.json()
            cargos = data['cargos']
        else:
            cargos = [] 
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros o esta protegido'
        context = {'cargos': cargos, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'cargos/buscarCargo.html', context)      
    
def buscar_cargos(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'cargos/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    cargos = {}
                    cargos = data['cargos']
                    logger = definir_log_info('buscar_cargo','logs_cargo')
                    logger.debug("Se obtuvo el cargo especifico(filtrado por ID): " + mensaje)
                    context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'cargos/buscarCargo.html', context)     
                else:
                    cargos = []
                    mensaje = 'No se encontraron cargos'
                    logger = definir_log_info('error_buscar_cargo','logs_cargo')
                    logger.debug("No se obtuvo el cargo especifico(filtrado por ID): " + mensaje)
                    return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})  
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    cargos = {}
                    cargos = data['cargos']
                    logger = definir_log_info('buscar_cargo','logs_cargo')
                    logger.debug("Se obtuvo el cargo especifico(filtrado por nombre): " + mensaje)
                    context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'cargos/buscarCargo.html', context)
                else:
                    cargos = []
                    mensaje = 'No se encontraron cargos'
                    logger = definir_log_info('error_buscar_cargo','logs_cargo')
                    logger.debug("No se obtuvo el cargo especifico(filtrado por ID): " + mensaje)
                    return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            response = requests.get(url+'cargos/')
            if response.status_code == 200:
                data = response.json()
                cargos = data['cargos']
                mensaje = data['message']  
                logger = definir_log_info('buscar_cargo','logs_cargo')
                logger.debug("Se obtuvieron todos los cargos: " + mensaje )
                return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                cargos = []
                mensaje = 'No se encontraron cargos'
                logger = definir_log_info('error_buscar_cargo','logs_cargo')
                logger.debug("No se obtuvo el cargo especifico(filtrado por ID): " + mensaje)
            return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_cargo','logs_cargo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'cargos/')
        if response.status_code == 200:
            data = response.json()
            cargos = data['cargos']
            mensaje = data['message']  
            logger = definir_log_info('buscar_cargo','logs_cargo')
            logger.debug("Se obtuvieron todos los cargos: " + mensaje ) 
            return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            cargos = []
            mensaje = 'No se encontraron cargos'
            logger = definir_log_info('error_buscar_cargo','logs_cargo')
            logger.debug("No se pudo obtener informacion de cargos: " + mensaje)
        return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_cargos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    