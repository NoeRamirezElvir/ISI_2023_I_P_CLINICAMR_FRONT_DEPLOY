import ast
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


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
            return render(request, 'consulta/consulta.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})
        else:
            data = response.json()
            mensaje = data['message']
        return render(request, 'consulta/consulta.html', {'mensaje': "mensaje", 'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})
    else:
        return render(request, 'consulta/consulta.html', {'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})

def abrir_actualizar_consulta(request):
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
         context = {'registro_temp': registro_temp,'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'consulta/actualizar_consulta.html', context)   

def actualizar_consulta(request, id):
    #Se cargan las listas para los SELECT
    diagnostico_list = list_diagnostico()
    cita_list = list_cita()
    tipo_list = list_tipo()
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

        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
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
            return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})
    else:
        #Y aqui no se que hice la verdad
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
            return render(request, 'consulta/actualizar_consulta.html', {'registro_temp': registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})
        else:
            mensaje = data['message']
            return render(request, 'consulta/actualizar_consulta.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'diagnostico_list':diagnostico_list,'cita_list':cita_list,'tipo_list':tipo_list})


def buscar_consulta(request):
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
                    context = {'consultas': consultas, 'mensaje':mensaje}
                    return render(request, 'consulta/buscar_consulta.html', context)
                else:        
                    response = requests.get(url2+'documento/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        consultas = {}
                        consultas = data['consultas']
                        context = {'consultas': consultas, 'mensaje':mensaje}
                        return render(request, 'consulta/buscar_consulta.html', context)
                    else:
                        consultas = []
                        mensaje = 'No se encontraron muestras'
                        return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje})
            else:
                response = requests.get(url2+'documento/'+valor)
                data = response.json()
                if data['consultas']:
                    data = response.json()
                    mensaje = data['message']
                    consultas = {}
                    consultas = data['consultas']
                    context = {'consultas': consultas, 'mensaje':mensaje}
                    return render(request, 'consulta/buscar_consulta.html', context)
                else:
                    consultas = []
                    mensaje = 'No se encontraron muestras'
                    return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje})
        else:
            response = requests.get(url+'consultas/')
            if response.status_code == 200:
                data = response.json()
                consultas = data['consultas']
                mensaje = data['message']   
                return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje})
            else:
                consultas = []
                mensaje = 'No se encontraron consultas'
            return render(request, 'consulta/buscar_consulta.html', {'consultas': consultas, 'mensaje': mensaje})

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
                context = {'consultas': consultas}
            else:
                enfermedades = []
                mensaje = res['message']
                context = {'enfermedades': enfermedades, 'mensaje': mensaje}
            return render(request, 'consultas/buscar_consultas.html', context) 
    except:
        rsp_consultas = requests.get(url + 'consultas/') 
        context ={}
        mensaje = {}
        if  rsp_consultas.status_code == 200:
            data = rsp_consultas.json()
            consultas = data['consultas']
            context = {'consultas': consultas}
        else:
            consultas = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'consultas': consultas, 'error': mensaje}
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
    