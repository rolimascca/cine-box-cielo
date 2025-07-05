from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Sala, Precio, Usuario, Reserva, Pelicula, Horario, Pago
from .forms import RegistroUsuarioForm, CustomUsuarioChangeForm
from cloudinary.forms import CloudinaryFileField


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "capacidad", "imagen_preview")
    prepopulated_fields = {"slug": ("nombre",)}
    readonly_fields = ("imagen_preview",)
    
    # Sobrescribe el formfield para imágenes
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'imagen':
            return CloudinaryFileField()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def imagen_preview(self, obj):
        if obj.imagen_url:  # Usamos la propiedad que creaste
            return mark_safe(
                f'<img src="{obj.imagen_url}" style="max-height: 200px; border-radius: 5px;" />'
            )
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"

    def save_model(self, request, obj, form, change):
        """Valida que no se modifiquen salas con reservas existentes"""
        if change and Reserva.objects.filter(sala=obj).exists():
            raise ValidationError(
                "No puedes modificar una sala con reservas activas. "
                "Crea una nueva sala en su lugar."
            )
        
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """Bloquea edición de slug si hay reservas"""
        if obj and Reserva.objects.filter(sala=obj).exists():
            return ("slug",) + self.readonly_fields
        return self.readonly_fields


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ("sala", "precio")


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    form = CustomUsuarioChangeForm
    add_form = RegistroUsuarioForm
    list_display = ('email', 'is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ("Permisos", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Fechas", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error al guardar el usuario: {str(e)}")

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'sala')
    list_filter = ['sala']


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display  = ('sala', 'fecha', 'hora', 'disponible')
    list_filter   = ('sala', 'disponible', 'fecha')
    search_fields = ('sala__nombre', 'hora')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'usuario', 'horario', 'usada', 'fecha_reserva')
    list_filter = ('sala', 'usada', 'fecha_reserva')
    search_fields = ('usuario__email', 'horario')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'monto', 'metodo_pago', 'estado', 'fecha_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha_pago')
    search_fields = ('reserva__usuario__email', 'transaccion_id')


