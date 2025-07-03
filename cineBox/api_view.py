from django.http import JsonResponse
from .models import Reserva


def api_reserva_por_codigo(request, codigo):
    try:
        reserva = Reserva.objects.get(codigo_qr=codigo)
        data = {
            'id': reserva.id,
            'sala': reserva.sala.nombre,
            'horario': reserva.horario.hora.strftime('%Y-%m-%d %H:%M'),
            'usuario': reserva.usuario.username,
            'codigo_qr': reserva.codigo_qr,
        }
        return JsonResponse(data)
    except Reserva.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada'}, status=404)

def verificar_reserva_qr(request, codigo_qr):
    try:
        # Buscar reserva por código QR (UUID)
        reserva = Reserva.objects.get(codigo_qr=codigo_qr)
        
        # Validar si la reserva ya fue usada
        if reserva.usada:
            return JsonResponse({
                "status": "error",
                "mensaje": "Esta reserva ya fue utilizada."
            }, status=400)
            
        # Retornar datos de la reserva
        return JsonResponse({
            "status": "success",
            "reserva": {
                "usuario": reserva.usuario.email,
                "sala": reserva.sala.nombre,
                "horario": reserva.horario.hora,
                "precio": str(reserva.precio),
                "fecha_reserva": reserva.fecha_reserva.strftime("%Y-%m-%d %H:%M"),
                "codigo_qr": str(reserva.codigo_qr)
            }
        })
        
    except Reserva.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "mensaje": "Código QR no válido."
        }, status=404)