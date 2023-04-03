from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_examenes(request):
    response = requests.get(url+'examen/')
    if response.status_code == 200:
        data = response.json()
        examenes = data['examenes']
    else:
        examenes = []
    context = {'examenes': examenes}
    return render(request, 'examen/buscar_examen.html', context)

def crear_examenes(request):
    muestras_list = list_muestras()
    tipo_list = list_tipos()
    laboratorios_list = list_laboratorios()

    if request.method == 'POST':
        idMuestra = int(request.POST['idMuestra'])
        idTipo = int(request.POST['idTipo'])
        fechaProgramada = request.POST['fechaProgramada']
        observacion = request.POST['observacion']
        idLaboratorio = int(request.POST['idLaboratorio'])
        registro_temp = {'idMuestra': idMuestra, 'idTipo': idTipo, 'fechaProgramada': fechaProgramada, 'observacion':observacion, 'idLaboratorio':idLaboratorio}
        response = requests.post(url+'examen/', json={'idMuestra': idMuestra, 'idTipo': idTipo, 'fechaProgramada': fechaProgramada, 'observacion':observacion, 'idLaboratorio':idLaboratorio})
        data = response.json()
        if response.status_code == 200:
            mensaje = data['message']
            return render(request, 'examen/examen.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
        else:
            mensaje = data['message']
            return render(request, 'examen/examen.html', {'mensaje': mensaje,'registro_temp':registro_temp, 'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
    else:
        return render(request, 'examen/examen.html', {'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
    
def abrir_actualizar_examenes(request):
    muestras_list = list_muestras()
    tipo_list = list_tipos()
    laboratorios_list = list_laboratorios()
    if request.method == 'POST':
         print(request.POST['id_examenes'])
         resp = requests.get(url+'examen/busqueda/id/'+str(request.POST['id_examenes']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            examenes = data['examenes']
            mensaje = data['message']
         else:
            examenes = []
         context = {'examenes': examenes, 'mensaje':mensaje,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list}
         mensaje = data['message']
         return render(request, 'examen/actualizar_examen.html', context)
    
def actualizar_examenes(request, id):
    muestras_list = list_muestras()
    tipo_list = list_tipos()
    laboratorios_list = list_laboratorios()
    if request.method == 'POST':
        idTemporal = id
        idMuestra = int(request.POST['idMuestra'])
        idTipo = int(request.POST['idTipo'])
        fechaProgramada = request.POST['fechaProgramada']
        observacion = request.POST['observacion']
        idLaboratorio = int(request.POST['idLaboratorio'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'examen/id/{idTemporal}', json={'idMuestra': idMuestra, 'idTipo': idTipo, 'fechaProgramada': fechaProgramada, 'observacion':observacion, 'idLaboratorio':idLaboratorio})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'examen/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        examenes = data['examenes']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'examen/actualizar_examen.html', {'mensaje': mensaje,'examenes':examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'examen/actualizar_examen.html', {'mensaje': mensaje,'examenes':examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'examen/busqueda/id/{idTemporal}')
        data = response.json()
        if response.status_code == 200:
            examenes = data['examenes']
            mensaje = data['message']
            return render(request, 'examen/actualizar_examen.html', {'examenes': examenes,'muestra_list':muestras_list, 'tipo_list':tipo_list, 'laboratorio_list':laboratorios_list})
        else:
            mensaje = data['message']
            return render(request, 'examen/actualizar_examen.html', {'mensaje': mensaje,'examenes':examenes, 'muestras_list':muestras_list, 'tipo_list':tipo_list})

def eliminar_examenes(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'examen/id/{idTemporal}')
        res = response.json()
        rsp_examenes = requests.get(url + 'examen/') 
        if rsp_examenes.status_code == 200:
            data = rsp_examenes.json()
            examenes = data['examenes']
        else:
            examenes = []
        mensaje = res['message']
        context = {'examenes': examenes, 'mensaje': mensaje}
        return render(request, 'examen/buscar_examen.html', context)     
    
def buscar_examenes(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'examen/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['examenes']:
                    data = response.json()
                    mensaje = data['message']
                    examenes = {}
                    examenes = data['examenes']
                    context = {'examenes': examenes, 'mensaje':mensaje}
                    return render(request, 'examen/buscar_examen.html', context)
                else:        
                    response = requests.get(url2+'documento/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        examenes = {}
                        examenes = data['examenes']
                        context = {'examenes': examenes, 'mensaje':mensaje}
                        return render(request, 'examen/buscar_examen.html', context)
            else:
                response = requests.get(url2+'documento/'+valor)
                data = response.json()
                if data['examenes']:
                    data = response.json()
                    mensaje = data['message']
                    examenes = {}
                    examenes = data['examenes']
                    context = {'examenes': examenes, 'mensaje':mensaje}
                    return render(request, 'examen/buscar_examen.html', context)
                else:        
                    response = requests.get(url2+'nombre/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        examenes = {}
                        examenes = data['examenes']
                        context = {'examenes': examenes, 'mensaje':mensaje}
                        return render(request, 'examen/buscar_examen.html', context)
        else:
            response = requests.get(url+'examen/')
            if response.status_code == 200:
                data = response.json()
                examenes = data['examenes']
                mensaje = data['message']   
                return render(request, 'examen/buscar_examen.html', {'examenes': examenes, 'mensaje': mensaje})
            else:
                examenes = []
                mensaje = 'No se encontraron muestras'
            return render(request, 'examen/buscar_examen.html', {'examenes': examenes, 'mensaje': mensaje})

def list_tipos():
    rsp_tipo = requests.get(url+'tipo/busqueda/subtipo/examen')
    if rsp_tipo.status_code == 200:
        data = rsp_tipo.json()
        tipos_list = data['tipos']
        return tipos_list
    else:
        tipos_list = []
        return tipos_list

def list_muestras():
    rsp_muestra= requests.get(url+'muestras/')
    if rsp_muestra.status_code == 200:
        data = rsp_muestra.json()
        muestras_list = data['muestras']
        return muestras_list
    else:
        muestras_list = []
        return muestras_list
    
def list_laboratorios():
    rsp_laboratorios= requests.get(url+'laboratorios/')
    if rsp_laboratorios.status_code == 200:
        data = rsp_laboratorios.json()
        laboratorios_list = data['laboratorios']
        return laboratorios_list
    else:
        laboratorios_list = []
        return laboratorios_list