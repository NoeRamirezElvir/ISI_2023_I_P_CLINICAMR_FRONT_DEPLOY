from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_parametros_generales(request):
    response = requests.get(url+'parametrosgenerales/')
    if response.status_code == 200:
        data = response.json()
        parametrosgenerales = data['parametrosgenerales']
    else:
        parametrosgenerales = []
    context = {'parametrosgenerales': parametrosgenerales}
    return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)

def crear_parametros_generales(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            valor = request.POST['valor']
            registro_temp = {'nombre': nombre,'descripcion': descripcion, 'valor': valor}
            response = requests.post(url+'parametrosgenerales/', json={'nombre': nombre,'descripcion': descripcion, 'valor': valor})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_parametros_generales','logs_parametros_generales')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_parametros_generales','logs_parametros_generales')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'parametros_generales/parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'parametrosgenerales': registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_parametros_generales','logs_parametros_generales')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'parametros_generales/parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'parametrosgenerales': registro_temp})
        else:
            logger = definir_log_info('crear_parametros_generales','logs_parametros_generales')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'parametros_generales/parametros_generales.html',{'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_parametros_generales','logs_parametros_generales')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'parametros_generales/parametros_generales.html',{'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario()})
   

def abrir_actualizar_parametros_generales(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'parametrosgenerales/busqueda/id/'+str(request.POST['id_parametrosgenerales']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                parametrosgenerales = data['parametrosgenerales']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_parametros_generales','logs_parametros_generales')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_parametros_generales','logs_parametros_generales')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                parametrosgenerales = []
                logger = definir_log_info('abrir_actualizar_parametros_generales','logs_parametros_generales')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_parametros_generales','logs_parametros_generales')
        logger.exception("Ocurrio una excepcion:" + str(e))
        parametrosgenerales = []
        context = {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
        return render(request, 'parametros_generales/Actualizar_parametros_generales.html', context)
   

def actualizar_parametros_generales(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            valor = request.POST['valor']
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'parametrosgenerales/id/{idTemporal}', json={'nombre': nombre,'descripcion': descripcion, 'valor': valor})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'parametrosgenerales/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            parametrosgenerales = data['parametrosgenerales']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_parametros_generales','logs_parametros_generales')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'parametrosgenerales':parametrosgenerales })
            else:
                mensaje = rsp['message']      
                logger = definir_log_info('actualizar_parametros_generales','logs_parametros_generales')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                      #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'parametrosgenerales':parametrosgenerales})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'parametrosgenerales/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                parametrosgenerales = data['parametrosgenerales']
                mensaje = data['message']
                logger = definir_log_info('actualizar_parametros_generales','logs_parametros_generales')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_parametros_generales','logs_parametros_generales')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'parametrosgenerales':parametrosgenerales})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_parametros_generales','logs_parametros_generales')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+f'parametrosgenerales/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            parametrosgenerales = data['parametrosgenerales']
            mensaje = data['message']
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales})
        else:
            mensaje = data['message']
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'parametrosgenerales':parametrosgenerales})
    

def eliminar_parametros_generales(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'parametrosgenerales/id/{idTemporal}')
            res = response.json()
            rsp_parametrosgenerales = requests.get(url + 'parametrosgenerales/') 
            if rsp_parametrosgenerales.status_code == 200:
                data = rsp_parametrosgenerales.json()
                parametrosgenerales = data['parametrosgenerales']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_parametros_generales','logs_parametros_generales')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_parametros_generales','logs_parametros_generales')
                    logger.info("No se ha podido eliminar el registro")
            else:
                parametrosgenerales = []
                logger = definir_log_info('eliminar_parametros_generales','logs_parametros_generales')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje}
            return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)  
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_parametros_generales','logs_parametros_generales')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_parametrosgenerales = requests.get(url + 'parametrosgenerales/') 
        if rsp_parametrosgenerales.status_code == 200:
            data = rsp_parametrosgenerales.json()
            parametrosgenerales = data['parametrosgenerales']
        else:
            parametrosgenerales = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'error': mensaje}
        return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)  
        
def buscar_parametros_generales(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'parametrosgenerales/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    parametrosgenerales = {}
                    parametrosgenerales = data['parametrosgenerales']
                    if parametrosgenerales != []:   
                        logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
                    return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)       
                else:
                    parametrosgenerales = []
                    mensaje = 'No se encontraron parametros generales'
                    logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
      
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    parametrosgenerales = {}
                    parametrosgenerales = data['parametrosgenerales']
                    if parametrosgenerales != []:   
                        logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
                    return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)
                else:
                    parametrosgenerales = []
                    mensaje = 'No se encontraron parametros generales'
                    logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
      
        else:
            response = requests.get(url+'parametrosgenerales/')
            if response.status_code == 200:
                data = response.json()
                parametrosgenerales = data['parametrosgenerales']
                mensaje = data['message']   
                if parametrosgenerales != []:   
                    logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
            else:
                parametrosgenerales = []
                mensaje = 'No se encontraron parametros generales'
                logger = definir_log_info('buscar_parametros_generales','logs_parametros_generales')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_parametros_generales','logs_parametros_generales')
        logger.exception("Ocurrio una excepcion:" + str(e))    
        response = requests.get(url+'parametrosgenerales/')
        if response.status_code == 200:
            data = response.json()
            parametrosgenerales = data['parametrosgenerales']
            mensaje = data['message']   
            return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
        else:
            parametrosgenerales = []
            mensaje = 'No se encontraron parametros generales'
        return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'reportes_lista':DatosReportes.cargar_lista_parametros_generales(),'reportes_usuarios':DatosReportes.cargar_usuario(),'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
     