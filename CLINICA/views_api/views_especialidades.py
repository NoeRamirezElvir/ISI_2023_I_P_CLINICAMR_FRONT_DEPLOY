from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_especialidades(request):
    response = requests.get(url+'especialidad/')
    if response.status_code == 200:
        data = response.json()
        especialidad = data['especialidad']
        if not especialidad:
            especialidad = []
    else:
        especialidad = []
    context = {'especialidad': especialidad}
    return render(request, 'especialidad/BuscarEspecialidad.html', context)


def crear_especialidades(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        
        registro_temp={'nombre': nombre, 'descripcion': descripcion}
        response = requests.post(url+'especialidad/', json={'nombre': nombre, 'descripcion': descripcion})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'especialidad/especialidad.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'especialidad/especialidad.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'especialidad/especialidad.html')
    
def abrir_actualizar_especialidades(request):
    if request.method == 'POST':
         resp = requests.get(url+'especialidad/busqueda/id/'+str(request.POST['id_especialidad']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            especialidad = data['especialidad']
            mensaje = data['message']
         else:
            especialidad = []
         context = {'especialidad': especialidad, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'especialidad/especialidadActualizar.html', context)
    
def actualizar_especialidades(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'especialidad/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'especialidad/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        especialidad = data['especialidad']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'especialidad/especialidadActualizar.html', {'mensaje': mensaje,'especialidad':especialidad })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'especialidad/especialidadActualizar.html', {'mensaje': mensaje,'especialidad':especialidad})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'especialidad/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            usuario = data['especialidad']
            mensaje = data['message']
            return render(request, 'especialidad/especialidadActualizar.html', {'especialidad': especialidad})
        else:
            mensaje = data['message']
            return render(request, 'especialidad/especialidadActualizar.html', {'mensaje': mensaje,'especialidad':especialidad})

def eliminar_especialidades(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'especialidad/id/{idTemporal}')
        res = response.json()
        rsp_especialidad = requests.get(url + 'especialidad/') 
        if rsp_especialidad.status_code == 200:
            data = rsp_especialidad.json()
            especialidad = data['especialidad']
        else:
            especialidad = []
        mensaje = res['message']
        context = {'especialidad': especialidad, 'mensaje': mensaje}
        return render(request, 'especialidad/BuscarEspecialidad.html', context)     
    
def buscar_especialidades(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'especialidad/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    especialidad = {}
                    especialidad = data['especialidad']
                    context = {'especialidad': especialidad, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'especialidad/BuscarEspecialidad.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    especialidad = {}
                    especialidad = data['especialidad']
                    context = {'especialidad': especialidad, 'mensaje':mensaje}
                    return render(request, 'especialidad/BuscarEspecialidad.html', context)
        else:
            response = requests.get(url+'especialidad/')
            if response.status_code == 200:
                data = response.json()
                especialidad = data['especialidad']
                mensaje = data['message']   
                return render(request, 'especialidad/BuscarEspecialidad.html', {'especialidad': especialidad, 'mensaje': mensaje})
            else:
                especialidad = []
                mensaje = 'No se encontraron especialidades'
            return render(request, 'especialidad/BuscarEspecialidad.html', {'especialidad': especialidad, 'mensaje': mensaje})
    