from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_pantallas(request):
    response = requests.get(url+'pantallas/')
    if response.status_code == 200:
        data = response.json()
        pantallas = data['pantallas']
        if not pantallas:
            pantallas = []
    else:
        pantallas = []
    context = {'pantallas': pantallas}
    return render(request, 'pantallas/Buscar_pantallas.html', context)


def crear_pantallas(request):
    try:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            registro_temp={'nombre': nombre, 'descripcion': descripcion}
            response = requests.post(url+'pantallas/', json={'nombre': nombre, 'descripcion': descripcion})
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_pantallas','logs_pantallas')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_pantallas','logs_pantallas')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'pantallas/pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_pantallas','logs_pantallas')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'pantallas/pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            logger = definir_log_info('crear_pantallas','logs_pantallas')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'pantallas/pantallas.html',{'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_pantallas','logs_pantallas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'pantallas/pantallas.html',{'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje':mensaje})
    

def abrir_actualizar_pantallas(request):
    try:
        if request.method == 'POST':
            resp = requests.get(url+'pantallas/busqueda/id/'+str(request.POST['id_pantallas']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                pantallas = data['pantallas']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_pantallas','logs_pantallas')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_pantallas','logs_pantallas')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                pantallas = []
                logger = definir_log_info('abrir_actualizar_pantallas','logs_pantallas')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje':mensaje}
            mensaje = data['message']
            return render(request, 'pantallas/pantallas_Actualizar.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_pantallas','logs_pantallas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        pantallas = []
        context = {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje':mensaje}
        return render(request, 'pantallas/pantallas_Actualizar.html', context)

def actualizar_pantallas(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'pantallas/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'pantallas/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            pantallas = data['pantallas']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_pantallas','logs_pantallas')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'pantallas/pantallas_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'pantallas':pantallas })
            else:
                mensaje = rsp['message']   
                logger = definir_log_info('actualizar_pantallas','logs_pantallas')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'pantallas/pantallas_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'pantallas':pantallas})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'pantallas/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                usuario = data['pantallas']
                mensaje = data['message']
                logger = definir_log_info('actualizar_pantallas','logs_pantallas')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'pantallas/pantallas_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_pantallas','logs_pantallas')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                return render(request, 'pantallas/pantallas_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'pantallas':pantallas})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_pantallas','logs_pantallas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'pantallas/pantallas_Actualizar.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'pantallas':pantallas})
       
def eliminar_pantallas(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'pantallas/id/{idTemporal}')
            res = response.json()
            rsp_pantallas = requests.get(url + 'pantallas/') 
            if rsp_pantallas.status_code == 200:
                data = rsp_pantallas.json()
                pantallas = data['pantallas']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_pantallas','logs_pantallas')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_pantallas','logs_pantallas')
                    logger.info("No se ha podido eliminar el registro")
            else:
                pantallas = []
                logger = definir_log_info('eliminar_pantallas','logs_pantallas')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje': mensaje}
            return render(request, 'pantallas/Buscar_pantallas.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_pantallas','logs_pantallas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_pantallas = requests.get(url + 'pantallas/') 
        if rsp_pantallas.status_code == 200:
            data = rsp_pantallas.json()
            pantallas = data['pantallas']
        else:
            pantallas = []
        mensaje += ' No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'error': mensaje}
        return render(request, 'pantallas/Buscar_pantallas.html', context)     

def buscar_pantallas(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'pantallas/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pantallas = {}
                    pantallas = data['pantallas']
                    if pantallas != []:   
                        logger = definir_log_info('buscar_pantallas','logs_pantallas')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_pantallas','logs_pantallas')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje':mensaje}
                    return render(request, 'pantallas/Buscar_pantallas.html', context)     
                else:
                    pantallas = []
                    mensaje = 'No se encontraron pantallas'
                    logger = definir_log_info('buscar_pantallas','logs_pantallas')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'pantallas/Buscar_pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje': mensaje})  
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pantallas = {}
                    pantallas = data['pantallas']
                    if pantallas != []:   
                        logger = definir_log_info('buscar_pantallas','logs_pantallas')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_pantallas','logs_pantallas')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje':mensaje}
                    return render(request, 'pantallas/Buscar_pantallas.html', context)
                else:
                    pantallas = []
                    mensaje = 'No se encontraron pantallas'
                    logger = definir_log_info('buscar_pantallas','logs_pantallas')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'pantallas/Buscar_pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'pantallas/')
            if response.status_code == 200:
                data = response.json()
                pantallas = data['pantallas']
                mensaje = data['message']   
                if pantallas != []:   
                    logger = definir_log_info('buscar_pantallas','logs_pantallas')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_pantallas','logs_pantallas')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")
                return render(request, 'pantallas/Buscar_pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje': mensaje})
            else:
                pantallas = []
                mensaje = 'No se encontraron pantallas'
                logger = definir_log_info('buscar_pantallas','logs_pantallas')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'pantallas/Buscar_pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_pantallas','logs_pantallas')
        logger.exception("Ocurrio una excepcion:" + str(e))
        pantallas = []
        return render(request, 'pantallas/Buscar_pantallas.html', {'reportes_lista':DatosReportes.cargar_lista_pantallas(),'reportes_usuarios':DatosReportes.cargar_usuario(),'pantallas': pantallas, 'mensaje': mensaje})
   