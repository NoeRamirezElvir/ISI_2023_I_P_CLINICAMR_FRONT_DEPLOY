from decimal import Decimal
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests

url = 'https://clinicamr.onrender.com/api/'
def listar_tipo(request):
    response = requests.get(url+'tipo/')
    if response.status_code == 200:
        data = response.json()
        tipo = data['tipos']
    else:
        tipo = []
    context = {'tipo': tipo}
    return render(request, 'Tipos/buscartipo.html', context)

def crear_tipo(request):
    Subtipo = list_subtipos()
    impuestos = list_impuesto()
    if request.method == 'POST':
        idsubtipo = int(request.POST['idsubtipo'])
        idImpuesto = int(request.POST.get('idImpuesto', 0))
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        if 'precio' in request.POST: #Validar que precio este en la consulta, si no esta es que viene como 0 o vacio
            precio = request.POST['precio']
        else:
            precio = '0.00'

        registro_temp = {'nombre': nombre, 'descripcion': descripcion,'idImpuesto': idImpuesto,'idsubtipo':idsubtipo, 'precio': precio}
        response = requests.post(url+'tipo/', json={'nombre': nombre, 'descripcion': descripcion,'idImpuesto': idImpuesto,'idsubtipo':idsubtipo, 'precio':precio})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']

            return render(request, 'Tipos/tipo.html', {'mensaje': mensaje,'subtipo': Subtipo,'impuestos': impuestos, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'Tipos/tipo.html', {'mensaje': mensaje,'subtipo': Subtipo,'impuestos': impuestos, 'registro_temp':registro_temp})
    else:
        return render(request, 'Tipos/tipo.html',{'subtipo': Subtipo,'impuestos': impuestos})
    
def abrir_actualizar_tipo(request):
    subtipos = list_subtipos()
    impuestos = list_impuesto()
    if request.method == 'POST':
         resp = requests.get(url+'tipo/busqueda/id/'+str(request.POST['id_tipos']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            tipo = data['tipos']
            mensaje = data['message']
         else:
            tipo = []
         context = {'tipo': tipo,'subtipo': subtipos,'impuestos': impuestos, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Tipos/tipoactualizar.html', context)
    
def actualizar_tipo(request, id):
    subtipo = list_subtipos()
    impuestos = list_impuesto()
    if request.method == 'POST':
        idTemporal = id
        idsubtipo = int(request.POST['idsubtipo'])
        idImpuesto = int(request.POST.get('idImpuesto', 0))
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        if 'precio' in request.POST: #Validar que precio este en la consulta, si no esta es que viene como 0 o vacio
            precio = request.POST['precio']
        else:
            precio = '0.00'
        
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'tipo/id/{idTemporal}', json={'idsubtipo': idsubtipo,'idImpuesto': idImpuesto,'nombre': nombre, 'descripcion': descripcion, 'precio':precio})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el tipo relacionado con el id
        res = requests.get(url+f'tipo/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        tipo = data['tipos']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Tipos/tipoactualizar.html', {'mensaje': mensaje,'tipo':tipo,'subtipo':subtipo, 'impuestos': impuestos })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Tipos/tipoactualizar.html', {'mensaje': mensaje,'tipo':tipo,'subtipo':subtipo, 'impuestos': impuestos})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'tipo/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            tipo = data['tipos']
            mensaje = data['message']
            return render(request, 'Tipos/tipoactualizar.html', {'tipo': tipo,'subtipo':subtipo,'idImpuesto': idImpuesto, 'impuestos': impuestos})
        else:
            mensaje = data['message']
            return render(request, 'Tipos/tipoactualizar.html', {'mensaje': mensaje,'tipo':tipo,'idImpuesto': idImpuesto,'subtipo':subtipo, 'impuestos': impuestos})

def eliminar_tipo(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'tipo/id/{idTemporal}')
            res = response.json()
            rsp_tipo = requests.get(url + 'tipo/') 
            if rsp_tipo.status_code == 200:
                data = rsp_tipo.json()
                tipo = data['tipos']
            else:
                tipo = []
            mensaje = res['message']
            context = {'tipo': tipo, 'mensaje': mensaje}
            return render(request, 'Tipos/buscartipo.html', context)     
    except:
        rsp_tipo = requests.get(url + 'tipo/') 
        if rsp_tipo.status_code == 200:
            data = rsp_tipo.json()
            tipo = data['tipos']
        else:
            tipo = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'tipo': tipo, 'error': mensaje}
        return render(request, 'Tipos/buscartipo.html', context)     
    
def buscar_tipo(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'tipo/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tipo = {}
                    tipo = data['tipos']
                    context = {'tipo': tipo, 'mensaje':mensaje}
                    return render(request, 'Tipos/buscartipo.html', context)
                else:
                    tipo = []
                    mensaje = 'No se encontraron tipo'
                    return render(request, 'Tipos/buscartipo.html', {'tipo': tipo, 'mensaje': mensaje})       
            else:
                response = requests.get(url2+'nombre/'+valor)
                data = response.json()
                if data['tipos']:
                    mensaje = data['message']
                    tipo = {}
                    tipo = data['tipos']
                    context = {'tipo': tipo, 'mensaje':mensaje}
                    return render(request, 'Tipos/buscartipo.html', context)
                else:
                    response = requests.get(url2+'subtipo/'+valor)
                    data = response.json()
                    if data['tipos']:
                        mensaje = data['message']
                        tipo = {}
                        tipo = data['tipos']
                        context = {'tipo': tipo, 'mensaje':mensaje}
                        return render(request, 'Tipos/buscartipo.html', context)
                    else:
                        tipo = []
                        mensaje = 'No se encontraron tipo'
                        return render(request, 'Tipos/buscartipo.html', {'tipo': tipo, 'mensaje': mensaje})
        else:
            response = requests.get(url+'tipo/')
            if response.status_code == 200:
                data = response.json()
                tipo = data['tipos']
                mensaje = data['message']   
                return render(request, 'Tipos/buscartipo.html', {'tipo': tipo, 'mensaje': mensaje})
            else:
                tipo = []
                mensaje = 'No se encontraron tipo'
            return render(request, 'Tipos/buscartipo.html', {'tipo': tipo, 'mensaje': mensaje})


def list_subtipos():
    rsp_subtipo = requests.get(url+'subtipo/')
    if rsp_subtipo.status_code == 200:
        data = rsp_subtipo.json()
        subtipo = data['subtipo']
        return subtipo
    else:
        subtipo= []
        return subtipo
    
def list_impuesto():
    rsp_impuesto = requests.get(url+'Impuestos/')
    if rsp_impuesto.status_code == 200:
        data = rsp_impuesto.json()
        impuesto = data['Impuestos']
        return impuesto
    else:
        impuesto= []
        return impuesto