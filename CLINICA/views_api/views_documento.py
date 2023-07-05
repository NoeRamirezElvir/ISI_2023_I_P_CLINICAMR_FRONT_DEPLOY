from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_documentos(request):
    response = requests.get(url+'documentos/')
    if response.status_code == 200:
        data = response.json()
        documentos = data['documentos']
    else:
        documentos = []
    context = {'documentos': documentos}
    return render(request, 'documentos/buscarDocumento.html', context)

def crear_documento(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            longitud = int(request.POST['longitud'])



            #raise Exception('Error')
            registro_temp={'nombre': nombre, 'longitud': longitud}
            response = requests.post(url+'documentos/', json={'nombre': nombre, 'longitud': longitud})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('error_crear','logs_documento')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear','logs_documento')
                    logger.debug(f"Se ha registrado un documento: Nombre={nombre}")
                return render(request, 'documentos/documento.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_crear','logs_documento')
                logger.warning("No se pudo crear el documento: " + mensaje)
                return render(request, 'documentos/documento.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_documento','logs_documento')
            logger.debug('Entrando a la funcion crear documento')
            return render(request, 'documentos/documento.html',{'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        
    except Exception as e:
        logger = definir_log_info('excepcion_documento','logs_documento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'documentos/documento.html',{'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})    
        
def abrir_actualizar_documentos(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'documentos/busqueda/id/'+str(request.POST['id_documento']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                documentos = data['documentos']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info ('error_abrir_actualizar','logs_documento')
                    logger.info("se obtuvo el documento correspondiente a la actualizacion: " + mensaje) 
                else:
                    logger = definir_log_info('abrir_actualizar', 'logs_documento')
                    logger.debug("se obtuvo una respuesta invalida" + mensaje )
            else:
                documentos = []
                logger = definir_log_info ('error_abrir_actualizar','logs_documento')
                logger.debug("se obtuvo el documento correspondiente a la actuzalizacion "+ mensaje )
            context = {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'documentos/documentoactualizar.html', context)
    except Exception as e:
        logger = definir_log_info('excepcion_documento','logs_documento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'docuemnto': documentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'documentos/documentoactualizar.html', context)
    
def actualizar_documento(request, id):
    try:
        if id == '':
            raise Exception("ID: esta vacio")
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            longitud = int(request.POST['longitud'])
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'documentos/id/{idTemporal}', json={'nombre': nombre, 'longitud': longitud})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el documento relacionado con el id
            res = requests.get(url+f'documentos/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            documentos = data['documentos']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar','logs_documento')
                logger.debug("Actualizacion correcta del documento: " + mensaje)
                return render(request, 'documentos/documentoactualizar.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'documentos':documentos })
            
            else:
                logger = definir_log_info('error_actualizar','logs_documento')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                mensaje = rsp['message']
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'documentos/documentoactualizar.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'documentos':documentos})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'documentos/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                documentos = data['documentos']
                mensaje = data['message']
                logger = definir_log_info('actualizar','logs_documento')
                logger.debug("Obteniendo informacion del documento: " + mensaje)
                return render(request, 'documentos/documentoactualizar.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_actualizar','logs_documento')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'documentos/documentoactualizar.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'documentos':documentos})
    except Exception as e:
        logger = definir_log_info('excepcion_documento','logs_documento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'documentos/documentoactualizar.html', {'mensaje': mensaje,'documentos':documentos,'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})

def eliminar_documento(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'documentos/id/{idTemporal}')
            res = response.json()
            rsp_documentos = requests.get(url + 'documentos/') 
            if rsp_documentos.status_code == 200:
                data = rsp_documentos.json()
                documentos = data['documentos']
                logger = definir_log_info('eliminar_documento','logs_documento')
                logger.info("documento eliminado correctamente")
            else:
                documentos = []
                logger = definir_log_info('error_eliminar_documento','logs_documento')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje': mensaje}
            return render(request, 'documentos/buscarDocumento.html', context)     
    except Exception as e:   
        rsp_documentos = requests.get(url + 'documentos/') 
        if rsp_documentos.status_code == 200:
            data = rsp_documentos.json()
            documentos = data['documentos']
        else:
            documentos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        logger = definir_log_info('excepcion_documento','logs_documento')
        logger.exception("Ocurrio una excepcion:" + str(mensaje))
        context = {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'error': mensaje}
        return render(request, 'documentos/buscarDocumento.html', context)     
    
def buscar_documentos(request):
    try:    
        valor = request.GET.get('buscador', None)
        url2 = url + 'documentos/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    documentos = {}
                    documentos = data['documentos']
                    logger = definir_log_info('buscar_documento','logs_documento')
                    logger.debug("Se obtuvo el documento especifico(filtrado por ID): " + mensaje)
                    context = {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje':mensaje}
                    return render(request, 'documentos/buscarDocumento.html', context) 
                else:
                    documentos = []
                    mensaje = 'No se encontraron documentos'
                    logger = definir_log_info('error_buscar_documento','logs_documento')
                    logger.debug("No se obtuvo el documento especifico(filtrado por ID): " + mensaje)
                    return render(request, 'documentos/buscarDocumento.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje': mensaje})
        
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    documentos = {}
                    documentos = data['documentos']
                    logger = definir_log_info('buscar_documento','logs_documento')
                    logger.debug("Se obtuvo el documento especifico(filtrado por nombre): " + mensaje)
                    context = {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje':mensaje}
                    return render(request, 'documentos/buscarDocumento.html', context)
                else:
                    documentos = []
                    mensaje = 'No se encontraron documentos'
                    logger = definir_log_info('error_buscar_documento','logs_documento')
                    logger.debug("No se obtuvo el documento especifico(filtrado por ID): " + mensaje)
                    return render(request, 'documentos/buscarDocumento.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje': mensaje})
        else:
            response = requests.get(url+'documentos/')
            if response.status_code == 200:
                data = response.json()
                documentos = data['documentos']
                mensaje = data['message']   
                logger = definir_log_info('buscar_documento','logs_documento')
                logger.debug("Se obtuvieron todos los documentos: " + mensaje )
                return render(request, 'documentos/buscarDocumento.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje': mensaje})
            else:
                documentos = []
                mensaje = 'No se encontraron documentos'
                logger = definir_log_info('error_buscar_documento','logs_documento')
                logger.debug("No se obtuvo el documento especifico(filtrado por ID): " + mensaje)
            return render(request, 'documentos/buscarDocumento.html', {'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'documentos': documentos, 'mensaje': mensaje})
    
    except Exception as e:
        logger = definir_log_info('excepcion_documento','logs_documento')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'documentos/')
        if response.status_code == 200:
            data = response.json()
            documentos = data['documentos']
            mensaje = data['message']  
            logger = definir_log_info('buscar_documento','logs_documento')
            logger.debug("Se obtuvieron todos los documentos: " + mensaje ) 
            return render(request, 'documentos/buscardocumento.html', {'documentos': documentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            documentos = []
            mensaje = 'No se encontraron documentos'
            logger = definir_log_info('error_buscar_documento','logs_documento')
            logger.debug("No se pudo obtener informacion de documento: " + mensaje)
        return render(request, 'documentos/buscardocumento.html', {'documentos': documentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_documentos(),'reportes_usuarios':DatosReportes.cargar_usuario()})