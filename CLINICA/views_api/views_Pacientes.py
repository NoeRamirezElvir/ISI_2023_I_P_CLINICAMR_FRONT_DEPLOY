from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_pacientes(request):
    response = requests.get(url+'pacientes/')
    if response.status_code == 200:
        data = response.json()
        pacientes = data['pacientes']
    else:
        pacientes  = []
    context = {'pacientes': pacientes}
    return render(request, 'Pacientes/buscarPaciente.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_paciente(request):
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
            data = rsp_TipoDocumento.json()
            TipoDocumento = data['documentos']
    else:
            TipoDocumento = []
    
    try:
        if request.method == 'POST':
            
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            fechaNacimiento = request.POST['fechaNacimiento']
            idTipoDocumento = int(request.POST['idTipoDocument1'])
            documento= request.POST ['documento']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            direccion = request.POST ['direccion']
            
            registro_temp={'nombre': nombre,'apellido': apellido,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'documento': documento,'telefono': telefono,'correo': correo,'direccion': direccion }
            response = requests.post(url+'pacientes/', json={'nombre': nombre,'apellido': apellido,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'documento': documento,'telefono': telefono,'correo': correo,'direccion': direccion })
            pacientedata={}
            if response.status_code == 200:
                pacientedata = response.json()
                mensaje = pacientedata['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_paciente','logs_paciente')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_paciente','logs_paciente')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'Pacientes/Paciente.html', {'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = pacientedata['message']
                logger = definir_log_info('crear_paciente','logs_paciente')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'Pacientes/Paciente.html', {'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_paciente','logs_paciente')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'Pacientes/Paciente.html', { 'TipoDocumento': TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_paciente','logs_paciente')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Pacientes/Paciente.html', { 'TipoDocumento': TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
   

def abrir_actualizar_pacientes(request):
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
            data = rsp_TipoDocumento.json()
            TipoDocumento = data['documentos']
    else:
            TipoDocumento = []
    
    try:
        if request.method == 'POST':
            resp = requests.get(url+'pacientes/busqueda/id/'+str(request.POST['id_pacientes']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                pacientes = data['pacientes']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_paciente','logs_paciente')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_paciente','logs_paciente')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                pacientes = []
                logger = definir_log_info('abrir_actualizar_paciente','logs_paciente')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'pacientes': pacientes,'TipoDocumento': TipoDocumento, 'mensaje':mensaje ,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            mensaje = data['message']
            return render(request, 'Pacientes/PacienteActualizar.html', context)   
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_paciente','logs_paciente')
        logger.exception("Ocurrio una excepcion:" + str(e))
        pacientes = []
        context = {'pacientes': pacientes,'TipoDocumento': TipoDocumento, 'mensaje':mensaje ,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'Pacientes/PacienteActualizar.html', context)   
   

def actualizar_pacientes(request, id):
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
            data = rsp_TipoDocumento.json()
            TipoDocumento = data['documentos']
    else:
            TipoDocumento = []
    
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            fechaNacimiento = request.POST['fechaNacimiento']
            idTipoDocumento = int(request.POST['idTipoDocument1'])
            documento= request.POST ['documento']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            direccion = request.POST ['direccion']
            


            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'pacientes/id/{idTemporal}', json={'nombre': nombre,'apellido': apellido,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'documento': documento,'telefono': telefono,'correo': correo,'direccion': direccion })
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            pacientes = data['pacientes']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_paciente','logs_paciente')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = rsp['message']          
                logger = definir_log_info('actualizar_paciente','logs_paciente')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                pacientes = data['pacientes']
                mensaje = data['message']
                logger = definir_log_info('actualizar_paciente','logs_paciente')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'Pacientes/PacienteActualizar.html', {'pacientes': pacientes, 'TipoDocumento':TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_paciente','logs_paciente')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_paciente','logs_paciente')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            pacientes = data['pacientes']
            mensaje = data['message']
            return render(request, 'Pacientes/PacienteActualizar.html', {'pacientes': pacientes, 'TipoDocumento':TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            mensaje = data['message']
            return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    

def eliminar_pacientes(request, id):
    
    
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'pacientes/id/{idTemporal}')
            res = response.json()
            rsp_pacientes = requests.get(url + 'pacientes/') 
            if rsp_pacientes.status_code == 200:
                data = rsp_pacientes.json()
                pacientes = data['pacientes']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_paciente','logs_paciente')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_paciente','logs_paciente')
                    logger.info("No se ha podido eliminar el registro")

            else:
                pacientes = []
                logger = definir_log_info('eliminar_paciente','logs_paciente')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'Pacientes/buscarPaciente.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_paciente','logs_paciente')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_pacientes = requests.get(url + 'pacientes/') 
        if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            pacientes = data['pacientes']
        else:
            pacientes = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'pacientes': pacientes, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'Pacientes/buscarPaciente.html', context)     
            
def buscar_pacientes(request):
        
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'pacientes/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pacientes = {}
                    pacientes = data['pacientes']
                    if pacientes != []:   
                        logger = definir_log_info('buscar_paciente','logs_paciente')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_paciente','logs_paciente')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'pacientes': pacientes, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'Pacientes/buscarPaciente.html', context) 
                else:
                    pacientes = []
                    mensaje = 'No se encontro paciente'
                    logger = definir_log_info('buscar_paciente','logs_paciente')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pacientes = {}
                    pacientes = data['pacientes']
                    if pacientes != []:   
                        logger = definir_log_info('buscar_paciente','logs_paciente')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_paciente','logs_paciente')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'pacientes': pacientes, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'Pacientes/buscarPaciente.html', context)
                else:
                    pacientes = []
                    mensaje = 'No se encontro paciente'
                    logger = definir_log_info('buscar_paciente','logs_paciente')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    

        else:
            response = requests.get(url+'pacientes/')
            if response.status_code == 200:
                data = response.json()
                pacientes = data['pacientes']
                mensaje = data['message']   
                if pacientes != []:   
                    logger = definir_log_info('buscar_paciente','logs_paciente')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_paciente','logs_paciente')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                pacientes = []
                mensaje = 'No se encontro paciente'
                logger = definir_log_info('buscar_paciente','logs_paciente')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_paciente','logs_paciente')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'pacientes/')
        if response.status_code == 200:
            data = response.json()
            pacientes = data['pacientes']
            mensaje = data['message']   
            return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            pacientes = []
            mensaje = 'No se encontro paciente'
        return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_pacientes(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
