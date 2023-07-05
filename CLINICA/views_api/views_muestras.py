from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info



url = 'https://clinicamr.onrender.com/api/'
def listar_muestras(request):
    response = requests.get(url+'muestras/')
    if response.status_code == 200:
        data = response.json()
        muestras = data['muestras']
    else:
        muestras = []
    context = {'muestras': muestras}
    return render(request, 'Muestras/buscarMuestra.html', context)

def crear_muestras(request):
    rsp_paciente = requests.get(url+'pacientes/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            pacientes_list = data['pacientes']
    else:
            pacientes_list = []
    rsp_tipo_muestra = requests.get(url+'tmuestra/')
    if rsp_paciente.status_code == 200:
            data = rsp_tipo_muestra.json()
            tipo_list = data['tmuestra']
    else:
            tipo_list = []
    try:
        if request.method == 'POST':
            idPaciente = int(request.POST['idPaciente'])
            idTipoMuestra = int(request.POST['idTipoMuestra'])
            fecha = request.POST['fecha']
            registro_temp = {'idPaciente': idPaciente, 'idTipoMuestra': idTipoMuestra, 'fecha': fecha}
            response = requests.post(url+'muestras/', json={'idPaciente': idPaciente, 'idTipoMuestra': idTipoMuestra, 'fecha': fecha})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_muestras','logs_muestras')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_muestras','logs_muestras')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'Muestras/Muestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp, 'paciente_list':pacientes_list, 'tipo_list':tipo_list})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_muestras','logs_muestras')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'Muestras/Muestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'paciente_list':pacientes_list, 'tipo_list':tipo_list})
        else:
            logger = definir_log_info('crear_muestras','logs_muestras')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'Muestras/Muestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'paciente_list':pacientes_list, 'tipo_list':tipo_list})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_muestras','logs_muestras')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Muestras/Muestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'paciente_list':pacientes_list, 'tipo_list':tipo_list})
    

def abrir_actualizar_muestras(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'muestras/busqueda/id/'+str(request.POST['id_muestra']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                muestras = data['muestras']
                mensaje = data['message']
            else:
                muestras = []
            context = {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'Muestras/MuestraActualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_muestras','logs_muestras')
        logger.exception("Ocurrio una excepcion:" + str(e))
        muestras = []
        context = {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje':mensaje}
        return render(request, 'Muestras/MuestraActualizar.html', context)
    

def actualizar_muestras(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            idPaciente = int(request.POST['idPaciente'])
            idTipoMuestra = int(request.POST['idTipoMuestra'])
            fecha = request.POST['fecha']
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'muestras/id/{idTemporal}', json={'idPaciente': idPaciente, 'idTipoMuestra': idTipoMuestra, 'fecha': fecha})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'muestras/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            muestras = data['muestras']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                return render(request, 'Muestras/MuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'muestras':muestras })
            else:
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'Muestras/MuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'muestras':muestras})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'muestras/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                muestras = data['muestras']
                mensaje = data['message']
                return render(request, 'Muestras/MuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras})
            else:
                mensaje = data['message']
                return render(request, 'Muestras/MuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'muestras':muestras})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_muestras','logs_muestras')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'muestras/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            muestras = data['muestras']
            mensaje = data['message']
            return render(request, 'Muestras/MuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras})
        else:
            mensaje = data['message']
            return render(request, 'Muestras/MuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'muestras':muestras})
    

def eliminar_muestras(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'muestras/id/{idTemporal}')
            res = response.json()
            rsp_muestras = requests.get(url + 'muestras/') 
            mensaje = res['message']
            if rsp_muestras.status_code == 200:
                data = rsp_muestras.json()
                muestras = data['muestras']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_muestras','logs_muestras')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_muestras','logs_muestras')
                    logger.info("No se ha podido eliminar el registro")
            else:
                muestras = []
                logger = definir_log_info('eliminar_muestras','logs_muestras')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            context = {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje}
            return render(request, 'Muestras/BuscarMuestra.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_muestras','logs_muestras')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_muestras = requests.get(url + 'muestras/') 
        if rsp_muestras.status_code == 200:
            data = rsp_muestras.json()
            muestras = data['muestras']
        else:
            muestras = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'error': mensaje}
        return render(request, 'Muestras/BuscarMuestra.html', context)     
           
def buscar_muestras(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'muestras/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    muestras = {}
                    muestras = data['muestras']
                    if muestras != []:   
                        logger = definir_log_info('buscar_muestras','logs_muestras')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_muestras','logs_muestras')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje':mensaje}

                    return render(request, 'Muestras/BuscarMuestra.html', context) 
                else:
                    muestras = []
                    mensaje = 'No se encontraron muestras'
                    logger = definir_log_info('buscar_muestras','logs_muestras')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'Muestras/BuscarMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje})
          
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    muestras = {}
                    muestras = data['muestras']
                    if muestras != []:   
                        logger = definir_log_info('buscar_muestras','logs_muestras')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_muestras','logs_muestras')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje':mensaje}
                    return render(request, 'Muestras/BuscarMuestra.html', context)
                else:
                    muestras = []
                    mensaje = 'No se encontraron muestras'
                    logger = definir_log_info('buscar_muestras','logs_muestras')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'Muestras/BuscarMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'muestras/')
            if response.status_code == 200:
                data = response.json()
                muestras = data['muestras']
                mensaje = data['message'] 
                if muestras != []:   
                    logger = definir_log_info('buscar_muestras','logs_muestras')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_muestras','logs_muestras')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")  
                return render(request, 'Muestras/BuscarMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje})
            else:
                muestras = []
                mensaje = 'No se encontraron muestras'
                logger = definir_log_info('buscar_muestras','logs_muestras')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'Muestras/BuscarMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_muestras','logs_muestras')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'muestras/')
        if response.status_code == 200:
            data = response.json()
            muestras = data['muestras']
            mensaje = data['message']   
            return render(request, 'Muestras/BuscarMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje})
        else:
            muestras = []
            mensaje = 'No se encontraron muestras'
        return render(request, 'Muestras/BuscarMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_muestras(),'reportes_usuarios':DatosReportes.cargar_usuario(),'muestras': muestras, 'mensaje': mensaje})
   