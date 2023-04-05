from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_autorizacion(request):
    response = requests.get(url+'autorizar/')
    if response.status_code == 200:
        data = response.json()
        autorizar = data['autorizar']
    else:
        autorizar = []
    context = {'autorizar': autorizar}
    return render(request, 'Autorizacion/Autorizar.html', context)

def crear_autorizacion(request):
    if request.method == 'POST':
        motivos = request.POST['motivos']        
        confirmacion = int(request.POST['payment_method'])

        registro_temp={'motivos': motivos, 'confirmacion': confirmacion}
        response = requests.post(url+'autorizar/', json={'motivos': motivos,  'confirmacion': confirmacion})
        data={}
        data = response.json()
        if response.status_code == 200:
            mensaje = data['message']
            return render(request, 'Autorizacion/Autorizar.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'Autorizacion/Autorizar.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'Autorizacion/Autorizar.html')
    
def abrir_actualizar_autorizacion(request):
    if request.method == 'POST':
         resp = requests.get(url+'autorizar/busqueda/id/'+str(request.POST['id_autorizar']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            autorizar = data['autorizar']
            mensaje = data['message']
         else:
            autorizar = []
         context = {'autorizar': autorizar, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Autorizacion/Autorizaractualizar.html', context)
    
def actualizar_autorizacion(request, id):
    if request.method == 'POST':
        idTemporal = id
        motivos = request.POST['motivos']
        
        confirmacion = int(request.POST['payment_method'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'autorizar/id/{idTemporal}', json={'motivos': motivos,  'confirmacion': confirmacion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'autorizar/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        autorizar = data['autorizar']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'autorizar/busqueda/id/{idTemporal}')
        data = response.json()
        if response.status_code == 200:
            autorizar = data['autorizar']
            mensaje = data['message']
            return render(request, 'Autorizacion/Autorizaractualizar.html', {'autorizar': autorizar})
        else:
            mensaje = data['message']
            return render(request, 'Autorizacion/Autorizaractualizar.html', {'mensaje': mensaje,'autorizar':autorizar})

def eliminar_autorizacion(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'autorizar/id/{idTemporal}')
        res = response.json()
        rsp_autorizar = requests.get(url + 'autorizar/') 
        if rsp_autorizar.status_code == 200:
            data = rsp_autorizar.json()
            autorizar = data['autorizar']
        else:
            autorizar = []
        mensaje = res['message']
        context = {'autorizar': autorizar, 'mensaje': mensaje}
        return render(request, 'Autorizacion/buscarAutorizar.html', context)     
    
def buscar_autorizacion(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'autorizar/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    autorizar = {}
                    autorizar = data['autorizar']
                    context = {'autorizar': autorizar, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'Autorizacion/buscarAutorizar.html', context)
                else:
                    autorizar = []
                    mensaje = 'No se encontraron Autorizaciones de pacientes'
                    return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje})    
            else:
                response = requests.get(url2+'motivos/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    autorizar = {}
                    autorizar = data['autorizar']
                    context = {'autorizar': autorizar, 'mensaje':mensaje}
                    return render(request, 'Autorizacion/buscarAutorizar.html', context)
                else:
                    autorizar = []
                    mensaje = 'No se encontraron Autorizaciones de pacientes'
                    return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje})    
        else:
            response = requests.get(url+'autorizar/')
            if response.status_code == 200:
                data = response.json()
                autorizar = data['autorizar']
                mensaje = data['message']   
                return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje})
            else:
                autorizar = []
                mensaje = 'No se encontraron Autorizaciones de pacientes'
            return render(request, 'Autorizacion/buscarAutorizar.html', {'autorizar': autorizar, 'mensaje': mensaje})
    