from django.http import HttpResponse
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_correlativo(request):
    response = requests.get(url+'correlativo/')
    if response.status_code == 200:
        data = response.json()
        correlativo = data['correlativo']
    else:
        correlativo = []
    context = {'correlativo': correlativo}
    return render(request, 'correlativo/buscar_correlativo.html', context)

def crear_correlativo(request):
    if request.method == 'POST':
        cai = request.POST['cai']
        rangoInicial = int(request.POST['rangoInicial'])
        rangoFinal = int(request.POST['rangoFinal'])
        fechaLimiteEmision = request.POST['fechaLimiteEmision']
        
        

        registro_temp={'cai': cai, 
                       'rangoInicial': rangoInicial,
                       'rangoFinal': rangoFinal,                   
                       'fechaLimiteEmision': fechaLimiteEmision
                       }
        
        response = requests.post(url+'correlativo/', json={'cai': cai, 
                                                            'rangoInicial': rangoInicial,
                                                            'rangoFinal': rangoFinal,  
                                                            'fechaLimiteEmision': fechaLimiteEmision
                                                            })
        data = response.json()
        if response.status_code == 200:
        
            mensaje = data['message']
            return render(request, 'correlativo/correlativo.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'correlativo/correlativo.html', {'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'correlativo/correlativo.html')
    
def abrir_actualizar_correlativo(request):
    if request.method == 'POST':
         print(request.POST['id_correlativo'])
         resp = requests.get(url+'correlativo/busqueda/id/'+str(request.POST['id_correlativo']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            correlativo = data['correlativo']
            mensaje = data['message']
         else:
            correlativo = []
         context = {'correlativo': correlativo, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'correlativo/actualizar_correlativo.html', context)
    
def actualizar_correlativo(request, id):
    if request.method == 'POST':
        idTemporal = id
        cai = request.POST['cai']
        rangoInicial = int(request.POST['rangoInicial'])
        rangoFinal = int(request.POST['rangoFinal'])  
        fechaLimiteEmision = request.POST['fechaLimiteEmision']
        consecutivo = request.POST['consecutivo']
        
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'correlativo/id/{idTemporal}', json={'cai': cai, 
                                                                            'rangoInicial': rangoInicial,
                                                                            'rangoFinal': rangoFinal,
                                                                            'fechaLimiteEmision': fechaLimiteEmision,
                                                                            'consecutivo':consecutivo
                                                                            })
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'correlativo/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        correlativo = data['correlativo']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'correlativo/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            correlativo = data['correlativo']
            mensaje = data['message']
            return render(request, 'correlativo/actualizar_correlativo.html', {'correlativo':correlativo})
        else:
            mensaje = data['message']
            return render(request, 'correlativo/actualizar_correlativo.html', {'mensaje': mensaje,'correlativo':correlativo})

def eliminar_correlativo(request, id):
    if request.method == 'POST':
        idTemporal = id
        response = requests.delete(url + f'correlativo/id/{idTemporal}')
        res = response.json()
        rsp_correlativo = requests.get(url + 'correlativo/') 
        if rsp_correlativo.status_code == 200:
            data = rsp_correlativo.json()
            correlativo = data['correlativo']
        else:
            correlativo = []
        mensaje = res['message']
        context = {'correlativo': correlativo, 'mensaje': mensaje}
        return render(request, 'correlativo/buscar_correlativo.html', context)     
    
def buscar_correlativo(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'correlativo/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    correlativo = {}
                    correlativo = data['correlativo']
                    context = {'correlativo': correlativo, 'mensaje':mensaje}
                    return render(request, 'correlativo/buscar_correlativo.html', context)
                else:
                    correlativo = []
                    mensaje = 'No se encontraron correlativos'
                    return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje})
          
            else:
                response = requests.get(url2+'cai/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    correlativo = {}
                    correlativo = data['correlativo']
                    context = {'correlativo': correlativo, 'mensaje':mensaje}
                    return render(request, 'correlativo/buscar_correlativo.html', context)
                else:
                    correlativo = []
                    mensaje = 'No se encontraron correlativos'
                    return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'correlativo/')
            if response.status_code == 200:
                data = response.json()
                correlativo = data['correlativo']
                mensaje = data['message']   
                return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje})
            else:
                correlativo = []
                mensaje = 'No se encontraron correlativos'
            return render(request, 'correlativo/buscar_correlativo.html', {'correlativo': correlativo, 'mensaje': mensaje})
    