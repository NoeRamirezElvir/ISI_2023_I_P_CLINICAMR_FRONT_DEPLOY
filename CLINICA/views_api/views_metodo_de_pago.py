from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_metodos_De_pago(request):
    response = requests.get(url+'metodop/')
    if response.status_code == 200:
        data = response.json()
        metodop = data['metodop']
        if not metodop:
            metodop = []
    else:
        metodop = []
    context = {'metodop': metodop}
    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)


def crear_metodos_De_pago(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        
        registro_temp={'nombre': nombre, 'descripcion': descripcion}
        response = requests.post(url+'metodop/', json={'nombre': nombre, 'descripcion': descripcion})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'MetodoDePago/MetodoDePago.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'MetodoDePago/MetodoDePago.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'MetodoDePago/MetodoDePago.html')
    
def abrir_actualizar_metodos_De_pago(request):
    if request.method == 'POST':
         resp = requests.get(url+'metodop/busqueda/id/'+str(request.POST['id_metodo']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            metodop = data['metodop']
            mensaje = data['message']
         else:
            metodop = []
         context = {'metodop': metodop, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', context)
    
def actualizar_metodos_De_pago(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'metodop/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'metodop/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        metodop = data['metodop']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'mensaje': mensaje,'metodop':metodop })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'mensaje': mensaje,'metodop':metodop})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'metodop/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            metodop = data['metodop']
            mensaje = data['message']
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'metodop': metodop})
        else:
            mensaje = data['message']
            return render(request, 'MetodoDePago/ActualizarMetodoDePago.html', {'mensaje': mensaje,'metodop':metodop})

def eliminar_metodos_De_pago(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'metodop/id/{idTemporal}')
        res = response.json()
        rsp_metodop = requests.get(url + 'metodop/') 
        if rsp_metodop.status_code == 200:
            data = rsp_metodop.json()
            metodop = data['metodop']
        else:
            metodop = []
        mensaje = res['message']
        context = {'metodop': metodop, 'mensaje': mensaje}
        return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)     
    
def buscar_metodos_De_pago(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'metodop/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    metodop = {}
                    metodop = data['metodop']
                    context = {'metodop': metodop, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    metodop = {}
                    metodop = data['metodop']
                    context = {'metodop': metodop, 'mensaje':mensaje}
                    return render(request, 'MetodoDePago/BuscarMetodoDePago.html', context)
        else:
            response = requests.get(url+'metodop/')
            if response.status_code == 200:
                data = response.json()
                metodop = data['metodop']
                mensaje = data['message']   
                return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'metodop': metodop, 'mensaje': mensaje})
            else:
                metodop = []
                mensaje = 'No se encontraron Metodos de pago'
            return render(request, 'MetodoDePago/BuscarMetodoDePago.html', {'metodop': metodop, 'mensaje': mensaje})
    