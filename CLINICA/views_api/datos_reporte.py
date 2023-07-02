import requests

from ..views_api.logger import definir_log_info


url = 'https://clinicamr.onrender.com/api/'
class DatosReportes():

    def cargar_usuario():
        response = requests.get(url+'usuarios/busqueda/sesion/1')
        if response.status_code == 200:
            data = response.json()
            usuario = data['usuariosr']
            nombre = usuario[0]['nombreUsuario']
        else:
            nombre  = ''
        return nombre
    
    def cargar_lista_autorizacion():
        response = requests.get(url+'autorizar/')
        if response.status_code == 200:
            data = response.json()
            lista = data['autorizar']
        else:
            lista  = []
        return lista
    
    def cargar_lista_cargos():
        try:
            response = requests.get(url+'cargos/')
            if response.status_code == 200:
                data = response.json()
                lista = data['cargos']
                if data['message'] != "Consulta exitosa":
                    logger = definir_log_info('cargos_pdf','logs_cargo')
                    logger.debug("No se obtuvieron cargos")
                else:
                    logger = definir_log_info('cargos_pdf','logs_cargo')
                    logger.debug("Se obtuvo la informacion correspondiente a cargos")
            else:
                lista  = []
            return lista
        except Exception as e:
            logger = definir_log_info('cargos_pdf_excepcion','logs_cargo')
            logger.exception(f"Se produjo una excepcion: {str(e)}")
            lista  = []
            return lista

    
    def cargar_lista_citas():
        response = requests.get(url+'citas/')
        if response.status_code == 200:
            data = response.json()
            lista = data['citas']
        else:
            lista  = []
        return lista
    
    def cargar_lista_pacientes():
        response = requests.get(url+'pacientes/')
        if response.status_code == 200:
            data = response.json()
            lista = data['pacientes']
        else:
            lista  = []
        return lista
    
    def cargar_lista_consultas():
        response = requests.get(url+'consultas/')
        if response.status_code == 200:
            data = response.json()
            lista = data['consultas']
        else:
            lista  = []
        return lista
    
    def cargar_lista_sar():
        response = requests.get(url+'correlativo/')
        if response.status_code == 200:
            data = response.json()
            lista = data['correlativo']
        else:
            lista  = []
        return lista
    
    def cargar_lista_costo_historico_medicamento():
        response = requests.get(url+'costoHistoricoMedicamento/')
        if response.status_code == 200:
            data = response.json()
            lista = data['historicos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_descuentos():
        response = requests.get(url+'Descuentos/')
        if response.status_code == 200:
            data = response.json()
            lista = data['Descuentos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_detalle_consulta():
        response = requests.get(url+'consultaDetalle/')
        if response.status_code == 200:
            data = response.json()
            lista = data['detalles']
        else:
            lista  = []
        return lista

    def cargar_lista_diagnostico():
        response = requests.get(url+'diagnostico/')
        if response.status_code == 200:
            data = response.json()
            lista = data['diagnosticos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_detalle_diagnostico():
        response = requests.get(url+'diagnosticoDetalle/')
        if response.status_code == 200:
            data = response.json()
            lista = data['detalles']
        else:
            lista  = []
        return lista
    
    def cargar_lista_documentos():
        response = requests.get(url+'documentos/')
        if response.status_code == 200:
            data = response.json()
            lista = data['documentos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_empleados():
        response = requests.get(url+'empleados/')
        if response.status_code == 200:
            data = response.json()
            lista = data['empleados']
        else:
            lista  = []
        return lista
    
    def cargar_lista_enfermedades():
        response = requests.get(url+'enfermedades/')
        if response.status_code == 200:
            data = response.json()
            lista = data['enfermedades']
        else:
            lista  = []
        return lista
    
    def cargar_lista_detalle_enfermedad():
        response = requests.get(url+'enfermedadDetalle/')
        if response.status_code == 200:
            data = response.json()
            lista = data['detalles']
        else:
            lista  = []
        return lista
    
    def cargar_lista_especialidades():
        response = requests.get(url+'especialidad/')
        if response.status_code == 200:
            data = response.json()
            lista = data['especialidad']
        else:
            lista  = []
        return lista
    
    def cargar_lista_examen():
        response = requests.get(url+'examen/')
        if response.status_code == 200:
            data = response.json()
            lista = data['examenes']
        else:
            lista  = []
        return lista
    
    def cargar_lista_expediente():
        response = requests.get(url+'expediente/')
        if response.status_code == 200:
            data = response.json()
            lista = data['expedientes']
        else:
            lista  = []
        return lista
    
    def cargar_lista_historico_impuesto():
        response = requests.get(url+'impuestoHistorico/')
        if response.status_code == 200:
            data = response.json()
            lista = data['historicos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_impuesto():
        response = requests.get(url+'Impuestos/')
        if response.status_code == 200:
            data = response.json()
            lista = data['Impuestos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_laboratorios():
        response = requests.get(url+'laboratorios/')
        if response.status_code == 200:
            data = response.json()
            lista = data['laboratorios']
        else:
            lista  = []
        return lista
    
    def cargar_lista_medicamentos():
        response = requests.get(url+'medicamentos/')
        if response.status_code == 200:
            data = response.json()
            lista = data['medicamentos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_metodo_pago():
        response = requests.get(url+'metodop/')
        if response.status_code == 200:
            data = response.json()
            lista = data['metodop']
        else:
            lista  = []
        return lista
    
    def cargar_lista_muestras():
        response = requests.get(url+'muestras/')
        if response.status_code == 200:
            data = response.json()
            lista = data['muestras']
        else:
            lista  = []
        return lista
    
    def cargar_lista_parametros_generales():
        response = requests.get(url+'parametrosgenerales/')
        if response.status_code == 200:
            data = response.json()
            lista = data['parametrosgenerales']
        else:
            lista  = []
        return lista
    
    def cargar_lista_historico_precio_examen():
        response = requests.get(url+'precioHistoricoExamen/')
        if response.status_code == 200:
            data = response.json()
            lista = data['historicos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_historico_precio_tratamiento():
        response = requests.get(url+'precioHistoricoTratamiento/')
        if response.status_code == 200:
            data = response.json()
            lista = data['historicos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_historico_precio_consulta():
        response = requests.get(url+'precioHistoricoConsulta/')
        if response.status_code == 200:
            data = response.json()
            lista = data['historicos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_precio_historico_medicamento():
        response = requests.get(url+'precioHistoricoMedicamento/')
        if response.status_code == 200:
            data = response.json()
            lista = data['historicos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_detalle_recaudo_examen():
        response = requests.get(url+'recaudoDetalleExamen/')
        if response.status_code == 200:
            data = response.json()
            lista = data['detalles']
        else:
            lista  = []
        return lista
    
    def cargar_lista_detalle_recaudo_medicamento():
        response = requests.get(url+'recaudoDetalleMedicamento/')
        if response.status_code == 200:
            data = response.json()
            lista = data['detalles']
        else:
            lista  = []
        return lista
    
    def cargar_lista_detalle_recaudo_tratamiento():
        response = requests.get(url+'recaudoDetalleTratamiento/')
        if response.status_code == 200:
            data = response.json()
            lista = data['detalles']
        else:
            lista  = []
        return lista
    
    def cargar_lista_proveedores():
        response = requests.get(url+'proveedores/')
        if response.status_code == 200:
            data = response.json()
            lista = data['proveedores']
        else:
            lista  = []
        return lista
    
    def cargar_lista_recaudo():
        response = requests.get(url+'recaudo/')
        if response.status_code == 200:
            data = response.json()
            lista = data['recaudo']
        else:
            lista  = []
        return lista
    
    def cargar_lista_resultado():
        response = requests.get(url+'resultados/')
        if response.status_code == 200:
            data = response.json()
            lista = data['resultados']
        else:
            lista  = []
        return lista
    
    def cargar_lista_sintoma():
        response = requests.get(url+'sintomas/')
        if response.status_code == 200:
            data = response.json()
            lista = data['sintomas']
        else:
            lista  = []
        return lista
    
    def cargar_lista_subtipo():
        response = requests.get(url+'subtipo/')
        if response.status_code == 200:
            data = response.json()
            lista = data['subtipo']
        else:
            lista  = []
        return lista
    
    def cargar_lista_tipo():
        response = requests.get(url+'tipo/')
        if response.status_code == 200:
            data = response.json()
            lista = data['tipos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_tipo_muestra():
        response = requests.get(url+'tmuestra/')
        if response.status_code == 200:
            data = response.json()
            lista = data['tmuestra']
        else:
            lista  = []
        return lista
    
    def cargar_lista_traslados():
        response = requests.get(url+'traslados/')
        if response.status_code == 200:
            data = response.json()
            lista = data['traslados']
        else:
            lista  = []
        return lista
    
    def cargar_lista_tratamiento():
        response = requests.get(url+'tratamientos/')
        if response.status_code == 200:
            data = response.json()
            lista = data['tratamientos']
        else:
            lista  = []
        return lista
    
    def cargar_lista_usuarios():
        response = requests.get(url+'usuarios/')
        if response.status_code == 200:
            data = response.json()
            lista = data['usuariosr']
        else:
            lista  = []
        return lista