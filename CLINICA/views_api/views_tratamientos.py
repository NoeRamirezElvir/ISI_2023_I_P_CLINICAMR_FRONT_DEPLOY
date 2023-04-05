from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_tratamientos(request):
    response = requests.get(url+'tratamientos/')
    if response.status_code == 200:
        data = response.json()
        tratamientos = data['tratamientos']
    else:
        tratamientos = []
    context = {'tratamientos': tratamientos}
    return render(request, 'tratamiento/Buscar_tratamiento.html', context)

def crear_tratamientos(request):
    pacientes_list = list_pacientes()
    tipo_list = list_tipos()

    if request.method == 'POST':
        idPaciente = int(request.POST['idPaciente'])
        idTipo = int(request.POST['idTipo'])
        fecha = request.POST['fecha']
        diasTratamiento = int(request.POST['diasTratamiento'])
        estado = request.POST['estado']
        registro_temp = {'idPaciente': idPaciente, 'idTipo': idTipo, 'fecha': fecha, 'diasTratamiento':diasTratamiento, 'estado':estado}
        response = requests.post(url+'tratamientos/', json={'idPaciente': idPaciente, 'idTipo': idTipo, 'fecha': fecha, 'diasTratamiento':diasTratamiento, 'estado':estado})
        data = response.json()
        if response.status_code == 200:
            mensaje = data['message']
            return render(request, 'tratamiento/tratamiento.html', {'mensaje': mensaje, 'registro_temp':registro_temp, 'paciente_list':pacientes_list, 'tipo_list':tipo_list})
        else:
            mensaje = data['message']
            return render(request, 'tratamiento/tratamiento.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'paciente_list':pacientes_list, 'tipo_list':tipo_list})
    else:
        return render(request, 'tratamiento/tratamiento.html', {'paciente_list':pacientes_list, 'tipo_list':tipo_list})
    
def abrir_actualizar_tratamientos(request):
    pacientes_list = list_pacientes()
    tipo_list = list_tipos()
    if request.method == 'POST':
         resp = requests.get(url+'tratamientos/busqueda/id/'+str(request.POST['id_tratamientos']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            tratamientos = data['tratamientos']
            mensaje = data['message']
         else:
            tratamientos = []
         context = {'tratamientos': tratamientos, 'mensaje':mensaje, 'paciente_list':pacientes_list, 'tipo_list':tipo_list}
         mensaje = data['message']
         return render(request, 'tratamiento/Actualizar_tratamiento.html', context)
    
def actualizar_tratamientos(request, id):
    pacientes_list = list_pacientes()
    tipo_list = list_tipos()
    if request.method == 'POST':
        idTemporal = id
        idPaciente = int(request.POST['idPaciente'])
        idTipo = int(request.POST['idTipo'])
        fecha = request.POST['fecha']
        diasTratamiento = int(request.POST['diasTratamiento'])
        estado = request.POST['estado']
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'tratamientos/id/{idTemporal}', json={'idPaciente': idPaciente, 'idTipo': idTipo, 'fecha': fecha, 'diasTratamiento':diasTratamiento, 'estado':estado})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'tratamientos/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        tratamientos = data['tratamientos']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'tratamiento/Actualizar_tratamiento.html', {'mensaje': mensaje,'tratamientos':tratamientos,'paciente_list':pacientes_list, 'tipo_list':tipo_list})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'tratamiento/Actualizar_tratamiento.html', {'mensaje': mensaje,'tratamientos':tratamientos,'paciente_list':pacientes_list, 'tipo_list':tipo_list})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'tratamientos/busqueda/id/{idTemporal}')
        data = response.json()
        if response.status_code == 200:
            tratamientos = data['tratamientos']
            mensaje = data['message']
            return render(request, 'tratamiento/Actualizar_tratamiento.html', {'tratamientos': tratamientos, 'paciente_list':pacientes_list, 'tipo_list':tipo_list})
        else:
            mensaje = data['message']
            return render(request, 'tratamiento/Actualizar_tratamiento.html', {'mensaje': mensaje,'tratamientos':tratamientos, 'paciente_list':pacientes_list, 'tipo_list':tipo_list})

def eliminar_tratamientos(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'tratamientos/id/{idTemporal}')
        res = response.json()
        rsp_tratamientos = requests.get(url + 'tratamientos/') 
        if rsp_tratamientos.status_code == 200:
            data = rsp_tratamientos.json()
            tratamientos = data['tratamientos']
        else:
            tratamientos = []
        mensaje = res['message']
        context = {'tratamientos': tratamientos, 'mensaje': mensaje}
        return render(request, 'tratamiento/Buscar_tratamiento.html', context)     
    
def buscar_tratamientos(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'tratamientos/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tratamientos = {}
                    tratamientos = data['tratamientos']
                    context = {'tratamientos': tratamientos, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'tratamiento/Buscar_tratamiento.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tratamientos = {}
                    tratamientos = data['tratamientos']
                    context = {'tratamientos': tratamientos, 'mensaje':mensaje}
                    return render(request, 'tratamiento/Buscar_tratamiento.html', context)
                else:
                    tratamientos = []
                    mensaje = 'No se encontraron muestras'
                    return render(request, 'tratamiento/Buscar_tratamiento.html', {'tratamientos': tratamientos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'tratamientos/')
            if response.status_code == 200:
                data = response.json()
                tratamientos = data['tratamientos']
                mensaje = data['message']   
                return render(request, 'tratamiento/Buscar_tratamiento.html', {'tratamientos': tratamientos, 'mensaje': mensaje})
            else:
                tratamientos = []
                mensaje = 'No se encontraron muestras'
            return render(request, 'tratamiento/Buscar_tratamiento.html', {'tratamientos': tratamientos, 'mensaje': mensaje})

def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/tratamiento')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list

def list_pacientes():
    rsp_paciente = requests.get(url+'pacientes/')
    if rsp_paciente.status_code == 200:
        data = rsp_paciente.json()
        pacientes_list = data['pacientes']
        return pacientes_list
    else:
        pacientes_list = []
        return pacientes_list

