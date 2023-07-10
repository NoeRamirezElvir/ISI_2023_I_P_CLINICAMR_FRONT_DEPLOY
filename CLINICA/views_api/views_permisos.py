from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info




url = 'https://clinicamr.onrender.com/api/'
def listar_permisos(request):
    response = requests.get(url+'permisos/')
    if response.status_code == 200:
        data = response.json()
        permisos = data['permisos']
    else:
        permisos = []
    context = {'permisos': permisos}
    return render(request, 'permisos/buscar_permiso.html', context)

def crear_permisos(request):
    acciones_list = list_acciones()
    cargos_list = list_cargos()
    pantallas_list = list_pantallas()
    try:
        if request.method == 'POST':
            idAcciones = int(request.POST['idAcciones'])
            idCargoEmpleado = int(request.POST['idCargoEmpleado'])
            idPantallas = int(request.POST['idPantallas'])
            
            activo = int(request.POST['payment_method'])
            
            registro_temp = {'idAcciones': idAcciones, 
                            'idCargoEmpleado': idCargoEmpleado, 
                            'idPantallas': idPantallas, 
                            'activo':activo
                            }
            response = requests.post(url+'permisos/', json={'idAcciones': idAcciones, 
                                                        'idCargoEmpleado': idCargoEmpleado, 
                                                        'idPantallas': idPantallas, 
                                                        'activo':activo
                                                        })
            data = response.json()
            print (data)
            if response.status_code == 200:
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('crear_permisos','logs_permisos')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_permisos','logs_permisos')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'permisos/permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 
                                                                'registro_temp':registro_temp,
                                                                'acciones_list':acciones_list, 
                                                                'cargos_list':cargos_list, 
                                                                'pantallas_list':pantallas_list})
            else:
                mensaje = data['message']
                logger = definir_log_info('crear_permisos','logs_permisos')
                logger.warning("No se pudo realizar el registro" + mensaje)
                return render(request, 'permisos/permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'acciones_list':acciones_list, 'cargos_list':cargos_list, 'pantallas_list':pantallas_list})
        else:
            logger = definir_log_info('crear_permisos','logs_permisos')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'permisos/permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'acciones_list':acciones_list, 
                                                            'cargos_list':cargos_list, 
                                                            'pantallas_list':pantallas_list})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_permisos','logs_permisos')
        logger.exception("Ocurrio una excepcion:" + str(e))   
        return render(request, 'permisos/permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                         'acciones_list':acciones_list, 
                                                        'cargos_list':cargos_list, 
                                                        'pantallas_list':pantallas_list})

    
def abrir_actualizar_permisos(request):
    acciones_list = list_acciones()
    cargos_list = list_cargos()
    pantallas_list = list_pantallas()
    try:
        if request.method == 'POST':
            
            resp = requests.get(url+'permisos/busqueda/id/'+str(request.POST['id_permisos']))
            data = resp.json()
            mensaje = data['message']
            
            
            if resp.status_code == 200:
                permisos = data['permisos']
                mensaje = data['message']

                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_permisos','logs_permisos')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_permisos','logs_permisos')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
            else:
                permisos = []
                logger = definir_log_info('abrir_actualizar_permisos','logs_permisos')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje':mensaje,
                                                'acciones_list':acciones_list,
                                                'cargos_list':cargos_list,
                                                'pantallas_list':pantallas_list                                          
                                                }
            mensaje = data['message']
            print(context)
            return render(request, 'permisos/actualizar_permiso.html', context)
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_permisos','logs_permisos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        permisos = []
        context = {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje':mensaje,
                                            'acciones_list':acciones_list,
                                            'cargos_list':cargos_list,
                                            'pantallas_list':pantallas_list                                          
                                            }
        return render(request, 'permisos/actualizar_permiso.html', context)
      
def actualizar_permisos(request, id):
    acciones_list = list_acciones()
    cargos_list = list_cargos()
    pantallas_list = list_pantallas()
    try:
        if request.method == 'POST':
            idTemporal = id
            idAcciones = int(request.POST['idAcciones'])
            idCargoEmpleado = int(request.POST['idCargoEmpleado'])
            idPantallas = int(request.POST['idPantallas'])
            activo = request.POST['payment_method']
            

            response = requests.put(url+f'permisos/id/{idTemporal}', json={'idAcciones': idAcciones, 
                                                                            'idCargoEmpleado': idCargoEmpleado, 
                                                                            'idPantallas': idPantallas, 
                                                                            'activo':activo, 
                                                                            })

            rsp =  response.json()
            res = requests.get(url+f'permisos/busqueda/id/{idTemporal}')
            data = res.json()
            permisos = data['permisos']
            
            
            
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_permisos','logs_permisos')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'permisos/actualizar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                            'mensaje': mensaje,
                                                                            'permisos':permisos,
                                                                            'acciones_list':acciones_list,
                                                                            'cargos_list':cargos_list,
                                                                            'pantallas_list':pantallas_list                                          
                                                                                                    })
            else:                                                   
                mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
                logger = definir_log_info('actualizar_permisos','logs_permisos')
                logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'permisos/actualizar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                            'mensaje': mensaje,
                                                                            'permisos':permisos,
                                                                            'acciones_list':acciones_list,
                                                                            'cargos_list':cargos_list,
                                                                            'pantallas_list':pantallas_list })
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'permisos/busqueda/id/{idTemporal}')
            data = response.json()
            if response.status_code == 200:
                permisos = data['permisos']
                mensaje = data['message']
                logger = definir_log_info('actualizar_permisos','logs_permisos')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                return render(request, 'permisos/actualizar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                            'permisos':permisos,
                                                                            'acciones_list':acciones_list,
                                                                            'cargos_list':cargos_list,
                                                                            'pantallas_list':pantallas_list})
            else:
                mensaje = data['message']
                print(permisos)
                logger = definir_log_info('actualizar_permisos','logs_permisos')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
                
                return render(request, 'permisos/actualizar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                            'mensaje': mensaje,
                                                                            'permisos':permisos,
                                                                            'acciones_list':acciones_list,
                                                                            'cargos_list':cargos_list,
                                                                            'pantallas_list':pantallas_list })
         
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_permisos','logs_permisos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'permisos/actualizar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),
                                                                    'mensaje': mensaje,
                                                                    'permisos':{},
                                                                    'acciones_list':acciones_list,
                                                                    'cargos_list':cargos_list,
                                                                    'pantallas_list':pantallas_list })


def eliminar_permisos(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'permisos/id/{idTemporal}')
            res = response.json()
            rsp_permisos = requests.get(url + 'permisos/') 
            if rsp_permisos.status_code == 200:
                data = rsp_permisos.json()
                permisos = data['permisos']
                if response.json()['message'] == 'Registro Eliminado':
                    logger = definir_log_info('eliminar_permisos','logs_permisos')
                    logger.info("Registro eliminado correctamente")
                else:
                    logger = definir_log_info('eliminar_permisos','logs_permisos')
                    logger.info("No se ha podido eliminar el registro")
            else:
                permisos = []
                logger = definir_log_info('eliminar_permisos','logs_permisos')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje': mensaje}
            return render(request, 'permisos/buscar_permiso.html', context)     
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_permisos','logs_permisos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        rsp_permisos = requests.get(url + 'permisos/') 
        if rsp_permisos.status_code == 200:
            data = rsp_permisos.json()
            permisos = data['permisos']
        else:
            permisos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'error': mensaje}
        return render(request, 'permisos/buscar_permiso.html', context)     
     
def buscar_permisos(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'permisos/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    permisos = {}
                    permisos = data['permisos']
                    if permisos != []:   
                        logger = definir_log_info('buscar_permisos','logs_permisos')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_permisos','logs_permisos')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje':mensaje}
                    return render(request, 'permisos/buscar_permiso.html', context)
                
            else:        
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    permisos = {}
                    permisos = data['permisos']
                    if permisos != []:   
                        logger = definir_log_info('buscar_permisos','logs_permisos')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_permisos','logs_permisos')
                        logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    context = {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje':mensaje}
                    return render(request, 'permisos/buscar_permiso.html', context)
                else:
                    permisos = []
                    mensaje = 'No se encontraron muestras'
                    logger = definir_log_info('buscar_permisos','logs_permisos')
                    logger.info(f"No se obtuvieron los registros:Filtrado(nombre){valor} - {mensaje}")
                    return render(request, 'permisos/buscar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'permisos/')
            if response.status_code == 200:
                data = response.json()
                permisos = data['permisos']
                mensaje = data['message']
                if permisos != []:   
                    logger = definir_log_info('buscar_permisos','logs_permisos')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_permisos','logs_permisos')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")   
                return render(request, 'permisos/buscar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje': mensaje})
            
            else:
                permisos = []
                mensaje = 'No se encontraron permisos'
                logger = definir_log_info('buscar_permisos','logs_permisos')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'permisos/buscar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje': mensaje})
    except Exception as e:
        mensaje = 'Ocurrio una excepcion'
        logger = definir_log_info('excepcion_permisos','logs_permisos')
        logger.exception("Ocurrio una excepcion:" + str(e))
        permisos = []
        return render(request, 'permisos/buscar_permiso.html', {'reportes_lista':DatosReportes.cargar_lista_permisos(),'reportes_usuarios':DatosReportes.cargar_usuario(),'permisos': permisos, 'mensaje': mensaje})
   

def list_acciones():
    rsp_acciones = requests.get(url+'acciones/')
    if rsp_acciones.status_code == 200:
        data = rsp_acciones.json()
        acciones_list = data['acciones']
        return acciones_list
    else:
        acciones_list = []
        return acciones_list

def list_cargos():
    rsp_cargos= requests.get(url+'cargos/')
    if rsp_cargos.status_code == 200:
        data = rsp_cargos.json()
        cargos_list = data['cargos']
        return cargos_list
    else:
        cargos_list = []
        return cargos_list
    
def list_pantallas():
    rsp_pantallas= requests.get(url+'pantallas/')
    if rsp_pantallas.status_code == 200:
        data = rsp_pantallas.json()
        pantallas_list = data['pantallas']
        return pantallas_list
    else:
        pantallas_list = []
        return pantallas_list