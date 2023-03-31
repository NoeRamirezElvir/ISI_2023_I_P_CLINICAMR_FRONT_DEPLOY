import ast
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_enfermedad(request):
    response = requests.get(url+'enfermedades/')
    if response.status_code == 200:
        data = response.json()
        enfermedades = data['enfermedades']
    else:
        enfermedades = []
    context = {'enfermedades': enfermedades}
    return render(request, 'enfermedad/buscar_enfermedad.html', context)


def crear_enfermedad(request):
    #Se cargan las listas para los SELECT
    sintomas = list_sintomas()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        valores_seleccionados_json = request.POST['valoresSeleccionados']
        valores_seleccionados = json.loads(valores_seleccionados_json)

        # Crear la lista de diccionarios para los sintomas seleccionados
        sintomas_seleccionados = []
        for valor in valores_seleccionados:
            sintoma = {}
            sintoma['id'] = int(valor.split("-")[0])
            sintoma['nombre'] = str(valor.split("-")[1])
            sintomas_seleccionados.append(sintoma)

        # Crear el diccionario final
        resultado = {}
        resultado['nombre'] = nombre
        resultado['idSintomas'] = sintomas_seleccionados


        # Convertir el diccionario a JSON
        resultado_json = json.dumps(resultado)
        registro_temp = {'nombre': nombre, 'lista': sintomas_seleccionados}
        
        response = requests.post(url+'enfermedades/', resultado_json)
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'enfermedad/enfermedad.html', {'mensaje': mensaje, 'registro_temp':registro_temp, 'sintomas':sintomas})
        else:
            data = response.json()
            mensaje = data['message']
        return render(request, 'enfermedad/enfermedad.html', {'mensaje': "mensaje", 'registro_temp':registro_temp, 'sintomas':sintomas})
    else:
        return render(request, 'enfermedad/enfermedad.html', {'sintomas':sintomas})

def abrir_actualizar_enfermedad(request):
    #Se cargan las listas para los SELECT
    sintomas = list_sintomas()
    if request.method == 'POST':
         resp = requests.get(url+'enfermedades/busqueda/id/'+str(request.POST['id_enfermedad']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            mensaje = data['message']
            enfermedades = data['enfermedades'][0]
            id = enfermedades['id']
            nombre = enfermedades['nombre']
            idSintomas = enfermedades['idSintomas']
            # crear una lista de IDs de síntomas
            ids_sintomas = [{'id': idSintomas[str(key)]['id'], 'nombre': idSintomas[str(key)]['nombre']} for key in idSintomas]

            # crear un diccionario con los datos deseados
            registro_temp = {'id':id, 'nombre': nombre, 'lista': ids_sintomas}
         else:
            registro_temp = {}
         context = {'registro_temp': registro_temp,'sintomas': sintomas, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'enfermedad/actualizar_enfermedad.html', context)   

def actualizar_enfermedad(request, id):
    #Se cargan las listas para los SELECT
    sintomas = list_sintomas()
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        valores_seleccionados_json = request.POST['valoresSeleccionados']
        valores_seleccionados = json.loads(valores_seleccionados_json)
        # Crear la lista de diccionarios para los sintomas seleccionados
        sintomas_seleccionados = []
        for valor in valores_seleccionados:
            sintoma = {}
            sintoma['id'] = int(valor.split("-")[0])
            sintoma['nombre'] = str(valor.split("-")[1])
            sintomas_seleccionados.append(sintoma)

        # Crear el diccionario final
        resultado = {}
        resultado['nombre'] = nombre
        resultado['idSintomas'] = sintomas_seleccionados

        # Convertir el diccionario a JSON
        resultado_json = json.dumps(resultado)

        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'enfermedades/id/{idTemporal}', resultado_json)
        rsp =  response.json()

        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'enfermedades/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        enfermedades = data['enfermedades'][0]
        id_enfermedad = enfermedades['id']
        nombre = enfermedades['nombre']
        idSintomas = enfermedades['idSintomas']
        # crear una lista de IDs de síntomas
        ids_sintomas = [{'id': idSintomas[str(key)]['id'], 'nombre': idSintomas[str(key)]['nombre']} for key in idSintomas]

        # crear un diccionario con los datos deseados
        registro_temp = {'id':id_enfermedad, 'nombre': nombre, 'lista': sintomas_seleccionados}
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'enfermedad/actualizar_enfermedad.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'sintomas':sintomas})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'enfermedad/actualizar_enfermedad.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'sintomas':sintomas})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'enfermedades/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            enfermedades = data['enfermedades'][0]
            id_enfermedad = enfermedades['id']
            nombre = enfermedades['nombre']
            idSintomas = enfermedades['idSintomas']
            # crear una lista de IDs de síntomas
            ids_sintomas = [{'id': idSintomas[str(key)]['id'], 'nombre': idSintomas[str(key)]['nombre']} for key in idSintomas]

            # crear un diccionario con los datos deseados
            registro_temp = {'id':id_enfermedad, 'nombre': nombre, 'lista': ids_sintomas}
            return render(request, 'enfermedad/actualizar_enfermedad.html', {'registro_temp': registro_temp, 'sintomas':sintomas})
        else:
            mensaje = data['message']
            return render(request, 'enfermedad/actualizar_enfermedad.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'sintomas':sintomas})


def buscar_enfermedad(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'enfermedades/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    enfermedades = {}
                    enfermedades = data['enfermedades']
                    context = {'enfermedades': enfermedades, 'mensaje':mensaje}
                    return render(request, 'enfermedad/buscar_enfermedad.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    enfermedades = {}
                    enfermedades = data['enfermedades']
                    context = {'enfermedades': enfermedades, 'mensaje':mensaje}
                    return render(request, 'enfermedad/buscar_enfermedad.html', context)
        else:
            response = requests.get(url+'enfermedades/')
            if response.status_code == 200:
                data = response.json()
                enfermedades = data['enfermedades']
                mensaje = data['message']   
                return render(request, 'enfermedad/buscar_enfermedad.html', {'enfermedades': enfermedades, 'mensaje': mensaje})
            else:
                enfermedades = []
                mensaje = 'No se encontraron registros'
            return render(request, 'enfermedad/buscar_enfermedad.html', {'enfermedades': enfermedades, 'mensaje': mensaje})

def eliminar_enfermedad(request, id):  
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'enfermedades/id/{idTemporal}')
            res = response.json()
            rsp_enfermedades = requests.get(url + 'enfermedades/') 
            context ={}
            if rsp_enfermedades.status_code == 200:
                data = rsp_enfermedades.json()
                enfermedades = data['enfermedades']
                context = {'enfermedades': enfermedades}
            else:
                enfermedades = []
                mensaje = res['message']
                context = {'enfermedades': enfermedades, 'mensaje': mensaje}
            return render(request, 'enfermedades/buscar_enfermedad.html', context) 
    except:
        rsp_enfermedades = requests.get(url + 'enfermedades/') 
        context ={}
        mensaje = {}
        if  rsp_enfermedades.status_code == 200:
            data = rsp_enfermedades.json()
            enfermedades = data['enfermedades']
            context = {'enfermedades': enfermedades}
        else:
            enfermedades = []
            mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'enfermedades': enfermedades, 'error': mensaje}
        return render(request, 'enfermedad/buscar_enfermedad.html', context)






def list_sintomas():
    rsp_sintomas = requests.get(url+'sintomas/')
    if rsp_sintomas.status_code == 200:
        data = rsp_sintomas.json()
        list_sintomas = data['sintomas']
        return list_sintomas
    else:
        list_sintomas = []
        return list_sintomas
    

    