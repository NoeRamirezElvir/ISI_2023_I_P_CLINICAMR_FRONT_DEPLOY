import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'https://clinicamr.onrender.com/api/'
#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
def eliminar_precio_historico_examen(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'precioHistoricoExamen/id/{idTemporal}')
            res = response.json()
            rsp_historicos = requests.get(url + 'precioHistoricoExamen/') 
            if rsp_historicos.status_code == 200:
                data = rsp_historicos.json()
                historicos = data['historicos']
            else:
                historicos = []
            mensaje = res['message']
            context = {'historicos': historicos, 'mensaje': mensaje}
            return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)     
    except:
        rsp_historicos = requests.get(url + 'precioHistoricoExamen/') 
        if rsp_historicos.status_code == 200:
            data = rsp_historicos.json()
            historicos = data['historicos']
        else:
            historicos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'historicos': historicos, 'error': mensaje}
        return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)     
    
def buscar_precio_historico_examen(request):
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
                    print(context)
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)       
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de examenes'
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'historicos': historicos, 'mensaje': mensaje})

            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    historicos = {}
                    historicos = data['historicos']
                    context = {'historicos': historicos, 'mensaje':mensaje}
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', context)
                else:
                    historicos = []
                    mensaje = 'No se encontrarón historicos de examenes'
                    return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'historicos': historicos, 'mensaje': mensaje})

        else:
            response = requests.get(url+'precioHistoricoExamen/')
            if response.status_code == 200:
                data = response.json()
                historicos = data['historicos']
                mensaje = data['message']   
                return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'historicos': historicos, 'mensaje': mensaje})
            else:
                historicos = []
                mensaje = 'No se encontrarón historicos de examenes'
            return render(request, 'precio_historico_examen/buscar_precio_historico_examen.html', {'historicos': historicos, 'mensaje': mensaje})
