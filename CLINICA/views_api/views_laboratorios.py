from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_laboratorios(request):
    response = requests.get(url+'laboratorios/')
    if response.status_code == 200:
        data = response.json()
        laboratorios = data['laboratorios']
    else:
        laboratorios = []
    context = {'laboratorios': laboratorios}
    return render(request, 'Laboratorios/BuscarLaboratorios.html', context)

def crear_laboratorios(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        disponibilidad = int(request.POST['payment_method'])

        registro_temp={'nombre': nombre, 'direccion': direccion,'telefono': telefono, 'disponibilidad': disponibilidad}
        response = requests.post(url+'laboratorios/', json={'nombre': nombre, 'direccion': direccion,'telefono': telefono, 'disponibilidad': disponibilidad})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Laboratorios/Laboratorios.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'Laboratorios/Laboratorios.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'Laboratorios/Laboratorios.html')
    
def abrir_actualizar_laboratorios(request):
    if request.method == 'POST':
         resp = requests.get(url+'laboratorios/busqueda/id/'+str(request.POST['id_laboratorios']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            laboratorios = data['laboratorios']
            mensaje = data['message']
         else:
            laboratorios = []
         context = {'laboratorios': laboratorios, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Laboratorios/ActualizarLaboratorios.html', context)
    
def actualizar_laboratorios(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        disponibilidad = int(request.POST['payment_method'])
        
        response = requests.put(url+f'laboratorios/id/{idTemporal}', json={'nombre': nombre, 'direccion': direccion,'telefono': telefono, 'disponibilidad': disponibilidad})
        
        rsp =  response.json()
       
        res = requests.get(url+f'laboratorios/busqueda/id/{idTemporal}')
        data = res.json()
        laboratorios = data['laboratorios']
        
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'mensaje': mensaje,'laboratorios':laboratorios })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'mensaje': mensaje,'laboratorios':laboratorios})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'laboratorios/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            laboratorios = data['laboratorios']
            mensaje = data['message']
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'laboratorios': laboratorios})
        else:
            mensaje = data['message']
            return render(request, 'Laboratorios/ActualizarLaboratorios.html', {'mensaje': mensaje,'laboratorios':laboratorios})

def eliminar_laboratorios(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'laboratorios/id/{idTemporal}')
        res = response.json()
        rsp_laboratorios = requests.get(url + 'laboratorios/') 
        if rsp_laboratorios.status_code == 200:
            data = rsp_laboratorios.json()
            laboratorios = data['laboratorios']
        else:
            laboratorios = []
        mensaje = res['message']
        context = {'laboratorios': laboratorios, 'mensaje': mensaje}
        return render(request, 'Laboratorios/BuscarLaboratorios.html', context)     
    
def buscar_laboratorios(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'laboratorios/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    laboratorios = {}
                    laboratorios = data['laboratorios']
                    context = {'laboratorios': laboratorios, 'mensaje':mensaje}
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', context)  
                else:
                    laboratorios = []
                    mensaje = 'No se encontraron laboratorios'
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', {'laboratorios': laboratorios, 'mensaje': mensaje})
             
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    laboratorios = {}
                    laboratorios = data['laboratorios']
                    context = {'laboratorios': laboratorios, 'mensaje':mensaje}
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', context)
                else:
                    laboratorios = []
                    mensaje = 'No se encontraron laboratorios'
                    return render(request, 'Laboratorios/BuscarLaboratorios.html', {'laboratorios': laboratorios, 'mensaje': mensaje})
        else:
            response = requests.get(url+'laboratorios/')
            if response.status_code == 200:
                data = response.json()
                laboratorios = data['laboratorios']
                mensaje = data['message']   
                return render(request, 'Laboratorios/BuscarLaboratorios.html', {'laboratorios': laboratorios, 'mensaje': mensaje})
            else:
                laboratorios = []
                mensaje = 'No se encontraron laboratorios'
            return render(request, 'Laboratorios/BuscarLaboratorios.html', {'laboratorios': laboratorios, 'mensaje': mensaje})
    