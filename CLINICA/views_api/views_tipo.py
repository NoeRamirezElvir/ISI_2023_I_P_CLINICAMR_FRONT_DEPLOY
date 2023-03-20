from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_tipo(request):
    response = requests.get(url+'tipo/')
    if response.status_code == 200:
        data = response.json()
        tipo = data['tipo']
    else:
        tipo = []
    context = {'tipo': tipo}
    return render(request, 'Tipos/buscartipo.html', context)

def crear_tipo(request):
    rsp_Subtipo = requests.get(url+'subtipo/')
    if rsp_Subtipo.status_code == 200:
            data = rsp_Subtipo.json()
            Subtipo = data['subtipo']
    else:
            Subtipo= []

    if request.method == 'POST':
        idsubtipo = int(request.POST['idsubtipo'])
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        registro_temp = {'nombre': nombre, 'descripcion': descripcion,'idsubtipo':idsubtipo}
        response = requests.post(url+'tipo/', json={'nombre': nombre, 'descripcion': descripcion,'idsubtipo':idsubtipo})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']

            return render(request, 'Tipos/tipo.html', {'mensaje': mensaje,'subtipo': Subtipo, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'Tipos/tipo.html', {'mensaje': mensaje,'subtipo': Subtipo, 'registro_temp':registro_temp})
    else:
        return render(request, 'Tipos/tipo.html',{'subtipo': Subtipo})
    
def abrir_actualizar_tipo(request):
    rsp_subtipo = requests.get(url+'subtipo/')
    if rsp_subtipo.status_code == 200:
            data = rsp_subtipo.json()
            subtipo = data['subtipo']
    else:
            subtipo= []

    if request.method == 'POST':
         resp = requests.get(url+'tipo/busqueda/id/'+str(request.POST['id_tipos']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            tipo = data['tipo']
            mensaje = data['message']
         else:
            tipo = []
         context = {'tipo': tipo,'subtipo': subtipo, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Tipos/tipoactualizar.html', context)
    
def actualizar_tipo(request, id):
    rsp_subtipo = requests.get(url+'subtipo/')
    if rsp_subtipo.status_code == 200:
            data = rsp_subtipo.json()
            subtipo = data['subtipo']
    else:
            subtipo= []
    if request.method == 'POST':
        idTemporal = id
        idsubtipo = int (request.POST['idsubtipo'])
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'tipo/id/{idTemporal}', json={'idsubtipo': idsubtipo,'nombre': nombre, 'descripcion': descripcion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el tipo relacionado con el id
        res = requests.get(url+f'tipo/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        tipo = data['tipo']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Tipos/tipoactualizar.html', {'mensaje': mensaje,'tipo':tipo,'subtipo':subtipo })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Tipos/tipoactualizar.html', {'mensaje': mensaje,'tipo':tipo,'subtipo':subtipo})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'tipo/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            tipo = data['tipo']
            mensaje = data['message']
            return render(request, 'Tipos/tipoactualizar.html', {'tipo': tipo,'subtipo':subtipo})
        else:
            mensaje = data['message']
            return render(request, 'Tipos/tipoactualizar.html', {'mensaje': mensaje,'tipo':tipo,'subtipo':subtipo})

def eliminar_tipo(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'tipo/id/{idTemporal}')
        res = response.json()
        rsp_tipo = requests.get(url + 'tipo/') 
        if rsp_tipo.status_code == 200:
            data = rsp_tipo.json()
            tipo = data['tipo']
        else:
            tipo = []
        mensaje = res['message']
        context = {'tipo': tipo, 'mensaje': mensaje}
        return render(request, 'Tipos/buscartipo.html', context)     
    
def buscar_tipo(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'tipo/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tipo = {}
                    tipo = data['tipo']
                    context = {'tipo': tipo, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'Tipos/buscartipo.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tipo = {}
                    tipo = data['tipo']
                    context = {'tipo': tipo, 'mensaje':mensaje}
                    return render(request, 'Tipos/buscartipo.html', context)
        else:
            response = requests.get(url+'tipo/')
            if response.status_code == 200:
                data = response.json()
                tipo = data['tipo']
                mensaje = data['message']   
                return render(request, 'Tipos/buscartipo.html', {'tipo': tipo, 'mensaje': mensaje})
            else:
                tipo = []
                mensaje = 'No se encontraron tipo'
            return render(request, 'Tipos/buscartipo.html', {'tipo': tipo, 'mensaje': mensaje})
    