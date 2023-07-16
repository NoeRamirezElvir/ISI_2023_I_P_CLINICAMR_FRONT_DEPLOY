from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info
from ..views_api.views_datos_permisos import cargar_datos



url = 'https://clinicamr.onrender.com/api/'
def listar_sintomas(request):
    response = requests.get(url+'sintomas/')
    if response.status_code == 200:
        data = response.json()
        sintomas = data['sintomas']
    else:
        sintomas = []
    context = {'sintomas': sintomas}
    return render(request, 'sintomas/buscar_sintomas.html', context)

def crear_sintomas(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            registro_temp={'nombre': nombre, 'descripcion': descripcion}
            response = requests.post(url+'sintomas/', json={'nombre': nombre, 'descripcion': descripcion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_sintomas','logs_sintomas')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_sintomas','logs_sintomas')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'sintomas/sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_sintomas','logs_sintomas')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'sintomas/sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_sintomas','logs_sintomas')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'sintomas/sintomas.html',{'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_sintomas','logs_sintomas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'sintomas/sintomas.html',{'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
   

def abrir_actualizar_sintomas(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'sintomas/busqueda/id/'+str(request.POST['id_sintoma']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                sintomas = data['sintomas']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_sintomas','logs_sintomas')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_sintomas','logs_sintomas')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                sintomas = []
                logger = definir_log_info('abrir_actualizar_sintomas','logs_sintomas')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'sintomas/actualizar_sintomas.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_sintomas','logs_sintomas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        sintomas = []
        context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
        return render(request, 'sintomas/actualizar_sintomas.html', context)
    
def actualizar_sintomas(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']

            response = requests.put(url+f'sintomas/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
            rsp =  response.json()

            res = requests.get(url+f'sintomas/busqueda/id/{idTemporal}')
            data = res.json()
            sintomas = data['sintomas']
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_sintomas','logs_sintomas')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':sintomas })
            else:
                mensaje = rsp['message']     
                logger = definir_log_info('actualizar_sintomas','logs_sintomas')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)                       #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':sintomas})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'sintomas/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                sintomas = data['sintomas']
                mensaje = data['message']
                logger = definir_log_info('actualizar_sintomas','logs_sintomas')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_sintomas','logs_sintomas')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':sintomas})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_sintomas','logs_sintomas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        mensaje = data['message']
        return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':[]})
    

def eliminar_sintomas(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'sintomas/id/{idTemporal}')
            res = response.json()
            rsp_cargos = requests.get(url + 'sintomas/') 
            if rsp_cargos.status_code == 200:
                data = rsp_cargos.json()
                sintomas = data['sintomas']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_sintomas','logs_sintomas')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_sintomas','logs_sintomas')
                    logger.info("No se ha podido eliminar el registro")
            else:
                sintomas = []
                logger = definir_log_info('eliminar_sintomas','logs_sintomas')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje}
            return render(request, 'sintomas/buscar_sintomas.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_sintomas','logs_sintomas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_cargos = requests.get(url + 'sintomas/') 
        if rsp_cargos.status_code == 200:
            data = rsp_cargos.json()
            sintomas = data['sintomas']
        else:
            sintomas = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'error': mensaje}
        return render(request, 'sintomas/buscar_sintomas.html', context)     
        
def buscar_sintomas(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'sintomas/busqueda/'
        if valor is not None and (len(valor)>0):           
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    sintomas = {}
                    sintomas = data['sintomas']
                    if sintomas != []:   
                        logger = definir_log_info('buscar_sintomas','logs_sintomas')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_sintomas','logs_sintomas')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
                    return render(request, 'sintomas/buscar_sintomas.html', context)
                else:
                    sintomas = []
                    mensaje = 'No se encontraron sintomas'
                    logger = definir_log_info('buscar_sintomas','logs_sintomas')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
           
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    sintomas = {}
                    sintomas = data['sintomas']
                    if sintomas != []:   
                        logger = definir_log_info('buscar_sintomas','logs_sintomas')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_sintomas','logs_sintomas')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
                    return render(request, 'sintomas/buscar_sintomas.html', context)
                else:
                    sintomas = []
                    mensaje = 'No se encontraron sintomas'
                    logger = definir_log_info('buscar_sintomas','logs_sintomas')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
           
        else:
            response = requests.get(url+'sintomas/')
            if response.status_code == 200:
                data = response.json()
                sintomas = data['sintomas']
                mensaje = data['message']  
                if sintomas != []:   
                    logger = definir_log_info('buscar_sintomas','logs_sintomas')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_sintomas','logs_sintomas')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
            else:
                sintomas = []
                mensaje = 'No se encontraron sintomas'
                logger = definir_log_info('buscar_sintomas','logs_sintomas')
                logger.info(f"No se obtuvieron los registros:{mensaje}")

            return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_sintomas','logs_sintomas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        sintomas = []
        return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
   