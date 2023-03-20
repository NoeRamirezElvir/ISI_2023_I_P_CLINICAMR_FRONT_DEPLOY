import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_impuesto_historico(request):
    response = requests.get(url+'impuestoHistorico/')
    if response.status_code == 200:
        data = response.json()
        historicos = data['historicos']
    else:
        citas  = []
    context = {'historicos': historicos}
    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_impuesto_historico(request):
    rsp_paciente = requests.get(url+'Impuestos/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            impuestos_list = data['Impuestos']
    else:
            impuestos_list = []
    if request.method == 'POST':
        idImpuesto = int(request.POST['idImpuesto'])
        valor= float(request.POST ['valor'])
        registro_temp = {'idImpuesto':idImpuesto,'valor': valor}
        response = requests.post(url+'impuestoHistorico/', json={'idImpuesto':idImpuesto,'valor': valor})
        pacientedata={}
        if response.status_code == 200:
            pacientedata = response.json()
            mensaje = pacientedata['message']
            return render(request, 'impuesto_historico/impuesto_historico.html', {'mensaje': mensaje,  'impuesto_list': impuestos_list, 'registro_temp':registro_temp})
        else:
            mensaje = pacientedata['message']
            
            return render(request, 'impuesto_historico/impuesto_historico.html', {'mensaje': mensaje,  'impuesto_list': impuestos_list, 'registro_temp':registro_temp})
    else:
        return render(request, 'impuesto_historico/impuesto_historico.html', { 'impuesto_list': impuestos_list})


def abrir_actualizar_impuesto_historico(request):
    rsp_paciente = requests.get(url+'Impuestos/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            impuestos_list = data['Impuestos']
    else:
            impuestos_list = []
    if request.method == 'POST':
         resp = requests.get(url+'impuestoHistorico/busqueda/id/'+str(request.POST['id_historicos']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            historicos = data['historicos']
            mensaje = data['message']
         else:
            historicos = []
         context = {'historicos': historicos,'impuesto_list': impuestos_list, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'impuesto_historico/impuesto_historico_actualizar.html', context)   
    
def actualizar_impuesto_historico(request, id):
    rsp_paciente = requests.get(url+'Impuestos/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            impuestos_list = data['Impuestos']
    else:
            impuestos_list = []
    if request.method == 'POST':
        idTemporal = id
        idImpuesto = int(request.POST['idImpuesto'])
        valor= float(request.POST ['valor'])

        response = requests.put(url+f'impuestoHistorico/id/{idTemporal}',json={'idImpuesto':idImpuesto,'valor': valor})
        rsp =  response.json()
        res = requests.get(url+f'impuestoHistorico/busqueda/id/{idTemporal}')
        data = res.json()
        historicos = data['historicos']
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'impuesto_historico/impuesto_historico_actualizar.html', {'mensaje': mensaje,'historicos':historicos, 'impuesto_list':impuestos_list})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'impuesto_historico/impuesto_historico_actualizar.html', {'mensaje': mensaje,'historicos':historicos, 'impuesto_list':impuestos_list})
    else:
        idTemporal = id
        response = requests.get(url+f'impuestoHistorico/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            historicos = data['historicos']
            mensaje = data['message']
            return render(request, 'impuesto_historico/impuesto_historico_actualizar.html', {'historicos': historicos, 'impuesto_list':impuestos_list})
        else:
            mensaje = data['message']
            return render(request, 'impuesto_historico/impuesto_historico_actualizar.html', {'mensaje': mensaje,'historicos':historicos, 'impuesto_list':impuestos_list})

def eliminar_impuesto_historico(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'impuestoHistorico/id/{idTemporal}')
        res = response.json()
        rsp_pacientes = requests.get(url + 'impuestoHistorico/') 
        if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            historicos = data['historicos']
        else:
            historicos = []
        mensaje = res['message']
        context = {'historicos': historicos, 'mensaje': mensaje}
        return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)     
    
def buscar_impuesto_historico(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'impuestoHistorico/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'historicos': historicos, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'impuesto_historico/impuesto_historico_buscar.html', context)
        else:
            response = requests.get(url+'impuestoHistorico/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón citas'
            return render(request, 'impuesto_historico/impuesto_historico_buscar.html', {'historicos': historicos, 'mensaje': mensaje})
