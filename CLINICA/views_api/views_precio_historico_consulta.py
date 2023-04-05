import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
def eliminar_precio_historico_consulta(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'precioHistoricoConsulta/id/{idTemporal}')
        res = response.json()
        rsp_historicos = requests.get(url + 'precioHistoricoConsulta/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
        else:
            historicos = []
        mensaje = res['message']
        context = {'historicos': historicos, 'mensaje': mensaje}
        return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', context)     
    
def buscar_precio_historico_consulta(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'precioHistoricoExamen/busqueda/'

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
                    return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', context)       
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de examenes'
                    return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', {'historicos': historicos, 'mensaje': mensaje})

            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de examenes'
                    return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', {'historicos': historicos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'precioHistoricoConsulta/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', {'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón historicos de examenes'
            return render(request, 'precio_historico_consulta/buscar_precio_historico_consulta.html', {'historicos': historicos, 'mensaje': mensaje})
