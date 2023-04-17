from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_subtipo(request):
    response = requests.get(url+'subtipo/')
    if response.status_code == 200:
        data = response.json()
        subtipo = data['subtipo']
    else:
        subtipo = []
    context = {'subtipo': subtipo}
    return render(request, 'SubTipo/subtipo.html', context)

def crear_subtipo(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        activo = int(request.POST['payment_method'])

        registro_temp={'nombre': nombre,  'activo': activo}
        response = requests.post(url+'subtipo/', json={'nombre': nombre,  'activo': activo})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'SubTipo/subtipo.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'SubTipo/subtipo.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'SubTipo/subtipo.html')
    
def abrir_actualizar_subtipo(request):
    if request.method == 'POST':
         resp = requests.get(url+'subtipo/busqueda/id/'+str(request.POST['id_subtipo']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            subtipo = data['subtipo']
            mensaje = data['message']
         else:
            subtipo = []
         context = {'subtipo': subtipo, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'SubTipo/subtipoActualizar.html', context)
    
def actualizar_subtipo(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        
        activo = int(request.POST['payment_method'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'subtipo/id/{idTemporal}', json={'nombre': nombre,  'activo': activo})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el subtipo relacionado con el id
        res = requests.get(url+f'subtipo/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        subtipo = data['subtipo']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'SubTipo/subtipoActualizar.html', {'mensaje': mensaje,'subtipo':subtipo })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'SubTipo/subtipoActualizar.html', {'mensaje': mensaje,'subtipo':subtipo})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'subtipo/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            subtipo = data['subtipo']
            mensaje = data['message']
            return render(request, 'SubTipo/subtipoActualizar.html', {'subtipo': subtipo})
        else:
            mensaje = data['message']
            return render(request, 'SubTipo/subtipoActualizar.html', {'mensaje': mensaje,'subtipo':subtipo})

def eliminar_subtipo(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'subtipo/id/{idTemporal}')
            res = response.json()
            rsp_subtipo = requests.get(url + 'subtipo/') 
            if rsp_subtipo.status_code == 200:
                data = rsp_subtipo.json()
                subtipo = data['subtipo']
            else:
                subtipo = []
            mensaje = res['message']
            context = {'subtipo': subtipo, 'mensaje': mensaje}
            return render(request, 'SubTipo/buscarsubtipo.html', context)     
    except:
        rsp_subtipo = requests.get(url + 'subtipo/') 
        if rsp_subtipo.status_code == 200:
            data = rsp_subtipo.json()
            subtipo = data['subtipo']
        else:
            subtipo = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'subtipo': subtipo, 'error': mensaje}
        return render(request, 'SubTipo/buscarsubtipo.html', context)     
       
def buscar_subtipo(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'subtipo/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    subtipo = {}
                    subtipo = data['subtipo']
                    context = {'subtipo': subtipo, 'mensaje':mensaje}
                    return render(request, 'SubTipo/buscarsubtipo.html', context)
                else:
                    subtipo = []
                    mensaje = 'No se encontraron subtipo'
                    return render(request, 'SubTipo/buscarsubtipo.html', {'subtipo': subtipo, 'mensaje': mensaje})
           
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    subtipo = {}
                    subtipo = data['subtipo']
                    context = {'subtipo': subtipo, 'mensaje':mensaje}
                    return render(request, 'SubTipo/buscarsubtipo.html', context)
                else:
                    subtipo = []
                    mensaje = 'No se encontraron subtipo'
                    return render(request, 'SubTipo/buscarsubtipo.html', {'subtipo': subtipo, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'subtipo/')
            if response.status_code == 200:
                data = response.json()
                subtipo = data['subtipo']
                mensaje = data['message']   
                return render(request, 'SubTipo/buscarsubtipo.html', {'subtipo': subtipo, 'mensaje': mensaje})
            else:
                subtipo = []
                mensaje = 'No se encontraron subtipo'
            return render(request, 'SubTipo/buscarsubtipo.html', {'subtipo': subtipo, 'mensaje': mensaje})
    