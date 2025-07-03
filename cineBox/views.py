import uuid
import io
import json
import qrcode

from datetime import datetime, timedelta
from django.utils import timezone

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from xhtml2pdf import pisa

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Sala, Precio, Reserva, Usuario, Horario, Pago
from .forms import RegistroUsuarioForm
from .utils import enviar_comprobante


def home(request):
    salas = Sala.objects.all()
    image_data = [{"url": sala.imagen.url, "slug": sala.slug} for sala in salas]
    return render(request, 'index.html', {"salas": salas, "image_urls": json.dumps(image_data)})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Sesión iniciada correctamente.')
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')

    return render(request, 'cineBox/login.html', {'next': request.GET.get('next', '')})


def logout_view(request):
    logout(request)
    return redirect('home')


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'cineBox/registrar.html', {'form': form})

def detalle_sala(request, slug):
    sala = get_object_or_404(Sala, slug=slug)

    # Determinar fecha_actual (GET o hoy)
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        try:
            fecha_actual = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            fecha_actual = timezone.now().date()
    else:
        fecha_actual = timezone.now().date()

    # Intentar cargar horarios para la fecha seleccionada
    horarios = list(
        Horario.objects
                .filter(sala=sala, fecha=fecha_actual)
                .order_by('hora')
    )

    # Si no hay horarios y la fecha seleccionada es futura, "heredamos" los de hoy
    hoy = timezone.now().date()
    if not horarios and fecha_actual > hoy:
        horarios = list(
            Horario.objects
                    .filter(sala=sala, fecha=hoy)
                    .order_by('hora')
        )

    precio = Precio.objects.filter(sala=sala).first()

    # Sólo 3 días: Hoy, Mañana, Pasado mañana
    labels = ["Hoy", "Mañana", "Pasado mañana"]
    dias = []
    for i, label in enumerate(labels):
        dia_obj = hoy + timedelta(days=i)
        dias.append({
            'fecha_obj': dia_obj,
            'fecha_str': dia_obj.strftime("%Y-%m-%d"),
            'titulo':    label,
        })

    return render(request, 'cineBox/detalle_sala.html', {
        'sala':         sala,
        'horarios':     horarios,
        'precio':       precio,
        'fecha_actual': fecha_actual,
        'dias':         dias,
    })
def lista_salas(request):
    # Obtener todas las salas con sus películas relacionadas
    salas = Sala.objects.prefetch_related('peliculas').all()
    
    return render(request, 'cineBox/lista_salas.html', {
        'salas': salas,
        'titulo': 'Nuestras Salas'
    })



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Sala, Horario, Reserva, Precio

@login_required(login_url='login')
def reservar_sala(request, slug):
    sala = get_object_or_404(Sala, slug=slug)
    
    if request.method == 'POST':
        horario_id = request.POST.get('horario_id')
        
        if not horario_id:
            messages.error(request, "Debes seleccionar un horario válido.")
            return redirect('detalle_sala', slug=slug)
        
        try:
            horario = Horario.objects.get(id=horario_id, sala=sala)
        except Horario.DoesNotExist:
            messages.error(request, "El horario seleccionado no existe.")
            return redirect('detalle_sala', slug=slug)
        
        # Verificar disponibilidad
        if not horario.disponible:
            messages.error(request, "Este horario ya no está disponible.")
            return redirect('detalle_sala', slug=slug)
        
        # Verificar reserva existente
        if Reserva.objects.filter(usuario=request.user, horario=horario).exists():
            messages.warning(request, "Ya tienes una reserva para este horario.")
            return redirect('mis_reservas')
        
        # Obtener precio (usando el más reciente)
        precio = Precio.objects.filter(sala=sala).order_by('-id').first()
        if not precio:
            messages.error(request, "No se encontró información de precios para esta sala.")
            return redirect('detalle_sala', slug=slug)
        
        # Crear reserva
        try:
            horario.disponible = False
            horario.save()
            
            reserva = Reserva.objects.create(
                sala=sala,
                usuario=request.user,
                horario=horario,
                precio=precio.precio
            )
            
            messages.success(request, f"¡Reserva exitosa para {horario.hora}!")
            return redirect('pasarela_pago', reserva_id=reserva.id)
            
        except Exception as e:
            messages.error(request, f"Error al crear la reserva: {str(e)}")
            return redirect('detalle_sala', slug=slug)
    
    # Si no es POST, redirigir a detalle
    return redirect('detalle_sala', slug=slug)

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('sala')
    return render(request, 'cineBox/mis_reservas.html', {'reservas': reservas})


def confirmacion_reserva_ex(request, slug, horario):
    sala = get_object_or_404(Sala, slug=slug)
    horarios = Horario.objects.filter(sala=sala)
    return render(request, 'cineBox/confirmacion_reserva.html', {
        'sala': sala,
        'horario': horario,
        'horarios': horarios
    })  


def verificar_horario(request):
    if request.method == "POST":
        data = json.loads(request.body)
        hora = data.get('horario')
        sala_slug = data.get('sala_slug')

        ocupado = Horario.objects.filter(sala__slug=sala_slug, hora=hora, disponible=False).exists()
        return JsonResponse({'ocupado': ocupado})


def horarios_por_fecha(request):
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha = None
    else:
        fecha = None

    if fecha:
        horarios = Horario.objects.filter(fecha=fecha, disponible=True).select_related('sala')
    else:
        horarios = Horario.objects.filter(disponible=True).select_related('sala')

    context = {
        'horarios': horarios,
        'fecha': fecha_str,
    }
    return render(request, 'horarios_por_fecha.html', context) 
