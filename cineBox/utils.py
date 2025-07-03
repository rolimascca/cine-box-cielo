

from email.message import EmailMessage
from flask import get_template_attribute
import io
from xhtml2pdf import pisa

def enviar_comprobante(pago):
    # Crear el PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    p.drawString(100, 800, "Comprobante de Pago - CineBox")
    p.line(100, 795, 400, 795)
    p.drawString(100, 770, f"ID del pago: {pago.id}")
    p.drawString(100, 750, f"Sala: {pago.reserva.sala.nombre}")
    p.drawString(100, 730, f"Horario: {pago.reserva.horario.hora}")
    p.drawString(100, 710, f"Fecha de pago: {pago.fecha_pago.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 690, f"Monto: S/ {pago.monto}")
    p.drawString(100, 670, f"Método de pago: {pago.metodo_pago}")
    p.drawString(100, 650, f"Estado: {pago.estado}")

    # Generar QR
    qr_img = qrcode.make(str(pago.reserva.codigo_qr))
    qr_pil = qr_img.get_image()
    p.drawInlineImage(qr_pil, 400, 680, width=120, height=120)

    p.showPage()
    p.save()
    buffer.seek(0)

    html_body = render_to_string("cineBox/correo_comprobante.html", {'pago': pago})

    email = EmailMessage(
        subject='🎟️ Comprobante de tu pago - CineBox',
        body=html_body,
        from_email=None,
        to=[pago.reserva.usuario.email],
    )
    email.content_subtype = "html"
    email.attach(f'comprobante_pago_{pago.id}.pdf', buffer.read(), 'application/pdf')
    email.send()