from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos




url = 'https://clinicamr.onrender.com/api/'
def listar_proveedor(request):
    response = requests.get(url+'proveedores/')
    if response.status_code == 200:
        data = response.json()
        proveedores = data['proveedores']
    else:
        proveedores = []
    context = {'proveedores': proveedores}
    return render(request, 'Proveedor/BuscarProveedor.html', context)

def crear_proveedor(request):
    tipos = list_tipos()
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            direccion = request.POST ['direccion']

            registro_temp = {'nombre': nombre,'telefono': telefono,'correo': correo,'direccion': direccion}
            response = requests.post(url+'proveedores/', json={'nombre': nombre,'telefono': telefono,'correo': correo,'direccion': direccion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_proveedor','logs_proveedor')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_proveedor','logs_proveedor')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'Proveedor/Proveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp, 'tipos':tipos})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_proveedor','logs_proveedor')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'Proveedor/Proveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'tipos':tipos})
        else:
            logger = definir_log_info('crear_proveedor','logs_proveedor')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'Proveedor/Proveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tipos':tipos})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_proveedor','logs_proveedor')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Proveedor/Proveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tipos':tipos})
    

def abrir_actualizar_proveedor(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'proveedores/busqueda/id/'+str(request.POST['id_proveedores']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                proveedores = data['proveedores']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_proveedor','logs_proveedor')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_proveedor','logs_proveedor')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                proveedores = []
                logger = definir_log_info('abrir_actualizar_proveedor','logs_proveedor')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'Proveedor/ProveedorActualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_proveedor','logs_proveedor')
        logger.exception("Ocurrio una excepcion:" + str(e))
        proveedores = []
        context = {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje':mensaje}
        return render(request, 'Proveedor/ProveedorActualizar.html', context)
    

def actualizar_proveedor(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            direccion = request.POST ['direccion']
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'proveedores/id/{idTemporal}', json={'nombre': nombre,'telefono': telefono,'correo': correo,'direccion': direccion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'proveedores/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            proveedores = data['proveedores']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_proveedor','logs_proveedor')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'Proveedor/ProveedorActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'proveedores':proveedores })
            else:
                mensaje = rsp['message']  
                logger = definir_log_info('actualizar_proveedor','logs_proveedor')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                          #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'Proveedor/ProveedorActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'proveedores':proveedores})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'proveedores/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                proveedores = data['proveedores']
                mensaje = data['message']
                logger = definir_log_info('actualizar_proveedor','logs_proveedor')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'Proveedor/ProveedorActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_proveedor','logs_proveedor')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'Proveedor/ProveedorActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'proveedores':proveedores})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_proveedor','logs_proveedor')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'proveedores/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            proveedores = data['proveedores']
            mensaje = data['message']
            return render(request, 'Proveedor/ProveedorActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores})
        else:
            mensaje = data['message']
            return render(request, 'Proveedor/ProveedorActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'proveedores':proveedores})
    

def eliminar_proveedor(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'proveedores/id/{idTemporal}')
            res = response.json()
            rsp_proveedores = requests.get(url + 'proveedores/') 
            if rsp_proveedores.status_code == 200:
                data = rsp_proveedores.json()
                proveedores = data['proveedores']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_proveedor','logs_proveedor')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_proveedor','logs_proveedor')
                    logger.info("No se ha podido eliminar el registro")
            else:
                proveedores = []
                logger = definir_log_info('eliminar_proveedor','logs_proveedor')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje}
            return render(request, 'Proveedor/BuscarProveedor.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_proveedor','logs_proveedor')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_proveedores = requests.get(url + 'proveedores/') 
        if rsp_proveedores.status_code == 200:
            data = rsp_proveedores.json()
            proveedores = data['proveedores']
        else:
            proveedores = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'error': mensaje}
        return render(request, 'Proveedor/BuscarProveedor.html', context)     

def buscar_proveedor(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'proveedores/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    proveedores = {}
                    proveedores = data['proveedores']
                    if proveedores != []:   
                        logger = definir_log_info('buscar_proveedor','logs_proveedor')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_proveedor','logs_proveedor')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje':mensaje}
                    return render(request, 'Proveedor/BuscarProveedor.html', context) 
                else:
                    proveedores = []
                    mensaje = 'No se encontraron proveedores'
                    logger = definir_log_info('buscar_proveedor','logs_proveedor')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'Proveedor/BuscarProveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje})
      
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    proveedores = {}
                    proveedores = data['proveedores']
                    if proveedores != []:   
                        logger = definir_log_info('buscar_proveedor','logs_proveedor')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_proveedor','logs_proveedor')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje':mensaje}
                    return render(request, 'Proveedor/BuscarProveedor.html', context)
                else:
                    proveedores = []
                    mensaje = 'No se encontraron proveedores'
                    logger = definir_log_info('buscar_proveedor','logs_proveedor')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'Proveedor/BuscarProveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje})

        else:
            response = requests.get(url+'proveedores/')
            if response.status_code == 200:
                data = response.json()
                proveedores = data['proveedores']
                mensaje = data['message']   
                if proveedores != []:   
                    logger = definir_log_info('buscar_proveedor','logs_proveedor')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_proveedor','logs_proveedor')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'Proveedor/BuscarProveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje})
            else:
                proveedores = []
                mensaje = 'No se encontraron proveedores'
                logger = definir_log_info('buscar_proveedor','logs_proveedor')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'Proveedor/BuscarProveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_proveedor','logs_proveedor')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'proveedores/')
        if response.status_code == 200:
            data = response.json()
            proveedores = data['proveedores']
            mensaje = data['message']   
            return render(request, 'Proveedor/BuscarProveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje})
        else:
            proveedores = []
            mensaje = 'No se encontraron proveedores'
        return render(request, 'Proveedor/BuscarProveedor.html', {'reportes_lista':DatosReportes.cargar_lista_proveedores(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'proveedores': proveedores, 'mensaje': mensaje})
    


def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/proveedor')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list