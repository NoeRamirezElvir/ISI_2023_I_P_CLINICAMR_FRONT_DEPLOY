from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_especialidades(request):
    response = requests.get(url+'especialidad/')
    if response.status_code == 200:
        data = response.json()
        especialidad = data['especialidad']
        if not especialidad:
            especialidad = []
    else:
        especialidad = []
    context = {'especialidad': especialidad}
    return render(request, 'especialidad/BuscarEspecialidad.html', context)


def crear_especialidades(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            registro_temp={'nombre': nombre, 'descripcion': descripcion}
            response = requests.post(url+'especialidad/', json={'nombre': nombre, 'descripcion': descripcion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_especialidad','logs_especialidad')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_especialidad','logs_especialidad')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'especialidad/especialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_especialidad','logs_especialidad')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'especialidad/especialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_especialidad','logs_especialidad')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'especialidad/especialidad.html',{'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_especialidad','logs_especialidad')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'especialidad/especialidad.html',{'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje':mensaje})
    

def abrir_actualizar_especialidades(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'especialidad/busqueda/id/'+str(request.POST['id_especialidad']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                especialidad = data['especialidad']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_especialidad','logs_especialidad')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_especialidad','logs_especialidad')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                especialidad = []
                logger = definir_log_info('abrir_actualizar_especialidad','logs_especialidad')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'especialidad/especialidadActualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_especialidad','logs_especialidad')
        logger.exception("Ocurrio una excepcion:" + str(e))
        especialidad = []
        context = {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje':mensaje}
        return render(request, 'especialidad/especialidadActualizar.html', context)

def actualizar_especialidades(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'especialidad/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'especialidad/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            especialidad = data['especialidad']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_especialidad','logs_especialidad')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'especialidad/especialidadActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'especialidad':especialidad })
            else:
                mensaje = rsp['message']   
                logger = definir_log_info('actualizar_especialidad','logs_especialidad')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'especialidad/especialidadActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'especialidad':especialidad})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'especialidad/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                usuario = data['especialidad']
                mensaje = data['message']
                logger = definir_log_info('actualizar_especialidad','logs_especialidad')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'especialidad/especialidadActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_especialidad','logs_especialidad')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'especialidad/especialidadActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'especialidad':especialidad})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_especialidad','logs_especialidad')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'especialidad/especialidadActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'especialidad':especialidad})
       
def eliminar_especialidades(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'especialidad/id/{idTemporal}')
            res = response.json()
            rsp_especialidad = requests.get(url + 'especialidad/') 
            if rsp_especialidad.status_code == 200:
                data = rsp_especialidad.json()
                especialidad = data['especialidad']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_especialidad','logs_especialidad')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_especialidad','logs_especialidad')
                    logger.info("No se ha podido eliminar el registro")
            else:
                especialidad = []
                logger = definir_log_info('eliminar_especialidad','logs_especialidad')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje': mensaje}
            return render(request, 'especialidad/BuscarEspecialidad.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_especialidad','logs_especialidad')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_especialidad = requests.get(url + 'especialidad/') 
        if rsp_especialidad.status_code == 200:
            data = rsp_especialidad.json()
            especialidad = data['especialidad']
        else:
            especialidad = []
        mensaje += ' No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'error': mensaje}
        return render(request, 'especialidad/BuscarEspecialidad.html', context)     

def buscar_especialidades(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'especialidad/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    especialidad = {}
                    especialidad = data['especialidad']
                    if especialidad != []:   
                        logger = definir_log_info('buscar_especialidad','logs_especialidad')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_especialidad','logs_especialidad')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje':mensaje}
                    return render(request, 'especialidad/BuscarEspecialidad.html', context)     
                else:
                    especialidad = []
                    mensaje = 'No se encontraron especialidades'
                    logger = definir_log_info('buscar_especialidad','logs_especialidad')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'especialidad/BuscarEspecialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje': mensaje})  
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    especialidad = {}
                    especialidad = data['especialidad']
                    if especialidad != []:   
                        logger = definir_log_info('buscar_especialidad','logs_especialidad')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_especialidad','logs_especialidad')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje':mensaje}
                    return render(request, 'especialidad/BuscarEspecialidad.html', context)
                else:
                    especialidad = []
                    mensaje = 'No se encontraron especialidades'
                    logger = definir_log_info('buscar_especialidad','logs_especialidad')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'especialidad/BuscarEspecialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'especialidad/')
            if response.status_code == 200:
                data = response.json()
                especialidad = data['especialidad']
                mensaje = data['message']   
                if especialidad != []:   
                    logger = definir_log_info('buscar_especialidad','logs_especialidad')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_especialidad','logs_especialidad')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'especialidad/BuscarEspecialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje': mensaje})
            else:
                especialidad = []
                mensaje = 'No se encontraron especialidades'
                logger = definir_log_info('buscar_especialidad','logs_especialidad')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'especialidad/BuscarEspecialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_especialidad','logs_especialidad')
        logger.exception("Ocurrio una excepcion:" + str(e))
        especialidad = []
        return render(request, 'especialidad/BuscarEspecialidad.html', {'reportes_lista':DatosReportes.cargar_lista_especialidades(),'reportes_usuarios':DatosReportes.cargar_usuario(),'especialidad': especialidad, 'mensaje': mensaje})
   