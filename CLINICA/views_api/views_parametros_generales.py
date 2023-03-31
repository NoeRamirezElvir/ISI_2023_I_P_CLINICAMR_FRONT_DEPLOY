from django.http import HttpResponse
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_parametros_generales(request):
    response = requests.get(url+'parametrosgenerales/')
    if response.status_code == 200:
        data = response.json()
        parametrosgenerales = data['parametrosgenerales']
    else:
        parametrosgenerales = []
    context = {'parametrosgenerales': parametrosgenerales}
    return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)

def crear_parametros_generales(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        valor = float(request.POST['valor'])
        registro_temp = {'nombre': nombre,'descripcion': descripcion, 'valor': valor}
        response = requests.post(url+'parametrosgenerales/', json={'nombre': nombre,'descripcion': descripcion, 'valor': valor})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'parametros_generales/parametros_generales.html', {'mensaje': mensaje, 'parametrosgenerales': registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'parametros_generales/parametros_generales.html', {'mensaje': mensaje, 'parametrosgenerales': registro_temp})
    else:
        return render(request, 'parametros_generales/parametros_generales.html')
    
def abrir_actualizar_parametros_generales(request):
    if request.method == 'POST':
         resp = requests.get(url+'parametrosgenerales/busqueda/id/'+str(request.POST['id_parametrosgenerales']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            parametrosgenerales = data['parametrosgenerales']
            mensaje = data['message']
         else:
            parametrosgenerales = []
         context = {'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'parametros_generales/Actualizar_parametros_generales.html', context)
    
def actualizar_parametros_generales(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        valor = float(request.POST['valor'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'parametrosgenerales/id/{idTemporal}', json={'nombre': nombre,'descripcion': descripcion, 'valor': valor})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'parametrosgenerales/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        parametrosgenerales = data['parametrosgenerales']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'mensaje': mensaje,'parametrosgenerales':parametrosgenerales })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'mensaje': mensaje,'parametrosgenerales':parametrosgenerales})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'parametrosgenerales/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            parametrosgenerales = data['parametrosgenerales']
            mensaje = data['message']
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'parametrosgenerales': parametrosgenerales})
        else:
            mensaje = data['message']
            return render(request, 'parametros_generales/Actualizar_parametros_generales.html', {'mensaje': mensaje,'parametrosgenerales':parametrosgenerales})

def eliminar_parametros_generales(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'parametrosgenerales/id/{idTemporal}')
        res = response.json()
        rsp_parametrosgenerales = requests.get(url + 'parametrosgenerales/') 
        if rsp_parametrosgenerales.status_code == 200:
            data = rsp_parametrosgenerales.json()
            parametrosgenerales = data['parametrosgenerales']
        else:
            parametrosgenerales = []
        mensaje = res['message']
        context = {'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje}
        return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)  
    
def buscar_parametros_generales(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'parametrosgenerales/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    parametrosgenerales = {}
                    parametrosgenerales = data['parametrosgenerales']
                    context = {'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
                    print(context)
                    return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    parametrosgenerales = {}
                    parametrosgenerales = data['parametrosgenerales']
                    context = {'parametrosgenerales': parametrosgenerales, 'mensaje':mensaje}
                    return render(request, 'parametros_generales/Buscar_parametros_generales.html', context)
        else:
            response = requests.get(url+'parametrosgenerales/')
            if response.status_code == 200:
                data = response.json()
                parametrosgenerales = data['parametrosgenerales']
                mensaje = data['message']   
                return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
            else:
                parametrosgenerales = []
                mensaje = 'No se encontraron parametros generales'
            return render(request, 'parametros_generales/Buscar_parametros_generales.html', {'parametrosgenerales': parametrosgenerales, 'mensaje': mensaje})
      