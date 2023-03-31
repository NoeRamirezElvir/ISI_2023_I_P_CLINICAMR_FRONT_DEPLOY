from django.http import HttpResponse
import json
from django.shortcuts import render
import requests

url = 'http://localhost:8080/api/'
def listar_proveedor(request):
    response = requests.get(url+'proveedores/')
    if response.status_code == 200:
        data = response.json()
        proveedores = data['proveedores']
    else:
        proveedores = []
    context = {'proveedores': proveedores}
    return render(request, 'Proveedor/BuscarProveedor.html', context)

def crear_proveedor(request):
    tipos = list_tipos()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST ['direccion']

        registro_temp = {'nombre': nombre,'telefono': telefono,'correo': correo,'direccion': direccion}
        response = requests.post(url+'proveedores/', json={'nombre': nombre,'telefono': telefono,'correo': correo,'direccion': direccion})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Proveedor/Proveedor.html', {'mensaje': mensaje, 'registro_temp':registro_temp, 'tipos':tipos})
        else:
            mensaje = data['message']
            return render(request, 'Proveedor/Proveedor.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'tipos':tipos})
    else:
        return render(request, 'Proveedor/Proveedor.html', {'tipos':tipos})
    
def abrir_actualizar_proveedor(request):
    if request.method == 'POST':
         resp = requests.get(url+'proveedores/busqueda/id/'+str(request.POST['id_proveedores']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            proveedores = data['proveedores']
            mensaje = data['message']
         else:
            proveedores = []
         context = {'proveedores': proveedores, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Proveedor/ProveedorActualizar.html', context)
    
def actualizar_proveedor(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST ['direccion']
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'proveedores/id/{idTemporal}', json={'nombre': nombre,'telefono': telefono,'correo': correo,'direccion': direccion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'proveedores/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        proveedores = data['proveedores']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Proveedor/ProveedorActualizar.html', {'mensaje': mensaje,'proveedores':proveedores })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Proveedor/ProveedorActualizar.html', {'mensaje': mensaje,'proveedores':proveedores})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'proveedores/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            proveedores = data['proveedores']
            mensaje = data['message']
            return render(request, 'Proveedor/ProveedorActualizar.html', {'proveedores': proveedores})
        else:
            mensaje = data['message']
            return render(request, 'Proveedor/ProveedorActualizar.html', {'mensaje': mensaje,'proveedores':proveedores})

def eliminar_proveedor(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'proveedores/id/{idTemporal}')
        res = response.json()
        rsp_proveedores = requests.get(url + 'proveedores/') 
        if rsp_proveedores.status_code == 200:
            data = rsp_proveedores.json()
            proveedores = data['proveedores']
        else:
            proveedores = []
        mensaje = res['message']
        context = {'proveedores': proveedores, 'mensaje': mensaje}
        return render(request, 'Proveedor/BuscarProveedor.html', context)     
    
def buscar_proveedor(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'proveedores/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    proveedores = {}
                    proveedores = data['proveedores']
                    context = {'proveedores': proveedores, 'mensaje':mensaje}
                    return render(request, 'Proveedor/BuscarProveedor.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    proveedores = {}
                    proveedores = data['proveedores']
                    context = {'proveedores': proveedores, 'mensaje':mensaje}
                    return render(request, 'Proveedor/BuscarProveedor.html', context)
        else:
            response = requests.get(url+'proveedores/')
            if response.status_code == 200:
                data = response.json()
                proveedores = data['proveedores']
                mensaje = data['message']   
                return render(request, 'Proveedor/BuscarProveedor.html', {'proveedores': proveedores, 'mensaje': mensaje})
            else:
                proveedores = []
                mensaje = 'No se encontraron proveedores'
            return render(request, 'Proveedor/BuscarProveedor.html', {'proveedores': proveedores, 'mensaje': mensaje})


def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/proveedor')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list