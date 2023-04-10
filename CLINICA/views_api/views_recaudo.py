from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'

def crear_recaudo(request):
    pacientes_list = list_pacientes()
    empleados_list = list_empleados()
    consultas_list = list_consultas()
    medicamentos_list = list_medicamentos()
    tratamientos_list = list_tratamientos()
    examenes_list = list_examenes()
    context = {'pacientes_list':pacientes_list,
                   'empleados_list':empleados_list,
                   'consultas_list':consultas_list,
                   'medicamentos_list':medicamentos_list,
                   'tratamientos_list':tratamientos_list,
                   'examenes_list':examenes_list,}
    if request.method == 'POST':
        pass
    else:
        return render(request, 'recaudo/recaudo.html', context)
    
def abrir_actualizar_sintomas(request):
    if request.method == 'POST':
         resp = requests.get(url+'sintomas/busqueda/id/'+str(request.POST['id_sintoma']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            sintomas = data['sintomas']
            mensaje = data['message']
         else:
            sintomas = []
         context = {'sintomas': sintomas, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'sintomas/actualizar_sintomas.html', context)
    
def actualizar_sintomas(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']

        response = requests.put(url+f'sintomas/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
        rsp =  response.json()

        res = requests.get(url+f'sintomas/busqueda/id/{idTemporal}')
        data = res.json()
        sintomas = data['sintomas']
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'sintomas/actualizar_sintomas.html', {'mensaje': mensaje,'sintomas':sintomas })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'sintomas/actualizar_sintomas.html', {'mensaje': mensaje,'sintomas':sintomas})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'sintomas/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            sintomas = data['sintomas']
            mensaje = data['message']
            return render(request, 'sintomas/actualizar_sintomas.html', {'sintomas': sintomas})
        else:
            mensaje = data['message']
            return render(request, 'sintomas/actualizar_sintomas.html', {'mensaje': mensaje,'sintomas':sintomas})
        
def list_consultas():
    rsp_consultas = requests.get(url+'consultas/')
    if rsp_consultas.status_code == 200:
        data = rsp_consultas.json()
        list_consultas = data['consultas']
        return list_consultas
    else:
        list_consultas = []
        return list_consultas
    
def list_medicamentos():
    rsp_medicamentos = requests.get(url+'medicamentos/')
    if rsp_medicamentos.status_code == 200:
        data = rsp_medicamentos.json()
        list_medicamentos = data['medicamentos']
        return list_medicamentos
    else:
        list_medicamentos = []
        return list_medicamentos
    
def list_tratamientos():
    rsp_tratamientos = requests.get(url+'tratamientos/')
    if rsp_tratamientos.status_code == 200:
        data = rsp_tratamientos.json()
        list_tratamientos = data['tratamientos']
        return list_tratamientos
    else:
        list_tratamientos = []
        return list_tratamientos
    
def list_examenes():
    rsp_examenes = requests.get(url+'examen/')
    if rsp_examenes.status_code == 200:
        data = rsp_examenes.json()
        list_examenes = data['examenes']
        return list_examenes
    else:
        list_examenes = []
        return list_examenes
    
def list_pacientes():
    rsp_pacientes = requests.get(url+'pacientes/')
    if rsp_pacientes.status_code == 200:
        data = rsp_pacientes.json()
        list_pacientes = data['pacientes']
        return list_pacientes
    else:
        list_pacientes = []
        return list_pacientes
    
def list_empleados():
    rsp_empleados = requests.get(url+'empleados/')
    if rsp_empleados.status_code == 200:
        data = rsp_empleados.json()
        list_empleados = data['empleados']
        return list_empleados
    else:
        list_empleados = []
        return list_empleados