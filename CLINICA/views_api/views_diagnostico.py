import ast
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
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
            return render(request, 'diagnostico/diagnostico.html', {'mensaje': mensaje, 'registro_temp':registro_temp, 'enfermedades':enfermedades})
        else:
            data = response.json()
            mensaje = data['message']
        return render(request, 'diagnostico/diagnostico.html', {'mensaje': "mensaje", 'registro_temp':registro_temp, 'enfermedades':enfermedades})
    else:
        return render(request, 'diagnostico/diagnostico.html', {'enfermedades':enfermedades})

def abrir_actualizar_diagnosticos(request):
    #Se cargan las listas para los SELECT
    enfermedades = list_enfermedades()
    if request.method == 'POST':
         resp = requests.get(url+'diagnostico/busqueda/id/'+str(request.POST['id_diagnostico']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            mensaje = data['message']
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
         context = {'registro_temp': registro_temp,'enfermedades': enfermedades, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'diagnostico/Actualizar_diagnostico.html', context)   

def actualizar_diagnosticos(request, id):
    #Se cargan las listas para los SELECT
    enfermedades = list_enfermedades()
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
            return render(request, 'diagnostico/Actualizar_diagnostico.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'enfermedades':enfermedades})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'diagnostico/Actualizar_diagnostico.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'enfermedades':enfermedades})
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

            # crear un diccionario con los datos deseados
            registro_temp = {'id':id_diagnosticos, 'descripcion': descripcion, 'lista': ids_enfermedades}
            return render(request, 'diagnostico/Actualizar_diagnostico.html', {'registro_temp': registro_temp, 'enfermedades':enfermedades})
        else:
            mensaje = data['message']
            return render(request, 'diagnostico/Actualizar_diagnostico.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'enfermedades':enfermedades})



def buscar_diagnosticos(request):
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
                    context = {'diagnostico': diagnostico, 'mensaje':mensaje}
                    return render(request, 'diagnostico/Buscar_diagnostico.html', context)       
            else:
                response = requests.get(url2+'descripcion/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    diagnostico = {}
                    diagnostico = data['diagnosticos']
                    context = {'diagnostico': diagnostico, 'mensaje':mensaje}
                    return render(request, 'diagnostico/Buscar_diagnostico.html', context)
        else:
            response = requests.get(url+'diagnostico/')
            if response.status_code == 200:
                data = response.json()
                diagnostico = data['diagnosticos']
                
                mensaje = data['message']   
                return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje})
            else:
                diagnostico = []
                mensaje = 'No se encontraron registros'
            return render(request, 'diagnostico/Buscar_diagnostico.html', {'diagnostico': diagnostico, 'mensaje': mensaje})

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
                context = {'diagnostico': diagnostico}
            else:
                diagnostico = []
                mensaje = res['message']
                context = {'diagnostico': diagnostico, 'mensaje': mensaje}
            return render(request, 'diagnostico/Buscar_diagnostico.html', context) 
    except:
        rsp_diagnostico = requests.get(url + 'diagnostico/') 
        context ={}
        if  rsp_diagnostico.status_code == 200:
            data = rsp_diagnostico.json()
            diagnostico = data['diagnosticos']
            context = {'diagnostico': diagnostico}
        else:
            diagnostico = []
        mensaje = 'No se puede eliminar, esta siendo utilizando en otros registros'
        context = {'diagnostico': diagnostico, 'error': mensaje}
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
    

    