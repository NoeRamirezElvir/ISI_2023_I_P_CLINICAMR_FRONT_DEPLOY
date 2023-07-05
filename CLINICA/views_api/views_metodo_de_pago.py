from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info


url = 'https://clinicamr.onrender.com/api/'
def listar_metodos_De_pago(request):
    response = requests.get(url+'metodop/')
    if response.status_code == 200:
        data = response.json()
        metodop = data['metodop']
        if not metodop:
            metodop = []
    else:
        metodop = []
    context = {'metodop': metodop}
    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)


def crear_metodos_De_pago(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            registro_temp={'nombre': nombre, 'descripcion': descripcion}
            response = requests.post(url+'metodop/', json={'nombre': nombre, 'descripcion': descripcion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_metodo_pago','logs_metodo_pago')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_metodo_pago','logs_metodo_pago')
                    logger.debug(f"Se ha realizado un registro")

                return render(request, 'MetodoDePago/MetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_metodo_pago','logs_metodo_pago')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'MetodoDePago/MetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_metodo_pago','logs_metodo_pago')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'MetodoDePago/MetodoDePago.html',{'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_metodo_pago','logs_metodo_pago')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'MetodoDePago/MetodoDePago.html',{'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def abrir_actualizar_metodos_De_pago(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'metodop/busqueda/id/'+str(request.POST['id_metodo']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                metodop = data['metodop']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_metodo_pago','logs_metodo_pago')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_metodo_pago','logs_metodo_pago')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                metodop = []
                logger = definir_log_info('abrir_actualizar_metodo_pago','logs_metodo_pago')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_metodo_pago','logs_metodo_pago')
        logger.exception("Ocurrio una excepcion:" + str(e))
        metodop = []
        context = {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje':mensaje}
        return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', context)
    

def actualizar_metodos_De_pago(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'metodop/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'metodop/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            metodop = data['metodop']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_metodo_pago','logs_metodo_pago')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'metodop':metodop })
            else:
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                logger = definir_log_info('actualizar_metodo_pago','logs_metodo_pago')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'metodop':metodop})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'metodop/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                metodop = data['metodop']
                mensaje = data['message']
                logger = definir_log_info('actualizar_metodo_pago','logs_metodo_pago')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_metodo_pago','logs_metodo_pago')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'metodop':metodop})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_metodo_pago','logs_metodo_pago')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'metodop/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            metodop = data['metodop']
            mensaje = data['message']
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop})
        else:
            mensaje = data['message']
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'metodop':metodop})
   

def eliminar_metodos_De_pago(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'metodop/id/{idTemporal}')
            res = response.json()
            rsp_metodop = requests.get(url + 'metodop/') 
            if rsp_metodop.status_code == 200:
                data = rsp_metodop.json()
                metodop = data['metodop']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_metodo_pago','logs_metodo_pago')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_metodo_pago','logs_metodo_pago')
                    logger.info("No se ha podido eliminar el registro")
            else:
                metodop = []
                logger = definir_log_info('eliminar_metodo_pago','logs_metodo_pago')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje}
            return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_metodo_pago','logs_metodo_pago')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_metodop = requests.get(url + 'metodop/') 
        if rsp_metodop.status_code == 200:
            data = rsp_metodop.json()
            metodop = data['metodop']
        else:
            metodop = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'error': mensaje}
        return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)     


def buscar_metodos_De_pago(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'metodop/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    metodop = {}
                    metodop = data['metodop']
                    if metodop != []:   
                        logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje':mensaje}
                    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)
                else:
                    metodop = []
                    mensaje = 'No se encontraron Metodos de pago'
                    logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje})
           
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    metodop = {}
                    metodop = data['metodop']
                    if metodop != []:   
                        logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje':mensaje}
                    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)
                else:
                    metodop = []
                    mensaje = 'No se encontraron Metodos de pago'
                    logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'metodop/')
            if response.status_code == 200:
                data = response.json()
                metodop = data['metodop']
                mensaje = data['message']   
                if metodop != []:   
                    logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje})
            else:
                metodop = []
                mensaje = 'No se encontraron Metodos de pago'
                logger = definir_log_info('buscar_metodo_pago','logs_metodo_pago')
                logger.info(f"No se obtuvieron los registros:{mensaje}")

            return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_metodo_pago','logs_metodo_pago')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'metodop/')
        if response.status_code == 200:
            data = response.json()
            metodop = data['metodop']
            mensaje = data['message']   
            return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje})
        else:
            metodop = []
            mensaje = 'No se encontraron Metodos de pago'
        return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'reportes_lista':DatosReportes.cargar_lista_metodo_pago(),'reportes_usuarios':DatosReportes.cargar_usuario(),'metodop': metodop, 'mensaje': mensaje})
   