
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .managers import UsuarioManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from decimal import Decimal
from datetime import timedelta
from cloudinary.models import CloudinaryField

class Sala(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField()
    imagen = CloudinaryField(
    'image',
    folder='salas',        # Carpeta en Cloudinary
    overwrite=True,
    resource_type='image',
    format='jpg',
    transformation={'quality': 'auto:eco'}
    )
    capacidad = models.IntegerField()

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        permissions = [
            ("ver_sala", "Puede ver las salas"),
            ("crear_sala", "Puede crear salas"),
            ("editar_sala", "Puede editar salas"),
            ("eliminar_sala", "Puede eliminar salas"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1

            while Sala.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}" 
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    @property
    def imagen_url(self):
        """Devuelve la URL completa de la imagen en Cloudinary"""
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        return None

class Horario(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='horarios')
    fecha = models.DateField()
    hora = models.TimeField()

    disponible = models.BooleanField(default=True)
    class Meta:
        permissions = [
            ("ver_horario", "Puede ver los horarios"),
            ("crear_horario", "Puede crear horarios"),
            ("editar_horario", "Puede editar horarios"),
            ("eliminar_horario", "Puede eliminar horarios"),
        ]
    

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.sala.nombre}"

class Precio(models.Model):
    sala = models.ForeignKey(Sala, related_name='precios', on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sala.nombre} - {self.precio}"
    
class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)
    usada = models.BooleanField(default=False)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    codigo_qr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) 
    
    def __str__(self):
        return f"Reserva de {self.usuario} para {self.sala.nombre} a las {self.horario}"

    class Meta:
        unique_together = ('usuario', 'sala', 'horario')

    
# Manager personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Usuario.Roles.ADMIN)
        return self.create_user(email, password, **extra_fields)

# Modelo personalizado de usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necesario para acceso al panel admin
    
    date_joined = models.DateTimeField(default=timezone.now)

    # Roles
    class Roles(models.TextChoices):
        CLIENTE = 'cliente', _('Cliente')
        ADMIN = 'admin', _('Administrador')
        GERENTE = 'gerente', _('Gerente')   

    rol = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.CLIENTE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    class Meta:
        permissions = [
            ("ver_usuario", "Puede ver usuarios"),
            ("crear_usuario", "Puede crear usuarios"),
            ("editar_usuario", "Puede editar usuarios"),
            ("eliminar_usuario", "Puede eliminar usuarios"),
        ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Si el usuario es admin, se le da acceso al panel de administración
        self.is_staff = self.rol == self.Roles.ADMIN
        super().save(*args, **kwargs)
    
class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = CloudinaryField('image', folder='peliculas', blank=True, null=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='peliculas')

    def __str__(self):
        return self.titulo

#modelo pago 
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=[('tarjeta', 'Tarjeta'), ('paypal', 'PayPal'), ('efectivo', 'Efectivo')])
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado'), ('fallido', 'Fallido')], default='pendiente')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    transaccion_id = models.CharField(max_length=100, blank=True, null=True)  # Por si se simula algo como Visa o Yape

    def __str__(self):
        return f"Pago de {self.reserva.usuario.email} - {self.estado}"

class PasswordResetToken(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    def es_valido(self):
        return not self.usado and (self.creado_en + timedelta(hours=1)) > timezone.now()


    def __str__(self):
        return f"Token para {self.usuario.email}"