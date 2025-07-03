from .models import Reserva
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 


@login_required
def mi_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user': request.user,
        'reservas_recientes': Reserva.objects.filter(usuario=request.user).order_by('-fecha_reserva')[:3],
    }
    return render(request, 'cineBox/mi_perfil.html', context)