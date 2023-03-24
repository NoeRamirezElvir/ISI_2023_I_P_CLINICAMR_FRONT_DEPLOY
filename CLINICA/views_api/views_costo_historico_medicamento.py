import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
def eliminar_costo_historico_medicamento(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'costoHistoricoMedicamento/id/{idTemporal}')
        res = response.json()
        rsp_historicos = requests.get(url + 'costoHistoricoMedicamento/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
        else:
            historicos = []
        mensaje = res['message']
        context = {'historicos': historicos, 'mensaje': mensaje}
        return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)     
    
def buscar_costo_historico_medicamento(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'costoHistoricoMedicamento/busqueda/'

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
                    return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', context)
        else:
            response = requests.get(url+'costoHistoricoMedicamento/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón citas'
            return render(request, 'costo_historico_medicamento/buscar_costo_historico_medicamento.html', {'historicos': historicos, 'mensaje': mensaje})
