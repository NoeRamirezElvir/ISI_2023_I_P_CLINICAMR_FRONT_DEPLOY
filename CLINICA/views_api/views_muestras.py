from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_muestras(request):
    response = requests.get(url+'muestras/')
    if response.status_code == 200:
        data = response.json()
        muestras= data['muestras']
    else:
        muestras = []
    context = {'muestras': muestras}
    return render(request, 'Muestras/Muestra.html', context)

def crear_muestras(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        
        
        response = requests.post(url+'muestras/', json={'nombre': nombre})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Muestras/Muestra.html', {'mensaje': mensaje})
        else:
            mensaje = data['message']
            return render(request, 'Muestras/Muestra.html', {'mensaje': mensaje})
    else:
        return render(request, 'Muestras/Muestra.html')
    
def abrir_actualizar_muestras(request):
    if request.method == 'POST':
         resp = requests.get(url+'muestras/busqueda/id/'+str(request.POST['id_muestras']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            muestras = data['muestras']
            mensaje = data['message']
         else:
            muestras = []
         context = {'muestras': muestras, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'MuestraActualizar.html', context)
    
def actualizar_muestras(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'muestras/id/{idTemporal}', json={'nombre': nombre})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'muestras/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        muestras = data['muestras']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'MuestraActualizar.html', {'mensaje': mensaje,'muestras':muestras })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'MuestraActualizar.html', {'mensaje': mensaje,'muestras':muestras})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'muestras/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            muestras = data['muestras']
            mensaje = data['message']
            return render(request, 'Muestras/MuestraActualizar.html', {'muestras': muestras})
        else:
            mensaje = data['message']
            return render(request, 'Muestras/MuestraActualizar.html', {'mensaje': mensaje,'muestras':muestras})

def eliminar_muestras(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'muestras/id/{idTemporal}')
        res = response.json()
        rsp_muestras = requests.get(url + 'muestras/') 
        if rsp_muestras.status_code == 200:
            data = rsp_muestras.json()
            muestras = data['muestras']
        else:
            muestras = []
        mensaje = res['message']
        context = {'muestras': muestras, 'mensaje': mensaje}
        return render(request, 'Muestras/BuscarMuestra.html', context)     
    
def buscar_muestras(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'muestras/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    muestras = {}
                    muestras = data['muestras']
                    context = {'muestras': muestras, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'Muestras/BuscarMuestra.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    muestras = {}
                    muestras = data['muestras']
                    context = {'muestras': muestras, 'mensaje':mensaje}
                    return render(request, 'Muestras/BuscarMuestra.html', context)
        else:
            response = requests.get(url+'muestras/')
            if response.status_code == 200:
                data = response.json()
                muestras = data['muestras']
                mensaje = data['message']   
                return render(request, 'Muestras/BuscarMuestra.html', {'muestras': muestras, 'mensaje': mensaje})
            else:
                muestras = []
                mensaje = 'No se encontraron muestras'
            return render(request, 'Muestras/BuscarMuestra.html', {'muestras': muestras, 'mensaje': mensaje})
    