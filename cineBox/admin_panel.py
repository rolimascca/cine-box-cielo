from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Sala, Horario, Pelicula, Precio, Reserva, Pago, Usuario
from .forms import SalaForm, HorarioForm, PeliculaForm, PrecioForm, ReservaForm, PagoForm, CustomUsuarioChangeForm, RegistroUsuarioForm

def admin_required(user):
    return user.is_authenticated and user.is_staff


@login_required
@permission_required('cineBox.ver_sala', raise_exception=True)
def sala_list(request):
    salas = Sala.objects.all()
    return render(request, 'panel_admin/sala_list.html', {'salas': salas})
# ---- PANEL ADMIN ----
@login_required
@user_passes_test(admin_required)
def admin_panel(request):
    context = {
        'salas': Sala.objects.all(),
        'horarios': Horario.objects.all(),
        'peliculas': Pelicula.objects.all(),
        'precios': Precio.objects.all(),
        'reservas': Reserva.objects.all(),
        'pagos': Pago.objects.all(),
        'usuarios': Usuario.objects.all(),
    }
    return render(request, 'cineBox/admin_panel.html', context)

# ---- SALA ----
@login_required
@permission_required('cineBox.add_sala', raise_exception=True)
def sala_add(request):
    if request.method == 'POST':
        form = SalaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = SalaForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Sala'})

@login_required
@permission_required('cineBox.change_sala', raise_exception=True)
def sala_edit(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        form = SalaForm(request.POST, request.FILES, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Sala'})

@login_required
@permission_required('cineBox.delete_sala', raise_exception=True)
def sala_delete(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        sala.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': sala, 'titulo': 'Eliminar Sala'})

# ---- HORARIO ----
@login_required
@permission_required('cineBox.add_horario', raise_exception=True)
def horario_add(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = HorarioForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Horario'})

@login_required
@permission_required('cineBox.change_horario', raise_exception=True)
def horario_edit(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Horario'})

@login_required
@permission_required('cineBox.delete_horario', raise_exception=True)
def horario_delete(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        horario.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': horario, 'titulo': 'Eliminar Horario'})

# ---- PELICULA ----
@login_required
@permission_required('cineBox.add_pelicula', raise_exception=True)
def pelicula_add(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PeliculaForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Película'})

@login_required
@permission_required('cineBox.change_pelicula', raise_exception=True)
def pelicula_edit(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Película'})

@login_required
@permission_required('cineBox.delete_pelicula', raise_exception=True)
def pelicula_delete(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        pelicula.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': pelicula, 'titulo': 'Eliminar Película'})

# ---- PRECIO ----
@login_required
@permission_required('cineBox.add_precio', raise_exception=True)
def precio_add(request):
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PrecioForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Precio'})

@login_required
@permission_required('cineBox.change_precio', raise_exception=True)
def precio_edit(request, pk):
    precio = get_object_or_404(Precio, pk=pk)
    if request.method == 'POST':
        form = PrecioForm(request.POST, instance=precio)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PrecioForm(instance=precio)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Precio'})

@login_required
@permission_required('cineBox.delete_precio', raise_exception=True)
def precio_delete(request, pk):
    precio = get_object_or_404(Precio, pk=pk)
    if request.method == 'POST':
        precio.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': precio, 'titulo': 'Eliminar Precio'})

# ---- RESERVA ----
@login_required
@permission_required('cineBox.add_reserva', raise_exception=True)
def reserva_add(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ReservaForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Reserva'})

@login_required
@permission_required('cineBox.change_reserva', raise_exception=True)
def reserva_edit(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Reserva'})

@login_required
@permission_required('cineBox.delete_reserva', raise_exception=True)
def reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': reserva, 'titulo': 'Eliminar Reserva'})

# ---- PAGO ----
@login_required
@permission_required('cineBox.add_pago', raise_exception=True)
def pago_add(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PagoForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Pago'})

@login_required
@permission_required('cineBox.change_pago', raise_exception=True)
def pago_edit(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Pago'})

@login_required
@permission_required('cineBox.delete_pago', raise_exception=True)
def pago_delete(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        pago.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': pago, 'titulo': 'Eliminar Pago'})

# ---- USUARIO ----
@login_required
@permission_required('cineBox.add_usuario', raise_exception=True)
def usuario_add(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Añadir Usuario'})

@login_required
@permission_required('cineBox.change_usuario', raise_exception=True)
def usuario_edit(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = CustomUsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = CustomUsuarioChangeForm(instance=usuario)
    return render(request, 'panel_admin/form.html', {'form': form, 'titulo': 'Editar Usuario'})

@login_required
@permission_required('cineBox.delete_usuario', raise_exception=True)
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('admin_panel')
    return render(request, 'panel_admin/confirm_delete.html', {'obj': usuario, 'titulo': 'Eliminar Usuario'})

##################################### reportes.py #####################################

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .reportes import obtener_datos_reporte_ventas, generar_excel_reporte_ventas

@login_required
@permission_required('cineBox.view_pago', raise_exception=True)
def reporte_ventas(request):
    datos = obtener_datos_reporte_ventas()
    return render(request, 'panel_admin/reporte_ventas.html', datos)


@login_required
@permission_required('cineBox.view_pago', raise_exception=True)
def exportar_reporte_excel(request):
    return generar_excel_reporte_ventas()