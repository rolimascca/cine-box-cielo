
from . import admin_panel 
from django.conf.urls.static import static 
from django.conf import settings
from django.urls import path, reverse
from .views import home, login_view, detalle_sala, reservar_sala, registro_usuario, confirmacion_reserva_ex, logout_view, mis_reservas, verificar_horario,  lista_salas, horarios_por_fecha

from .pagos_view import procesar_pago, pasarela_pago, pago_exitoso, generar_comprobante_pdf
from django.contrib.auth import views as auth_views

from debug_toolbar.toolbar import debug_toolbar_urls

from .api_view import api_reserva_por_codigo, verificar_reserva_qr

from .contraseña_view import password_reset_request, password_reset_confirm
from .perfil_view import mi_perfil

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login' ), 
    path('salas/', lista_salas, name='lista_salas'),
    path("salas/<slug:slug>/", detalle_sala, name="detalle_sala"),
    path('salas/<slug:slug>/reservar/', reservar_sala, name='reservar_sala'),
    path('registrar/', registro_usuario, name='registro_usuario'),
    path('reserva-exitosa/<slug:slug>/<str:horario>/', confirmacion_reserva_ex, name='reserva_exitosa'),
    path('mis-reservas/', mis_reservas, name='mis_reservas'),
    path('verificar_horario/', verificar_horario, name='verificar_horario'),
    path('logout/', logout_view, name='logout'),
    # Rutas de administración
    path('admin_panel/', admin_panel.admin_panel, name='admin_panel'),

    # Salas
    path('admin_panel/sala/add/', admin_panel.sala_add, name='sala_add'),
    path('admin_panel/sala/<int:pk>/edit/', admin_panel.sala_edit, name='sala_edit'),
    path('admin_panel/sala/<int:pk>/delete/', admin_panel.sala_delete, name='sala_delete'),

    # Horarios
    path('admin_panel/horario/add/', admin_panel.horario_add, name='horario_add'),
    path('admin_panel/horario/<int:pk>/edit/', admin_panel.horario_edit, name='horario_edit'),
    path('admin_panel/horario/<int:pk>/delete/', admin_panel.horario_delete, name='horario_delete'),

    # Películas
    path('admin_panel/pelicula/add/', admin_panel.pelicula_add, name='pelicula_add'),
    path('admin_panel/pelicula/<int:pk>/edit/', admin_panel.pelicula_edit, name='pelicula_edit'),
    path('admin_panel/pelicula/<int:pk>/delete/', admin_panel.pelicula_delete, name='pelicula_delete'),

    # Precios
    path('admin_panel/precio/add/', admin_panel.precio_add, name='precio_add'),
    path('admin_panel/precio/<int:pk>/edit/', admin_panel.precio_edit, name='precio_edit'),
    path('admin_panel/precio/<int:pk>/delete/', admin_panel.precio_delete, name='precio_delete'),

    # Reservas
    path('admin_panel/reserva/add/', admin_panel.reserva_add, name='reserva_add'),
    path('admin_panel/reserva/<int:pk>/edit/', admin_panel.reserva_edit, name='reserva_edit'),
    path('admin_panel/reserva/<int:pk>/delete/', admin_panel.reserva_delete, name='reserva_delete'),

    # Pagos
    path('admin_panel/pago/add/', admin_panel.pago_add, name='pago_add'),
    path('admin_panel/pago/<int:pk>/edit/', admin_panel.pago_edit, name='pago_edit'),
    path('admin_panel/pago/<int:pk>/delete/', admin_panel.pago_delete, name='pago_delete'),

    # Usuarios
    path('admin_panel/usuario/add/', admin_panel.usuario_add, name='usuario_add'),
    path('admin_panel/usuario/<int:pk>/edit/', admin_panel.usuario_edit, name='usuario_edit'),
    path('admin_panel/usuario/<int:pk>/delete/', admin_panel.usuario_delete, name='usuario_delete'),

    #reporte ventas
 

    path('reporte/', admin_panel.reporte_ventas, name='reporte_ventas'),
    path('reporte/excel/', admin_panel.exportar_reporte_excel, name='exportar_reporte_excel'),
    

    path('procesar-pago/<int:reserva_id>/', procesar_pago, name='procesar_pago'),

    path('pagar/<int:reserva_id>/', pasarela_pago, name='pasarela_pago'),
    path('pago_exitoso/<int:pago_id>', pago_exitoso, name='pago_exitoso'),
    #Generar pdf 
    path('generar-pdf/<int:pago_id>/', generar_comprobante_pdf, name='generar_comprobante_pdf'),
    #verificar reserva( APP )
    path('api/verificar/<str:codigo_qr>/', verificar_reserva_qr, name='verificar_reserva_qr'),
    #para recuperar contraseña
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/<uuid:token>/', password_reset_confirm, name='password_reset_confirm'),
    #Mi perfil
    path('mi-perfil/', mi_perfil, name='mi_perfil'),
    #reserva por qr cuando se genera el pdf
    path('api/reserva/<str:codigo>/', api_reserva_por_codigo, name='api_reserva_por_codigo'),

    path('horarios/', horarios_por_fecha, name='horarios_por_fecha'),



]    

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   