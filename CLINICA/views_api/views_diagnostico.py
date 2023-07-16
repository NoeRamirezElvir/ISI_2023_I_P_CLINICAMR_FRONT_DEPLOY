import ast
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.views_datos_permisos import cargar_datos


from ..views_api.logger import definir_log_info

url = 'https://clinicamr.onrender.com/api/'
def listar_diagnosticos(request):
    response = requests.get(url+'diagnostico/')
    if response.status_code == 200:
        data = response.json()
        diagnostico = data['diagnosticos']
    else:
        diagnostico = []
    context = {'diagnostico': diagnostico}
    return render(request, 'diagnostico/Buscar_diagnostico.html', context)


def crear_diagnosticos(request):
    #Se cargan las listas para los SELECT
    enfermedades = list_enfermedades()
    try:
        if request.method == 'POST':
            descripcion = request.POST['descripcion']
            valores_seleccionados_json = request.POST['valoresSeleccionados']
            valores_seleccionados = json.loads(valores_seleccionados_json)

            # Crear la lista de diccionarios para los sintomas seleccionados
            enfermedades_seleccionados = []
            for valor in valores_seleccionados:
                enfermedad = {}
                enfermedad['id'] = int(valor.split("-")[0])
                enfermedad['nombre'] = str(valor.split("-")[1])
                enfermedades_seleccionados.append(enfermedad)

            # Crear el diccionario final
            resultado = {}
            resultado['descripcion'] = descripcion
            resultado['idEnfermedades'] = enfermedades_seleccionados


            # Convertir el diccionario a JSON
            resultado_json = json.dumps(resultado)
            registro_temp = {'descripcion': descripcion, 'lista': enfermedades_seleccionados}
            
            response = requests.post(url+'diagnostico/', resultado_json)
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro exitoso':
                    logger = definir_log_info('crear_diagnostico','logs_diagnostico')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear_diagnostico','logs_diagnostico')
                    logger.debug(f"Se ha realizado un registro")
                return render(request, 'diagnostico/diagnostico.html', {'mensaje': mensaje, 'registro_temp':registro_temp, 'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                data = response.json()
                mensaje = data['message']
                logger = definir_log_info('crear_diagnostico','logs_diagnostico')
                logger.warning("No se pudo realizar el registro" + mensaje)
            return render(request, 'diagnostico/diagnostico.html', {'mensaje': "mensaje", 'registro_temp':registro_temp, 'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_diagnostico','logs_diagnostico')
            logger.debug('Entrando a la funcion de registro')
            return render(request, 'diagnostico/diagnostico.html', {'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_diagnostico','logs_diagnostico')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'diagnostico/diagnostico.html', {'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
     
def abrir_actualizar_diagnosticos(request):
    #Se cargan las listas para los SELECT
    enfermedades = list_enfermedades()
    try:
        if request.method == 'POST':
            resp = requests.get(url+'diagnostico/busqueda/id/'+str(request.POST['id_diagnostico']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('abrir_actualizar_diagnostico','logs_diagnostico')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar_diagnostico','logs_diagnostico')
                    logger.debug("Se obtuvo el registro correspondiente a la actualizacion: " + mensaje)
                diagnostico = data['diagnosticos'][0]
                id = diagnostico['id']
                descripcion = diagnostico['descripcion']
                idEnfermedades = diagnostico['idEnfermedades']
                # crear una lista de IDs de síntomas
                ids_Enfermedades = [{'id': idEnfermedades[str(key)]['id'], 'nombre': idEnfermedades[str(key)]['nombre']} for key in idEnfermedades]

                # crear un diccionario con los datos deseados
                registro_temp = {'id':id, 'descripcion': descripcion, 'lista': ids_Enfermedades}
            else:
                registro_temp = {}
                logger = definir_log_info('abrir_actualizar_diagnostico','logs_diagnostico')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)
            mensaje = data['message']
            context = {'registro_temp': registro_temp,'enfermedades': enfermedades, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'diagnostico/Actualizar_diagnostico.html', context)   
    except Exception as e:
        logger = definir_log_info('excepcion_diagnostico','logs_diagnostico')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'enfermedades': enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'diagnostico/Actualizar_diagnostico.html', context)  
    
def actualizar_diagnosticos(request, id):
    enfermedades = list_enfermedades()
    try:
        if request.method == 'POST':
            idTemporal = id
            descripcion = request.POST['descripcion']
            valores_seleccionados_json = request.POST['valoresSeleccionados']
            valores_seleccionados = json.loads(valores_seleccionados_json)
            # Crear la lista de diccionarios para los sintomas seleccionados
            enfermedades_seleccionados = []
            for valor in valores_seleccionados:
                enfermedad = {}
                enfermedad['id'] = int(valor.split("-")[0])
                enfermedad['nombre'] = str(valor.split("-")[1])
                enfermedades_seleccionados.append(enfermedad)

            # Crear el diccionario final
            resultado = {}
            resultado['descripcion'] = descripcion
            resultado['idEnfermedades'] = enfermedades_seleccionados

            # Convertir el diccionario a JSON
            resultado_json = json.dumps(resultado)

            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'diagnostico/id/{idTemporal}', resultado_json)
            rsp =  response.json()

            #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
            res = requests.get(url+f'diagnostico/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            diagnosticos = data['diagnosticos'][0]
            id_diagnosticos = diagnosticos['id']
            descripcion = diagnosticos['descripcion']
            idEnfermedades = diagnosticos['idEnfermedades']
            # crear una lista de IDs de síntomas
            ids_enfermedades = [{'id': idEnfermedades[str(key)]['id'], 'nombre': idEnfermedades[str(key)]['nombre']} for key in idEnfermedades]

            # crear un diccionario con los datos deseados
            registro_temp = {'id':id_diagnosticos, 'descripcion': descripcion, 'lista': enfermedades_seleccionados}
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_diagnostico','logs_diagnostico')
                logger.debug("Se ha actualizado correctamente el registro: " + mensaje)
                return render(request, 'diagnostico/Actualizar_diagnostico.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = rsp['message']
                logger = definir_log_info('actualizar_diagnostico','logs_diagnostico')
                logger.warning("Se obtuvo una respuesta invalida: " + mensaje)
                return render(request, 'diagnostico/Actualizar_diagnostico.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            #Y aqui no se que hice la verdad
            response = requests.get(url+f'diagnostico/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                diagnosticos = data['diagnosticos'][0]
                id_diagnosticos = diagnosticos['id']
                descripcion = diagnosticos['descripcion']
                idEnfermedades = diagnosticos['idEnfermedades']
                # crear una lista de IDs de síntomas
                ids_enfermedades = [{'id': idEnfermedades[str(key)]['id'], 'nombre': idEnfermedades[str(key)]['nombre']} for key in idEnfermedades]
                logger = definir_log_info('actualizar_diagnostico','logs_diagnostico')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado")
                registro_temp = {'id':id_diagnosticos, 'descripcion': descripcion, 'lista': ids_enfermedades}
                return render(request, 'diagnostico/Actualizar_diagnostico.html', {'registro_temp': registro_temp, 'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('actualizar_diagnostico','logs_diagnostico')
                logger.debug("Se obtuvo la informacion del registro, anteriormente actualizado: " + mensaje)
                return render(request, 'diagnostico/Actualizar_diagnostico.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_diagnostico','logs_diagnostico')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'diagnostico/Actualizar_diagnostico.html', {'enfermedades':enfermedades,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    

def buscar_diagnosticos(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'diagnostico/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    diagnostico = {}
                    diagnostico = data['diagnosticos']
                    if diagnostico != []:   
                        logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                        logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")

                    context = {'diagnostico': diagnostico, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'diagnostico/Buscar_diagnostico.html', context) 
                else:
                    diagnostico = []
                    mensaje = 'No se encontraron registros'
                    logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                    logger.info(f"No se obtuvieron los registros:Filtrado(ID){valor} - {mensaje}")
                    return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        
            else:
                response = requests.get(url2+'descripcion/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    diagnostico = {}
                    diagnostico = data['diagnosticos']
                    if diagnostico != []:   
                        logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                        logger.debug(f"Se obtuvieron los registros:Filtrado(descripcion){valor} - {mensaje}")
                    else:
                        logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                        logger.info(f"No se obtuvieron los registros:Filtrado(descripcion){valor} - {mensaje}")
                    context = {'diagnostico': diagnostico, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'diagnostico/Buscar_diagnostico.html', context)
                else:
                    diagnostico = []
                    mensaje = 'No se encontraron registros'
                    logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                    logger.info(f"No se obtuvieron los registros:Filtrado(descripcion){valor} - {mensaje}")
                    return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            response = requests.get(url+'diagnostico/')
            if response.status_code == 200:
                data = response.json()
                diagnostico = data['diagnosticos']
                mensaje = data['message'] 
                if diagnostico != []:   
                    logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                    logger.debug(f"Se obtuvieron los registros:{mensaje}")
                else:
                    logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                    logger.info(f"No se obtuvieron los registros:{mensaje}")  
                return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                diagnostico = []
                mensaje = 'No se encontraron registros'
                logger = definir_log_info('buscar_diagnostico','logs_diagnostico')
                logger.info(f"No se obtuvieron los registros:{mensaje}")
            return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        logger = definir_log_info('excepcion_diagnostico','logs_diagnostico')
        logger.exception("Ocurrio una excepcion:" + str(e))
        diagnostico = []
        mensaje = 'Ocurrio una excepcion'
        return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    

def eliminar_diagnosticos(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'diagnostico/id/{idTemporal}')
            res = response.json()
            rsp_diagnostico = requests.get(url + 'diagnostico/') 
            context ={}
            if rsp_diagnostico.status_code == 200:
                data = rsp_diagnostico.json()
                diagnostico = data['diagnosticos']
                logger = definir_log_info('eliminar_diagnostico','logs_diagnostico')
                logger.info("Registro eliminado correctamente")
                context = {'diagnostico': diagnostico,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            else:
                diagnostico = []
                mensaje = res['message']
                logger = definir_log_info('eliminar_diagnostico','logs_diagnostico')
                logger.warning("Se obtuvo una respuesta invalida" + mensaje)

                context = {'diagnostico': diagnostico, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'diagnostico/Buscar_diagnostico.html', context) 
    except Exception as e:
        logger = definir_log_info('excepcion_diagnostico','logs_diagnostico')
        logger.exception("Ocurrio una excepcion:" + str(e))

        rsp_diagnostico = requests.get(url + 'diagnostico/') 
        context ={}
        if  rsp_diagnostico.status_code == 200:
            data = rsp_diagnostico.json()
            diagnostico = data['diagnosticos']
            context = {'diagnostico': diagnostico,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        else:
            diagnostico = []
        mensaje = 'No se puede eliminar, esta siendo utilizando en otros registros'
        context = {'diagnostico': diagnostico, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_diagnostico(),'datos_permisos':cargar_datos(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'diagnostico/Buscar_diagnostico.html', context)


def list_enfermedades():
    rsp_enfermedades = requests.get(url+'enfermedades/')
    if rsp_enfermedades.status_code == 200:
        data = rsp_enfermedades.json()
        list_enfermedades = data['enfermedades']
        return list_enfermedades
    else:
        list_enfermedades = []
        return list_enfermedades
    

    