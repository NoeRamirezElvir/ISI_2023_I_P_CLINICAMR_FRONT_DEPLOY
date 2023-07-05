from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info


url = 'https://clinicamr.onrender.com/api/'
def listar_laboratorios(request):
    response = requests.get(url+'laboratorios/')
    if response.status_code == 200:
        data = response.json()
        laboratorios = data['laboratorios']
    else:
        laboratorios = []
    context = {'laboratorios': laboratorios}
    return render(request, 'Laboratorios/BuscarLaboratorios.html', context)

def crear_laboratorios(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            disponibilidad = int(request.POST['payment_method'])

            registro_temp={'nombre': nombre, 'direccion': direccion,'telefono': telefono, 'disponibilidad': disponibilidad}
            response = requests.post(url+'laboratorios/', json={'nombre': nombre, 'direccion': direccion,'telefono': telefono, 'disponibilidad': disponibilidad})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_laboratorios','logs_laboratorios')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_laboratorios','logs_laboratorios')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'Laboratorios/Laboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_laboratorios','logs_laboratorios')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'Laboratorios/Laboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_laboratorios','logs_laboratorios')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'Laboratorios/Laboratorios.html',{'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_laboratorios','logs_laboratorios')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'Laboratorios/Laboratorios.html',{'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    

def abrir_actualizar_laboratorios(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'laboratorios/busqueda/id/'+str(request.POST['id_laboratorios']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                laboratorios = data['laboratorios']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_laboratorios','logs_laboratorios')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_laboratorios','logs_laboratorios')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                laboratorios = []
                logger = definir_log_info('abrir_actualizar_laboratorios','logs_laboratorios')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_laboratorios','logs_laboratorios')
        logger.exception("Ocurrio una excepcion:" + str(e))
        laboratorios = []
        context = {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje':mensaje}
        return render(request, 'Laboratorios/ActualizarLaboratorios.html', context)
    

def actualizar_laboratorios(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            disponibilidad = int(request.POST['payment_method'])
            
            response = requests.put(url+f'laboratorios/id/{idTemporal}', json={'nombre': nombre, 'direccion': direccion,'telefono': telefono, 'disponibilidad': disponibilidad})
            
            rsp =  response.json()
        
            res = requests.get(url+f'laboratorios/busqueda/id/{idTemporal}')
            data = res.json()
            laboratorios = data['laboratorios']
            
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_laboratorios','logs_laboratorios')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'laboratorios':laboratorios })
            else:
                mensaje = rsp['message']       
                logger = definir_log_info('actualizar_laboratorios','logs_laboratorios')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                     #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'laboratorios':laboratorios})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'laboratorios/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                laboratorios = data['laboratorios']
                mensaje = data['message']
                logger = definir_log_info('actualizar_laboratorios','logs_laboratorios')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_laboratorios','logs_laboratorios')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'laboratorios':laboratorios})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_laboratorios','logs_laboratorios')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'laboratorios/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            laboratorios = data['laboratorios']
            mensaje = data['message']
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios})
        else:
            mensaje = data['message']
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'laboratorios':laboratorios})
    

def eliminar_laboratorios(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'laboratorios/id/{idTemporal}')
            res = response.json()
            rsp_laboratorios = requests.get(url + 'laboratorios/') 
            if rsp_laboratorios.status_code == 200:
                data = rsp_laboratorios.json()
                laboratorios = data['laboratorios']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_laboratorios','logs_laboratorios')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_laboratorios','logs_laboratorios')
                    logger.info("No se ha podido eliminar el registro")
            else:
                laboratorios = []
                logger = definir_log_info('eliminar_laboratorios','logs_laboratorios')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)

            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje}
            return render(request, 'Laboratorios/BuscarLaboratorios.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_laboratorios','logs_laboratorios')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_laboratorios = requests.get(url + 'laboratorios/') 
        if rsp_laboratorios.status_code == 200:
            data = rsp_laboratorios.json()
            laboratorios = data['laboratorios']
        else:
            laboratorios = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'error': mensaje}
        return render(request, 'Laboratorios/BuscarLaboratorios.html', context)     
   
def buscar_laboratorios(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'laboratorios/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    laboratorios = {}
                    laboratorios = data['laboratorios']
                    if laboratorios != []:   
                        logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje':mensaje}
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', context)  
                else:
                    laboratorios = []
                    mensaje = 'No se encontraron laboratorios'
                    logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje})
             
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    laboratorios = {}
                    laboratorios = data['laboratorios']
                    if laboratorios != []:   
                        logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje':mensaje}
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', context)
                else:
                    laboratorios = []
                    mensaje = 'No se encontraron laboratorios'
                    logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje})
        else:
            response = requests.get(url+'laboratorios/')
            if response.status_code == 200:
                data = response.json()
                laboratorios = data['laboratorios']
                mensaje = data['message']   
                if laboratorios != []:   
                    logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'Laboratorios/BuscarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje})
            else:
                laboratorios = []
                mensaje = 'No se encontraron laboratorios'
                logger = definir_log_info('buscar_laboratorios','logs_laboratorios')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'Laboratorios/BuscarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_laboratorios','logs_laboratorios')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'laboratorios/')
        if response.status_code == 200:
            data = response.json()
            laboratorios = data['laboratorios']
            mensaje = data['message']   
            return render(request, 'Laboratorios/BuscarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje})
        else:
            laboratorios = []
            mensaje = 'No se encontraron laboratorios'
        return render(request, 'Laboratorios/BuscarLaboratorios.html', {'reportes_lista':DatosReportes.cargar_lista_laboratorios(),'reportes_usuarios':DatosReportes.cargar_usuario(),'laboratorios': laboratorios, 'mensaje': mensaje})
   