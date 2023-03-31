from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_resultados(request):
    response = requests.get(url+'resultados/')
    if response.status_code == 200:
        data = response.json()
        resultados = data['resultados']
    else:
        resultados = []
    context = {'resultados': resultados}
    return render(request, 'Resultados/BuscarResultados', context)

def crear_resultados(request):
    rsp_tipos = requests.get(url+'tipos/')
    if rsp_tipos.status_code == 200:
            data = rsp_tipos.json()
            tipos_list = data['tipos']
    else:
            tipos_list = []
    rsp_resultados = requests.get(url+'resultados/')
    if rsp_resultados.status_code == 200:
            data = rsp_resultados.json()
            resultados_list = data['resultados']
    else:
            resultados_list = []
    
    if request.method == 'POST':
        idtipo = int(request.POST['idtipo'])
        observacion = request.POST['observacion']
        fecha = request.POST['fecha']
        registro_temp = {'idtipo': idtipo, 'observacion': observacion, 'fecha': fecha}
        response = requests.post(url+'resultados/', json={'idtipo': idtipo, 'observacion': observacion, 'fecha': fecha})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Resultados/Resultados.html', {'mensaje': mensaje, 'registro_temp':registro_temp, 'resultados_list':resultados_list,'tipos_list':tipos_list})
        else:
            mensaje = data['message']
            return render(request, 'Resultados/Resultados.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'resultados_list':resultados_list,'tipos_list':tipos_list})
    else:
        return render(request, 'Resultados/Resultados.html', {'resultados_list':resultados_list})
    
def abrir_actualizar_resultados(request):
    if request.method == 'POST':
         resp = requests.get(url+'resultados/busqueda/id/'+str(request.POST['id_resultados']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            resultados = data['resultados']
            mensaje = data['message']
         else:
            resultados = []
         context = {'resultados': resultados, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Resultados/ActualizarResultados.html', context)
    
def actualizar_resultados(request, id):
    if request.method == 'POST':
        idTemporal = id
        idTratamiento = int(request.POST['idTratamiento'])
        observacion = request.POST['observacion']
        fecha = request.POST['fecha']
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'resultados/id/{idTemporal}', json={'idTratamiento': idTratamiento, 'observacion': observacion, 'fecha': fecha})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'resultados/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        resultados = data['resultados']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Resultados/ActualizarResultados.html', {'mensaje': mensaje,'resultados':resultados })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Resultados/ActualizarResultados.html', {'mensaje': mensaje,'resultados':resultados})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'resultados/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            resultados = data['resultados']
            mensaje = data['message']
            return render(request, 'Resultados/ActualizarResultados.html', {'resultados': resultados})
        else:
            mensaje = data['message']
            return render(request, 'Resultados/ActualizarResultados.html', {'mensaje': mensaje,'resultados':resultados})

def eliminar_resultados(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'resultados/id/{idTemporal}')
        res = response.json()
        rsp_resultados = requests.get(url + 'resultados/') 
        if rsp_resultados.status_code == 200:
            data = rsp_resultados.json()
            resultados = data['resultados']
        else:
            resultados = []
        mensaje = res['message']
        context = {'resultados': resultados, 'mensaje': mensaje}
        return render(request, 'Resultados/BuscarResultados', context)     
    
def buscar_resultados(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'resultados/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    resultados = {}
                    resultados = data['resultados']
                    context = {'resultados': resultados, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'Resultados/BuscarResultados', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    resultados = {}
                    resultados = data['resultados']
                    context = {'resultados': resultados, 'mensaje':mensaje}
                    return render(request, 'Resultados/BuscarResultados', context)
        else:
            response = requests.get(url+'resultados/')
            if response.status_code == 200:
                data = response.json()
                resultados = data['resultados']
                mensaje = data['message']   
                return render(request, 'Resultados/BuscarResultados', {'resultados': resultados, 'mensaje': mensaje})
            else:
                resultados = []
                mensaje = 'No se encontraron muestras'
            return render(request, 'Resultados/BuscarResultados', {'resultados': resultados, 'mensaje': mensaje})

def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/tratamiento')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list