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
            sintomas_seleccionados.append(sintoma)

        # Crear el diccionario final
        resultado = {}
        resultado['nombre'] = nombre
        resultado['idSintomas'] = sintomas_seleccionados

        # Convertir el diccionario a JSON
        resultado_json = json.dumps(resultado)
        registro_temp = {'nombre': nombre}
        
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

def buscar_enfermedad(request):
        valor = request.GET.get('enfermedad', None)
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
                    print(context)
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
        if  rsp_enfermedades.status_code == 200:
            data = rsp_enfermedades.json()
            enfermedades = data['enfermedades']
            context = {'enfermedades': enfermedades}
        else:
            enfermedades = []
        mensaje = 'No se puede eliminar, esta siendo utilizando en otros registros'
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
    

    