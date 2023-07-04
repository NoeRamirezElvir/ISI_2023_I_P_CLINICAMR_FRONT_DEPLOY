from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_correlativo(request):
    response = requests.get(url+'correlativo/')
    if response.status_code == 200:
        data = response.json()
        correlativo = data['correlativo']
    else:
        correlativo = []
    context = {'correlativo': correlativo}
    return render(request, 'correlativo/buscar_correlativo.html', context)

def crear_correlativo(request):
    try:
        
        if request.method == 'POST':
            cai = request.POST['cai']
            rangoInicial = int(request.POST['rangoInicial'])
            rangoFinal = int(request.POST['rangoFinal'])
            fechaLimiteEmision = request.POST['fechaLimiteEmision']
            
            

            registro_temp={'cai': cai, 
                        'rangoInicial': rangoInicial,
                        'rangoFinal': rangoFinal,                   
                        'fechaLimiteEmision': fechaLimiteEmision
                        }
            
            response = requests.post(url+'correlativo/', json={'cai': cai, 
                                                                'rangoInicial': rangoInicial,
                                                                'rangoFinal': rangoFinal,  
                                                                'fechaLimiteEmision': fechaLimiteEmision
                                                                })
            data = response.json()
            if response.status_code == 200:
            
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('error_crear','logs_correlativo')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear','logs_correlativo')
                    logger.debug(f"Se ha registrado un correlativo: Cai={cai}")

                return render(request, 'correlativo/correlativo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_crear','logs_correlativo')
                logger.warning("No se pudo crear el correlativo: " + mensaje)
                return render(request, 'correlativo/correlativo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_correlativo','logs_correlativo')
            logger.debug('Entrando a la funcion crear correlativo')
            return render(request, 'correlativo/correlativo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_correlativo','logs_correlativo')
        logger.exception("Ocurrio una excepcion:" + str(e))
    return render(request, 'correlativo/correlativo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})       


def abrir_actualizar_correlativo(request):
    try:
    
        if request.method == 'POST':
            print(request.POST['id_correlativo'])
            resp = requests.get(url+'correlativo/busqueda/id/'+str(request.POST['id_correlativo']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                correlativo = data['correlativo']
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('error_abrir_actualizar','logs_correlativo')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar','logs_correlativo')
                    logger.debug("Se obtuvo el correlativo correspondiente a la actualizacion: " + mensaje)
            else:
                correlativo = []
                logger = definir_log_info('error_abrir_actualizar','logs_correlativo')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
            context = {'correlativo': correlativo, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            mensaje = data['message']
            return render(request, 'correlativo/actualizar_correlativo.html', context)
    except Exception as e:
        logger = definir_log_info('excepcion_correlativo','logs_correlativo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'correlativo': correlativo, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'correlativo/actualizar_correlativo.html', context)

def actualizar_correlativo(request, id):
    
    try:
        if request.method == 'POST':
            idTemporal = id
            cai = request.POST['cai']
            rangoInicial = int(request.POST['rangoInicial'])
            rangoFinal = int(request.POST['rangoFinal'])  
            fechaLimiteEmision = request.POST['fechaLimiteEmision']
            consecutivo = request.POST['consecutivo']
            
            
            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'correlativo/id/{idTemporal}', json={'cai': cai, 
                                                                                'rangoInicial': rangoInicial,
                                                                                'rangoFinal': rangoFinal,
                                                                                'fechaLimiteEmision': fechaLimiteEmision,
                                                                                'consecutivo':consecutivo
                                                                                })
            #obtener la respuesta en la variable rsp
            rsp =  response.json()
            #Ya que se necesita llenar de nuevo el formulario se busca el correlativo relacionado con el id
            res = requests.get(url+f'correlativo/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            correlativo = data['correlativo']
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar','logs_correlativo')
                logger.debug("Actualizacion correcta del correlativo: " + mensaje)
                return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo ,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                logger = definir_log_info('error_actualizar','logs_correlativo')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'correlativo/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                correlativo = data['correlativo']
                mensaje = data['message']
                logger = definir_log_info('actualizar','logs_correlativo')
                logger.debug("Obteniendo informacion del correlativo: " + mensaje)
                return render(request, 'correlativo/actualizar_correlativo.html', {'correlativo':correlativo,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_actualizar','logs_correlativo')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_correlativo','logs_correlativo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def eliminar_correlativo(request, id):
    
    
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'correlativo/id/{idTemporal}')
            res = response.json()
            rsp_correlativo = requests.get(url + 'correlativo/') 
            if rsp_correlativo.status_code == 200:
                data = rsp_correlativo.json()
                correlativo = data['correlativo']
                logger = definir_log_info('eliminar_correlativo','logs_correlativo')
                logger.info("correlativo eliminado correctamente")
            else:
                correlativo = []
                logger = definir_log_info('error_eliminar_correlativo','logs_correlativo')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'correlativo/buscar_correlativo.html', context)     
    except Exception as e:
        rsp_correlativo = requests.get(url + 'correlativo/') 
        if rsp_correlativo.status_code == 200:
            data = rsp_correlativo.json()
            correlativo = data['correlativo']
        else:
            correlativo = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        logger = definir_log_info('excepcion_correlativo','logs_correlativo')
        logger.exception("Ocurrio una excepcion:" + str(mensaje))
        context = {'correlativo': correlativo, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'correlativo/buscar_correlativo.html', context)     
         
def buscar_correlativo(request):
    try:    
        
        valor = request.GET.get('buscador', None)
        url2 = url + 'correlativo/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    correlativo = {}
                    correlativo = data['correlativo']
                    logger = definir_log_info('buscar_correlativo','logs_correlativo')
                    logger.debug("Se obtuvo el correlativo especifico(filtrado por ID): " + mensaje)
                    context = {'correlativo': correlativo, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'correlativo/buscar_correlativo.html', context)
                else:
                    correlativo = []
                    mensaje = 'No se encontraron correlativos'
                    logger = definir_log_info('error_buscar_correlativo','logs_correlativo')
                    logger.debug("No se obtuvo el correlativo especifico(filtrado por ID): " + mensaje)
                    return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
          
            else:
                response = requests.get(url2+'cai/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    correlativo = {}
                    correlativo = data['correlativo']
                    logger = definir_log_info('buscar_correlativo','logs_correlativo')
                    logger.debug("Se obtuvo el correlativo especifico(filtrado por nombre): " + mensaje)
                    context = {'correlativo': correlativo, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'correlativo/buscar_correlativo.html', context)
                else:
                    correlativo = []
                    mensaje = 'No se encontraron correlativos'
                    logger = definir_log_info('error_buscar_correlativo','logs_correlativo')
                    logger.debug("No se obtuvo el correlativo especifico(filtrado por ID): " + mensaje)
                    return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
        else:
            response = requests.get(url+'correlativo/')
            if response.status_code == 200:
                data = response.json()
                correlativo = data['correlativo']
                mensaje = data['message']   
                logger = definir_log_info('buscar_correlativo','logs_correlativo')
                logger.debug("Se obtuvieron todos los correlativos: " + mensaje )
                return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                correlativo = []
                mensaje = 'No se encontraron correlativos'
                logger = definir_log_info('error_buscar_correlativo','logs_correlativo')
                logger.debug("No se obtuvo el correlativo especifico(filtrado por ID): " + mensaje)
            return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
    except Exception as e:
        logger = definir_log_info('excepcion_correlativo','logs_correlativo')
        logger.exception("Ocurrio una excepcion:" + str(e))
        response = requests.get(url+'correlativo/')
        if response.status_code == 200:
            data = response.json()
            correlativo = data['correlativo']
            mensaje = data['message']  
            logger = definir_log_info('buscar_correlativo','logs_correlativo')
            logger.debug("Se obtuvieron todos los correlativos: " + mensaje ) 
            return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            correlativo = []
            mensaje = 'No se encontraron correlativos'
            logger = definir_log_info('error_buscar_correlativo','logs_correlativo')
            logger.debug("No se pudo obtener informacion de correlativos: " + mensaje)
        return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_sar(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    