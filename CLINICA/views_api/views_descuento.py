from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes

url = 'https://clinicamr.onrender.com/api/'
def listar_Descuentos(request):
    response = requests.get(url+'Descuentos/')
    if response.status_code == 200:
        data = response.json()
        Descuentos = data['Descuentos']
    else:
        Descuentos = []
    context = {'Descuentos': Descuentos}
    return render(request, 'Descuentos/BuscarDescuento.html', context)

def crear_Descuentos(request):
    
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        valor = float(request.POST['valor'])
        registro_temp = {'nombre': nombre, 'valor': valor}
        response = requests.post(url+'Descuentos/', json={'nombre': nombre, 'valor': valor})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Descuentos/Descuento.html', {'mensaje': mensaje, 'Descuentos': registro_temp,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            mensaje = data['message']
            return render(request, 'Descuentos/Descuento.html', {'mensaje': mensaje, 'Descuentos': registro_temp,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    else:
        return render(request, 'Descuentos/Descuento.html',{'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    
def abrir_actualizar_Descuentos(request):
    
    
    if request.method == 'POST':
         resp = requests.get(url+'Descuentos/busqueda/id/'+str(request.POST['id_Descuentos']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            Descuentos = data['Descuentos']
            mensaje = data['message']
         else:
            Descuentos = []
         context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
         mensaje = data['message']
         return render(request, 'Descuentos/DescuentoActualizar.html', context)
    
def actualizar_Descuentos(request, id):
    
    
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        valor = float(request.POST['valor'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'Descuentos/id/{idTemporal}', json={'nombre': nombre, 'valor': valor})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'Descuentos/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        Descuentos = data['Descuentos']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Descuentos':Descuentos ,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Descuentos':Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'Descuentos/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            Descuentos = data['Descuentos']
            mensaje = data['message']
            return render(request, 'Descuentos/DescuentoActualizar.html', {'Descuentos': Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            mensaje = data['message']
            return render(request, 'Descuentos/DescuentoActualizar.html', {'mensaje': mensaje,'Descuentos':Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})

def eliminar_Descuentos(request, id):
    
      
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'Descuentos/id/{idTemporal}')
            res = response.json()
            rsp_Descuentos = requests.get(url + 'Descuentos/') 
            context ={}
            if rsp_Descuentos.status_code == 200:
                data = rsp_Descuentos.json()
                Descuentos = data['Descuentos']
                context = {'Descuentos': Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
            else:
                Descuentos = []
                mensaje = res['message']
                context = {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
            return render(request, 'Descuentos/BuscarDescuento.html', context) 
    except:
        rsp_Descuentos = requests.get(url + 'Descuentos/') 
        context ={}
        if  rsp_Descuentos.status_code == 200:
            data = rsp_Descuentos.json()
            Descuentos = data['Descuentos']
            context = {'Descuentos': Descuentos,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario(),'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
        else:
            Descuentos = []
        mensaje = 'No se puede eliminar, esta siendo utilizando en otros registros'
        context = {'Descuentos': Descuentos, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
        return render(request, 'Descuentos/BuscarDescuento.html', context)
    
def buscar_Descuentos(request):
        
        
        valor = request.GET.get('buscador', None)
        url2 = url + 'Descuentos/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    Descuentos = {}
                    Descuentos = data['Descuentos']
                    context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
                    return render(request, 'Descuentos/BuscarDescuento.html', context)   
                else:
                    Descuentos = []
                    mensaje = 'No se encontraron registros'
                    return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    Descuentos = {}
                    Descuentos = data['Descuentos']
                    context = {'Descuentos': Descuentos, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()}
                    return render(request, 'Descuentos/BuscarDescuento.html', context)
                else:
                    Descuentos = []
                    mensaje = 'No se encontraron registros'
                    return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
        else:
            response = requests.get(url+'Descuentos/')
            if response.status_code == 200:
                data = response.json()
                Descuentos = data['Descuentos']
                mensaje = data['message']   
                return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
            else:
                Descuentos = []
                mensaje = 'No se encontraron registros'
            return render(request, 'Descuentos/BuscarDescuento.html', {'Descuentos': Descuentos, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_descuentos(),'reportes_usuarios': DatosReportes.cargar_usuario()})
    