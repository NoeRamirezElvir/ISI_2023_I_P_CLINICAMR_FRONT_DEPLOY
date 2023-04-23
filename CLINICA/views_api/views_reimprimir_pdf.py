from decimal import Decimal
from django.http import HttpResponse
import json
from django.shortcuts import redirect, render
from django.urls import reverse
import requests

from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


url = 'http://localhost:8080/api/'
def reimprimir_recaudo(request,id):
    if request.method == 'POST':
        rsp = requests.get(url + f'recaudo/busqueda/id/{id}')
        data = rsp.json()
        print('data')

        context = {}
        pdf = render_to_pdf('recaudo/recaudo_pdf.html', context)
        response_pdf = HttpResponse(pdf, content_type='application/pdf')
        response_pdf['Content-Disposition'] = 'attachment; filename="recaudo.pdf"'
        return response_pdf
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None