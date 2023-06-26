from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes




url = 'https://clinicamr.onrender.com/api/'
def listar_Impuestos(request):
    response = requests.get(url+'Impuestos/')
    if response.status_code == 200:
        data = response.json()
        Impuestos = data['Impuestos']
    else:
        Impuestos = []
    context = {'Impuestos': Impuestos}
    return render(request, 'Impuestos/BuscarImpuesto.html', context)

def crear_Impuestos(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        valor = float(request.POST['valor'])
        registro_temp = {'nombre': nombre, 'valor': valor}
        response = requests.post(url+'Impuestos/', json={'nombre': nombre, 'valor': valor})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Impuestos/Impuesto.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'impuestos': registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'Impuestos/Impuesto.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'impuestos': registro_temp})
    else:
        return render(request, 'Impuestos/Impuesto.html',{'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
def abrir_actualizar_Impuestos(request):
    if request.method == 'POST':
         resp = requests.get(url+'Impuestos/busqueda/id/'+str(request.POST['id_Impuestos']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            Impuestos = data['Impuestos']
            mensaje = data['message']
         else:
            Impuestos = []
         context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Impuestos/ImpuestoActualizar.html', context)
    
def actualizar_Impuestos(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        valor = float(request.POST['valor'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'Impuestos/id/{idTemporal}', json={'nombre': nombre, 'valor': valor})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'Impuestos/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        Impuestos = data['Impuestos']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Impuestos/ImpuestoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'Impuestos':Impuestos })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Impuestos/ImpuestoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'Impuestos':Impuestos})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'Impuestos/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            Impuestos = data['Impuestos']
            mensaje = data['message']
            return render(request, 'Impuestos/ImpuestoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos})
        else:
            mensaje = data['message']
            return render(request, 'Impuestos/ImpuestoActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'Impuestos':Impuestos})

def eliminar_Impuestos(request, id):  
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'Impuestos/id/{idTemporal}')
            res = response.json()
            rsp_Impuestos = requests.get(url + 'Impuestos/') 
            context ={}
            if rsp_Impuestos.status_code == 200:
                data = rsp_Impuestos.json()
                Impuestos = data['Impuestos']
                context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos}
            else:
                Impuestos = []
                mensaje = res['message']
                context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje': mensaje}
            return render(request, 'Impuestos/BuscarImpuesto.html', context) 
    except:
        rsp_Impuestos = requests.get(url + 'Impuestos/') 
        context ={}
        if  rsp_Impuestos.status_code == 200:
            data = rsp_Impuestos.json()
            Impuestos = data['Impuestos']
            context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos}
        else:
            Impuestos = []
        mensaje = 'No se puede eliminar, esta siendo utilizando en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'error': mensaje}
        return render(request, 'Impuestos/BuscarImpuesto.html', context)
    
def buscar_Impuestos(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'Impuestos/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    Impuestos = {}
                    Impuestos = data['Impuestos']
                    context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje':mensaje}
                    return render(request, 'Impuestos/BuscarImpuesto.html', context)   
                else:
                    Impuestos = []
                    mensaje = 'No se encontraron registros'
                    return render(request, 'Impuestos/BuscarImpuesto.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje': mensaje})
            
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    Impuestos = {}
                    Impuestos = data['Impuestos']
                    context = {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje':mensaje}
                    return render(request, 'Impuestos/BuscarImpuesto.html', context)
                else:
                    Impuestos = []
                    mensaje = 'No se encontraron registros'
                    return render(request, 'Impuestos/BuscarImpuesto.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje': mensaje})
        else:
            response = requests.get(url+'Impuestos/')
            if response.status_code == 200:
                data = response.json()
                Impuestos = data['Impuestos']
                mensaje = data['message']   
                return render(request, 'Impuestos/BuscarImpuesto.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje': mensaje})
            else:
                Impuestos = []
                mensaje = 'No se encontraron registros'
            return render(request, 'Impuestos/BuscarImpuesto.html', {'reportes_lista':DatosReportes.cargar_lista_impuesto(),'reportes_usuarios':DatosReportes.cargar_usuario(),'Impuestos': Impuestos, 'mensaje': mensaje})
    