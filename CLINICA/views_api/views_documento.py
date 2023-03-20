from django.http import HttpResponse
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_documentos(request):
    response = requests.get(url+'documentos/')
    if response.status_code == 200:
        data = response.json()
        documentos = data['documentos']
    else:
        documentos = []
    context = {'documentos': documentos}
    return render(request, 'documentos/buscarDocumento.html', context)

def crear_documento(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        longitud = int(request.POST['longitud'])

        registro_temp={'nombre': nombre, 'longitud': longitud}
        response = requests.post(url+'documentos/', json={'nombre': nombre, 'longitud': longitud})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'documentos/documento.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'documentos/documento.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'documentos/documento.html')
    
def abrir_actualizar_documentos(request):
    if request.method == 'POST':
         resp = requests.get(url+'documentos/busqueda/id/'+str(request.POST['id_documento']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            documentos = data['documentos']
            mensaje = data['message']
         else:
            documentos = []
         context = {'documentos': documentos, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'documentos/documentoactualizar.html', context)
    
def actualizar_documento(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        longitud = int(request.POST['longitud'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'documentos/id/{idTemporal}', json={'nombre': nombre, 'longitud': longitud})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'documentos/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        documentos = data['documentos']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'documentos/documentoactualizar.html', {'mensaje': mensaje,'documentos':documentos })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'documentos/documentoactualizar.html', {'mensaje': mensaje,'documentos':documentos})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'documentos/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            documentos = data['documentos']
            mensaje = data['message']
            return render(request, 'documentos/documentoactualizar.html', {'documentos': documentos})
        else:
            mensaje = data['message']
            return render(request, 'documentos/documentoactualizar.html', {'mensaje': mensaje,'documentos':documentos})

def eliminar_documento(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'documentos/id/{idTemporal}')
        res = response.json()
        rsp_documentos = requests.get(url + 'documentos/') 
        if rsp_documentos.status_code == 200:
            data = rsp_documentos.json()
            documentos = data['documentos']
        else:
            documentos = []
        mensaje = res['message']
        context = {'documentos': documentos, 'mensaje': mensaje}
        return render(request, 'documentos/buscarDocumento.html', context)     
    
def buscar_documentos(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'documentos/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    documentos = {}
                    documentos = data['documentos']
                    context = {'documentos': documentos, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'documentos/buscarDocumento.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    documentos = {}
                    documentos = data['documentos']
                    context = {'documentos': documentos, 'mensaje':mensaje}
                    return render(request, 'documentos/buscarDocumento.html', context)
        else:
            response = requests.get(url+'documentos/')
            if response.status_code == 200:
                data = response.json()
                documentos = data['documentos']
                mensaje = data['message']   
                return render(request, 'documentos/buscarDocumento.html', {'documentos': documentos, 'mensaje': mensaje})
            else:
                usuarios = []
                mensaje = 'No se encontraron documentos'
            return render(request, 'documentos/buscarDocumento.html', {'documentos': documentos, 'mensaje': mensaje})
    