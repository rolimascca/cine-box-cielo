import io
import qrcode
import base64
from .utils import enviar_comprobante  
from django.db import IntegrityError
from io import BytesIO
from reportlab.pdfgen import canvas

from django.urls import reverse


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.template.loader import render_to_string
from django.conf import settings
from .models import Pago
from xhtml2pdf import pisa
from .models import Reserva, Precio, Pago  
from decimal import Decimal, InvalidOperation
from datetime import datetime

def procesar_pago(request, reserva_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    reserva = get_object_or_404(Reserva, id=reserva_id)

    pago_existe = Pago.objects.filter(reserva=reserva).first()
    if pago_existe:
        messages.info(request, "Ya se ha reguistrado un pago para esta reserva")
        return redirect("pago_exitoso", pago_id=pago_existe.id)

    metodo_pago = request.POST.get('metodo_pago', 'tarjeta')
    monto = reserva.precio

    pago = Pago.objects.create(
        reserva=reserva,
        fecha_pago=datetime.now(),
        monto=monto,
        metodo_pago=metodo_pago,
        estado="Completado"
    )

    if enviar_comprobante(request, pago):
        messages.success(request, '¡pago realizado con exito, el corovante se envio a tu correo!')
    else:
        messages.success(request, "¡Pago realizado con éxito! sin envargo no se envao al correo")
    return redirect('pago_exitoso', pago_id=pago.id)


def pago_exitoso(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    return render(request, "cineBox/pago_exitoso.html", {'pago': pago})



@login_required
def pasarela_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    
    

    context = { 
        'reserva': reserva,
        'precio': float(reserva.precio)  
    }
    return render(request, 'cineBox/pasarela_pago.html', context)



def generar_qr_codigo(codigo_reserva):
    
    # Generar el código QR para la reserva
    qr = qrcode.make(codigo_reserva)
    qr_io = io.BytesIO()
    qr.save(qr_io, 'PNG')
    qr_io.seek(0)
    
    # Convertir el QR a un archivo de imagen
    qr_image = InMemoryUploadedFile(qr_io, None, 'codigo_qr.png', 'image/png', qr_io.tell(), None)
    return qr_image


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Pago
import qrcode
from PIL import Image
from io import BytesIO
from reportlab.lib.utils import ImageReader

def generar_comprobante_pdf(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    
    
    # Generar el código QR
    if request:
        codigo_url = request.build_absolute_uri(
        reverse('api_reserva_por_codigo', args=[str(pago.reserva.codigo_qr)])
    )
    else:
        base_url = settings.BASE_URL
        relative_url = reverse('api_reserva_por_codigo', args=[str(pago.reserva.codigo_qr)])
        codigo_url = f"{base_url}{relative_url}"

    
    qr = qrcode.make(codigo_url)
    
    # Convertir el QR a base64
    qr_io = BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_base64 = base64.b64encode(qr_io.getvalue()).decode('utf-8')
    # Renderizar la plantilla HTML
    context = {
        'pago': pago,
        'qr_base64': qr_base64,
        'logo_url': request.build_absolute_uri('/static/img/logo_cinebox.png'),
    }
    html = render_to_string('cineBox/comprobante_pago.html', context)
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="comprobante_pago_{pago.id}.pdf"'
    
    # Usar xhtml2pdf para convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

def enviar_comprobante(request, pago):
    # Generar el contenido del correo
    subject = 'Comprobante de Pago'
    message = f'Tu pago de {pago.monto} ha sido procesado exitosamente. Gracias por tu compra.'
    
    # Generar el PDF del comprobante
    pdf_response = generar_comprobante_pdf(request, pago.id)  # Llama a la función que genera el PDF
    pdf_content = pdf_response.content  # Obtén el contenido del PDF
    # Crear el correo electrónico
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pago.reserva.usuario.email],  # Asegúrate de que el usuario tenga un correo asociado
    )
    
    # Adjuntar el PDF al correo
    email.attach(f'comprobante_pago_{pago.id}.pdf', pdf_content, 'application/pdf')

    try:
        email.send(fail_silently=False)
        return True
    except Exeption as e:
        print(f'error al enviar al correo {str(e)}')
        return False
    # Enviar el correo
   

