import ast
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes
from ..views_api.logger import definir_log_info



url = 'https://clinicamr.onrender.com/api/'
def listar_consulta(request):
    response = requests.get(url+'consultas/')
    if response.status_code == 200:
        data = response.json()
        consultas = data['consultas']
    else:
        consultas = []
    context = {'consultas': consultas}
    return render(request, 'consulta/buscar_consulta.html', context)


def crear_consulta(request):
    try:
        #Se cargan las listas para los SELECT
        diagnostico_list = list_diagnostico()
        cita_list = list_cita()
        tipo_list = list_tipo()

        if request.method == 'POST':
            idCita = int(request.POST['idCita'])
            idTipo = int(request.POST['idTipo'])
            recomendaciones = (request.POST['recomendaciones'])
            informacionAdicional = (request.POST['informacionAdicional'])
            valores_seleccionados_json = request.POST['valoresSeleccionados']
            valores_seleccionados = json.loads(valores_seleccionados_json)

            # Crear la lista de diccionarios para los sintomas seleccionados
            diagnosticos_seleccionados = []
            for valor in valores_seleccionados:
                diagnostico = {}
                diagnostico['id'] = int(valor.split("-")[0])
                diagnostico['descripcion'] = str(valor.split("-")[1])
                diagnosticos_seleccionados.append(diagnostico)

            # Crear el diccionario final
            resultado = {}
            resultado['idCita'] = idCita
            resultado['idTipo'] = idTipo
            resultado['recomendaciones'] = recomendaciones
            resultado['informacionAdicional'] = informacionAdicional
            resultado['idDiagnostico'] = diagnosticos_seleccionados


            # Convertir el diccionario a JSON
            resultado_json = json.dumps(resultado)
            registro_temp = {'idCita': idCita,'idTipo': idTipo,'recomendaciones': recomendaciones,'informacionAdicional': informacionAdicional, 'lista': diagnosticos_seleccionados}
            
            response = requests.post(url+'consultas/', resultado_json)
            data={}
            if response.status_code == 200:
                data = response.json()
                mensaje = data['message']
                if mensaje != 'Registro Exitoso.':
                    logger = definir_log_info('error_crear','logs_consulta')
                    logger.info("Se obtuvo una respuesta invalida: " + mensaje)
                else:
                    logger = definir_log_info('crear','logs_consulta')
                    logger.debug(f"Se ha registrado un consulta: idCita={idCita}")
                return render(request, 'consulta/consulta.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                data = response.json()
                mensaje = data['message']
                logger = definir_log_info('error_crear','logs_consulta')
                logger.warning("No se obtuvo respuesta del servidor: " + mensaje)
            return render(request, 'consulta/consulta.html', {'mensaje': "mensaje", 'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('crear_consulta','logs_consulta')
            logger.debug('Entrando a la funcion crear consulta')
            return render(request, 'consulta/consulta.html', {'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})

    except Exception as e:
        logger = definir_log_info('excepcion_consulta','logs_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'consulta/consulta.html', {'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def abrir_actualizar_consulta(request):
    try:    
        #Se cargan las listas para los SELECT
        diagnostico_list = list_diagnostico()
        cita_list = list_cita()
        tipo_list = list_tipo()
        
        
        if request.method == 'POST':
            resp = requests.get(url+'consultas/busqueda/id/'+str(request.POST['id_consulta']))
            data = resp.json()
            mensaje = data['message']
            if resp.status_code == 200:
                data = resp.json()
                mensaje = data['message']
                if mensaje != 'Consulta exitosa':
                    logger = definir_log_info('error_abrir_actualizar','logs_consulta')
                    logger.info("Se obtuvo una respuesta invalida" + mensaje)
                else:
                    logger = definir_log_info('abrir_actualizar','logs_consulta')
                    logger.debug("Se obtuvo el consulta correspondiente a la actualizacion: " + mensaje)

                consultas = data['consultas'][0]
                id = consultas['id']
                idCita = consultas['idCita']
                idTipo = consultas['idTipo']
                recomendaciones = consultas['recomendaciones']
                informacionAdicional = consultas['informacionAdicional']
                idDiagnostico = consultas['idDiagnostico']
                # crear una lista de IDs de síntomas
                ids_diagnosticos = [{'id': idDiagnostico[str(key)]['id'], 'descripcion': idDiagnostico[str(key)]['descripcion']} for key in idDiagnostico]

                # crear un diccionario con los datos deseados
                registro_temp = {'id':id, 'idCita': idCita,'idTipo': idTipo,'recomendaciones': recomendaciones,'informacionAdicional': informacionAdicional, 'lista': ids_diagnosticos}
            else:
                registro_temp = {}
                logger = definir_log_info('error_abrir_actualizar','logs_consulta')
                logger.warning("Se obtuvo una respuesta invalida")
            context = {'registro_temp': registro_temp,'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            mensaje = data['message']
            return render(request, 'consulta/actualizar_consulta.html', context)   

    except Exception as e:
        logger = definir_log_info('excepcion_consulta','logs_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        context = {'consultas': consultas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'consultas/consultaactualizar.html', context)
    

def actualizar_consulta(request, id):
    diagnostico_list = list_diagnostico()
    cita_list = list_cita()
    tipo_list = list_tipo()
    try:
        if request.method == 'POST':
            idTemporal = id
            idCita = int(request.POST['idCita'])
            idTipo = int(request.POST['idTipo'])
            recomendaciones = (request.POST['recomendaciones'])
            informacionAdicional = (request.POST['informacionAdicional'])
            valores_seleccionados_json = request.POST['valoresSeleccionados']
            valores_seleccionados = json.loads(valores_seleccionados_json)
            # Crear la lista de diccionarios para los sintomas seleccionados
            diagnosticos_seleccionados = []
            for valor in valores_seleccionados:
                diagnostico = {}
                diagnostico['id'] = int(valor.split("-")[0])
                diagnostico['descripcion'] = str(valor.split("-")[1])
                diagnosticos_seleccionados.append(diagnostico)

            # Crear el diccionario final
            resultado = {}
            resultado['idCita'] = idCita
            resultado['idTipo'] = idTipo
            resultado['recomendaciones'] = recomendaciones
            resultado['informacionAdicional'] = informacionAdicional
            resultado['idDiagnostico'] = diagnosticos_seleccionados

            # Convertir el diccionario a JSON
            resultado_json = json.dumps(resultado)

            #LLamar la consulta put, con la url especifica
            response = requests.put(url+f'consultas/id/{idTemporal}', resultado_json)
            rsp =  response.json()

            #Ya que se necesita llenar de nuevo el formulario se busca el consulta relacionado con el id
            res = requests.get(url+f'consultas/busqueda/id/{idTemporal}')
            data = res.json()#se guarda en otra variable
            consultas = data['consultas'][0]
            id_consulta = consultas['id']
            idCita = consultas['idCita']
            idTipo = consultas['idTipo']
            recomendaciones = consultas['recomendaciones']
            informacionAdicional = consultas['informacionAdicional']
            idDiagnostico = consultas['idDiagnostico']
            # crear una lista de IDs de síntomas
            ids_diagnosticos = [{'id': idDiagnostico[str(key)]['id'], 'descripcion': idDiagnostico[str(key)]['descripcion']} for key in idDiagnostico]

            # crear un diccionario con los datos deseados
            registro_temp = {'id':id_consulta, 'idCita': idCita,'idTipo': idTipo,'recomendaciones': recomendaciones,'informacionAdicional': informacionAdicional, 'lista': ids_diagnosticos}
            #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
            if rsp['message'] == "La actualización fue exitosa.":
                mensaje = rsp['message']+'- Actualizado Correctamente'
                logger = definir_log_info('actualizar_consulta','logs_consulta')
                logger.debug(f"Se actualizo la consulta: ID {id_consulta}")
                return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = rsp['message']                         
                logger = definir_log_info('actualizar_consulta','logs_consulta')
                logger.info(f"No se pudo actualizar: {mensaje}")
                return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            logger = definir_log_info('actualizar_consulta','logs_consulta')
            logger.debug("Obteniendo información de la consulta")
            response = requests.get(url+f'consultas/busqueda/id/{idTemporal}')
            if response.status_code == 200:
                data = response.json()
                consultas = data['consultas'][0]
                id_consulta = consultas['id']
                idCita = consultas['idCita']
                idTipo = consultas['idTipo']
                recomendaciones = consultas['recomendaciones']
                informacionAdicional = consultas['informacionAdicional']
                idDiagnostico = consultas['idDiagnostico']
                # crear una lista de IDs de síntomas
                ids_diagnosticos = [{'id': idDiagnostico[str(key)]['id'], 'descripcion': idDiagnostico[str(key)]['descripcion']} for key in idDiagnostico]

                # crear un diccionario con los datos deseados
                registro_temp = {'id':id_consulta, 'idCita': idCita,'idTipo': idTipo,'recomendaciones': recomendaciones,'informacionAdicional': informacionAdicional, 'lista': ids_diagnosticos}
                return render(request, 'consulta/actualizar_consulta.html', {'registro_temp': registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                mensaje = data['message']
                logger = definir_log_info('error_actualizar_consulta','logs_consulta')
                logger.warning(f"Respuesta invalida del servidor: {mensaje}")
                return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Error'
        logger = definir_log_info('excepcion_consulta','logs_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        


def buscar_consulta(request):
    try:
        valor = request.GET.get('buscador', None)
        url2 = url + 'consultas/busqueda/'
        
        
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['consultas']:
                    data = response.json()
                    mensaje = data['message']
                    consultas = {}
                    consultas = data['consultas']
                    logger = definir_log_info('buscar_consulta','logs_consulta')
                    logger.debug("Se obtuvo la consulta especifica(filtrado por ID)")
                    context = {'consultas': consultas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'consulta/buscar_consulta.html', context)
                else:        
                    response = requests.get(url2+'documento/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        consultas = {}
                        consultas = data['consultas']
                        logger = definir_log_info('buscar_consulta','logs_consulta')
                        logger.debug("Se obtuvo la consulta especifica(filtrado por Documento)")
                        context = {'consultas': consultas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                        return render(request, 'consulta/buscar_consulta.html', context)
                    else:
                        consultas = []
                        mensaje = 'No se encontraron muestras'
                        return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                response = requests.get(url2+'documento/'+valor)
                data = response.json()
                if data['consultas']:
                    data = response.json()
                    mensaje = data['message']
                    consultas = {}
                    consultas = data['consultas']
                    logger = definir_log_info('buscar_consulta','logs_consulta')
                    logger.debug("Se obtuvo la consulta especifica(filtrado por Documento)")
                    context = {'consultas': consultas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'consulta/buscar_consulta.html', context)
                else:
                    consultas = []
                    mensaje = 'No se encontraron consultas'
                    logger = definir_log_info('buscar_consulta','logs_consulta')
                    logger.info("No se encontraron registros")
                    return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            response = requests.get(url+'consultas/')
            if response.status_code == 200:
                data = response.json()
                consultas = data['consultas']
                mensaje = data['message']  
                logger = definir_log_info('buscar_consulta','logs_consulta')
                logger.info("No obtuvieron registros")
                return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                consultas = []
                mensaje = 'No se encontraron consultas'
                logger = definir_log_info('buscar_consulta','logs_consulta')
                logger.info("No se encontraron registros")
            return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    except Exception as e:
        mensaje = 'Error'
        logger = definir_log_info('excepcion_consulta','logs_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def eliminar_consulta(request, id):  
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'consultas/id/{idTemporal}')
            res = response.json()
            rsp_consultas = requests.get(url + 'consultas/') 
            context ={}
            if rsp_consultas.status_code == 200:
                data = rsp_consultas.json()
                consultas = data['consultas']
                logger = definir_log_info('eliminar_consulta','logs_consulta')
                logger.info("Se elimino la consulta")
                context = {'consultas': consultas,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            else:
                enfermedades = []
                mensaje = res['message']
                logger = definir_log_info('eliminar_consulta','logs_consulta')
                logger.info("No se pudo eliminar la consulta")
                context = {'enfermedades': enfermedades, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'consultas/buscar_consultas.html', context) 
    except Exception as e:
        rsp_consultas = requests.get(url + 'consultas/') 
        context ={}
        mensaje = {}
        if  rsp_consultas.status_code == 200:
            data = rsp_consultas.json()
            consultas = data['consultas']
            context = {'consultas': consultas,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        else:
            consultas = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'consultas': consultas, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_consultas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        logger = definir_log_info('excepcion_consulta','logs_consulta')
        logger.exception("Ocurrio una excepcion:" + str(e))
        return render(request, 'consulta/buscar_consulta.html', context)



def list_tipo():
    rsp_tipos = requests.get(url+'tipo/busqueda/subtipo/consulta')
    if rsp_tipos.status_code == 200:
        data = rsp_tipos.json()
        list_tipo = data['tipos']
        return list_tipo
    else:
        list_tipo = []
        return list_tipo

def list_cita():
    rsp_citas = requests.get(url+'citas/')
    if rsp_citas.status_code == 200:
        data = rsp_citas.json()
        list_citas = data['citas']
        return list_citas
    else:
        list_citas = []
        return list_citas
    
def list_diagnostico():
    rsp_diagnosticos = requests.get(url+'diagnostico/')
    if rsp_diagnosticos.status_code == 200:
        data = rsp_diagnosticos.json()
        list_diagnosticos = data['diagnosticos']
        return list_diagnosticos
    else:
        list_diagnosticos = []
        return list_diagnosticos
    