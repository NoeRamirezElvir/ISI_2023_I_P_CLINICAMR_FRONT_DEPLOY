from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos


url = 'https://clinicamr.onrender.com/api/'
def listar_empleados(request):
    response = requests.get(url+'empleados/')
    if response.status_code == 200:
        data = response.json()
        empleados = data['empleados']
    else:
        empleados  = []
    context = {'empleados': empleados}
    return render(request, 'empleado/buscarEmpleado.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_empleados(request):
    TipoDocumento= list_tipodocumento()
    
    EspecialidadMedico= list_EspecialidadMedico()
    
    CargoEmpleado= list_cargoEmpleado()
    
    try:
        if request.method == 'POST':
            
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            fechaNacimiento = request.POST['fechaNacimiento']
            idTipoDocumento = int(request.POST['idTipoDocument1'])
            idEspecialidadMedico=int(request.POST['idEspecialidadMedic1'])
            idCargoEmpleado =int(request.POST['idCargoEmplead1'])
            documento= request.POST ['documento']
            telefono = request.POST['telefono']
            email = request.POST['email']
            direccion = request.POST ['direccion']
            activo = int(request.POST['payment_method'])
            
            registro_temp={'nombre': nombre,'apellidos':apellidos,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'idEspecialidadMedico':idEspecialidadMedico, 'idCargoEmpleado':idCargoEmpleado,'documento': documento,'telefono': telefono,'email': email,'direccion': direccion,'activo': activo}
            response = requests.post(url+'empleados/', json={'nombre': nombre,'apellidos': apellidos,'fechaNacimiento': fechaNacimiento,'idTipoDocumentos':idTipoDocumento, 'idEspecialidadMedico':idEspecialidadMedico, 'idCargoEmpleado':idCargoEmpleado, 'documento': documento,'telefono': telefono,'email': email,'direccion': direccion,'activo': activo })
            empleadosdata={}
            if response.status_code == 200:
                empleadosdata = response.json()
                mensaje = empleadosdata['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_empleados','logs_empleados')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_empleados','logs_empleados')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'empleado/empleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado, 'registro_temp':registro_temp})
            else:
                empleadosdata = response.json()
                mensaje = empleadosdata['message']
                logger = definir_log_info('crear_empleados','logs_empleados')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'empleado/empleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_empleados','logs_empleados')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'empleado/empleado.html', { 'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
    except Exception as e:
        logger = definir_log_info('excepcion_empleados','logs_empleados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'empleado/empleado.html', { 'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})

def list_tipodocumento():
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
        data = rsp_TipoDocumento.json()
        TipoDocumento = data['documentos']
        return TipoDocumento

    else:
        TipoDocumento = []
        return TipoDocumento
    

def list_EspecialidadMedico():
    rsp_EspecialidadMedico = requests.get(url +'especialidad/')
    if rsp_EspecialidadMedico.status_code == 200:
        data = rsp_EspecialidadMedico.json()
        EspecialidadMedico = data ['especialidad']
        return EspecialidadMedico
    else:
        EspecialidadMedico=[]
        return EspecialidadMedico
    
def list_cargoEmpleado():
    rsp_CargoEmpleado = requests.get(url +'cargos/')
    if rsp_CargoEmpleado.status_code == 200:
        data = rsp_CargoEmpleado.json()
        CargoEmpleado = data ['cargos']
        return CargoEmpleado
         
    else:
         
         CargoEmpleado=[]
         return CargoEmpleado
     
     

def abrir_actualizar_empleados(request):
    TipoDocumento= list_tipodocumento()
    
    EspecialidadMedico= list_EspecialidadMedico()
    
    CargoEmpleado= list_cargoEmpleado()

    try:
        if request.method == 'POST':
            resp = requests.get(url+'empleados/busqueda/id/'+str(request.POST['id_empleados']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                empleados = data['empleados']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_empleados','logs_empleados')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_empleados','logs_empleados')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                empleados = []
                logger = definir_log_info('abrir_actualizar_empleados','logs_empleados')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            context = {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados,'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'empleado/EmpleadoActualizar.html', context)   
    except Exception as e:
        logger = definir_log_info('excepcion_empleados','logs_empleados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados,'TipoDocumento': TipoDocumento, 'EspecialidadMedico': EspecialidadMedico,'CargoEmpleado': CargoEmpleado}
        return render(request, 'empleado/EmpleadoActualizar.html', context)  

def actualizar_empleados(request, id):
    TipoDocumento= list_tipodocumento()
    
    EspecialidadMedico= list_EspecialidadMedico()
    
    CargoEmpleado= list_cargoEmpleado()
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            fechaNacimiento = request.POST['fechaNacimiento']
            idTipoDocumento = int(request.POST['idTipoDocument1'])
            idEspecialidadMedico=int(request.POST['idEspecialidadMedic1'])
            idCargoEmpleado =int(request.POST['idCargoEmplead1'])
            documento= request.POST ['documento']
            telefono = request.POST['telefono']
            email = request.POST['email']
            direccion = request.POST ['direccion']
            activo =int(request.POST['payment_method'])
            
            


            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'empleados/id/{idTemporal}', json={'nombre': nombre,'apellidos': apellidos,'fechaNacimiento': fechaNacimiento,'idTipoDocumentos':idTipoDocumento,'idEspecialidadMedico':idEspecialidadMedico, 'idCargoEmpleado':idCargoEmpleado,'documento': documento,'telefono': telefono,'email': email,'direccion': direccion,'activo': activo })
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'empleados/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            empleados = data['empleados']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "El actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_empleados','logs_empleados')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'empleado/EmpleadoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
            else:
                mensaje = rsp['message'] 
                logger = definir_log_info('actualizar_empleados','logs_empleados')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                           #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'empleado/EmpleadoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'empleados/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                empleados = data['empleados']
                mensaje = data['message']
                logger = definir_log_info('actualizar_empleados','logs_empleados')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'empleado/EmpleadoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_empleados','logs_empleados')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'empleado/EmpleadoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
    except Exception as e:
        logger = definir_log_info('excepcion_empleados','logs_empleados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'empleados/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            empleados = data['empleados']
            mensaje = data['message']
            return render(request, 'empleado/EmpleadoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
        else:
            mensaje = data['message']
            return render(request, 'empleado/EmpleadoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'empleados':empleados, 'TipoDocumento':TipoDocumento,'EspecialidadMedico ': EspecialidadMedico,'CargoEmpleado': CargoEmpleado})
    


def eliminar_empleados(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'empleados/id/{idTemporal}')
            res = response.json()
            rsp_empleados = requests.get(url + 'empleados/') 
            if rsp_empleados.status_code == 200:
                data = rsp_empleados.json()
                empleados = data['empleados']
                logger = definir_log_info('eliminar_empleados','logs_empleados')
                logger.info("Registro eliminado correctamente")
            else:
                empleados = []
                logger = definir_log_info('eliminar_empleados','logs_empleados')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje}
            return render(request, 'empleado/buscarEmpleado.html', context)     
    except Exception as e:
        logger = definir_log_info('excepcion_empleados','logs_empleados')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_empleados = requests.get(url + 'empleados/') 
        if rsp_empleados.status_code == 200:
            data = rsp_empleados.json()
            empleados = data['empleados']
        else:
            empleados = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'error': mensaje}
        return render(request, 'empleado/buscarEmpleado.html', context)     
    
def buscar_empleados(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'empleados/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    empleados = {}
                    empleados = data['empleados']
                    if empleados != []:   
                        logger = definir_log_info('buscar_empleados','logs_empleados')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_empleados','logs_empleados')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje':mensaje}
                    return render(request, 'empleado/buscarEmpleado.html', context)       
                else:
                    empleados = []
                    mensaje = 'No se encontro empleados'
                    logger = definir_log_info('buscar_empleados','logs_empleados')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'empleado/buscarEmpleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje})
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    empleados = {}
                    empleados = data['empleados']
                    if empleados != []:   
                        logger = definir_log_info('buscar_empleados','logs_empleados')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_empleados','logs_empleados')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje':mensaje}
                    return render(request, 'empleado/buscarEmpleado.html', context)
                else:
                    empleados = []
                    mensaje = 'No se encontro empleados'
                    logger = definir_log_info('buscar_empleados','logs_empleados')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'empleado/buscarEmpleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje})
        else:
            response = requests.get(url+'empleados/')
            if response.status_code == 200:
                data = response.json()
                empleados = data['empleados']
                mensaje = data['message'] 
                if empleados != []:   
                    logger = definir_log_info('buscar_empleados','logs_empleados')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_empleados','logs_empleados')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")  
                return render(request, 'empleado/buscarEmpleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje})
            else:
                empleados = []
                mensaje = 'No se encontro empleados'
                logger = definir_log_info('buscar_empleados','logs_empleados')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'empleado/buscarEmpleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje})
    except Exception as e:
        logger = definir_log_info('excepcion_empleados','logs_empleados')
        logger.exception("Ocurrio una excepcion:" + str(e))

        response = requests.get(url+'empleados/')
        if response.status_code == 200:
            data = response.json()
            empleados = data['empleados']
            mensaje = data['message']   
            return render(request, 'empleado/buscarEmpleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje})
        else:
            empleados = []
            mensaje = 'No se encontro empleados'
        return render(request, 'empleado/buscarEmpleado.html', {'reportes_lista':DatosReportes.cargar_lista_empleados(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'empleados': empleados, 'mensaje': mensaje})
    
