from django.urls import reverse  

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import PasswordResetToken
from django.utils import timezone  
import uuid


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            usuario = User.objects.get(email=email)
            token, created = PasswordResetToken.objects.get_or_create(
                usuario=usuario,
                defaults={'token': uuid.uuid4()}
            )
            if not created:
                token.token = uuid.uuid4()
                token.usado = False
                token.creado_en = timezone.now()
                token.save()

            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[token.token])
            )
            
            send_mail(
                'Recuperación de contraseña',
                f'Usa este enlace para resetear tu contraseña: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [usuario.email],
                fail_silently=False,
            )
            messages.success(request, '¡Correo enviado! Revisa tu bandeja de entrada.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese email.')
        


    return render(request, 'cineBox/password_reset_request.html')  


def password_reset_confirm(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
        print("Token recibido en vista:", token, type(token))

        if token_obj.usado:
            messages.error(request, 'Este enlace ya fue usado.')
            return redirect('password_reset')

        if not token_obj.es_valido():
            messages.error(request, 'El enlace ha expirado o es inválido.')
            return redirect('password_reset')

        if request.method == 'POST':
            nueva_contraseña = request.POST.get('nueva_contraseña')
            confirmar_contraseña = request.POST.get('confirmar_contraseña')

            if nueva_contraseña == confirmar_contraseña:
                usuario = token_obj.usuario
                usuario.set_password(nueva_contraseña)
                usuario.save()

                token_obj.usado = True
                token_obj.save()

                messages.success(request, '¡Contraseña actualizada! Ahora puedes iniciar sesión.')
                return redirect('login')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')

        return render(request, 'cineBox/password_reset_confirm.html')

    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Token inválido.')
        return redirect('password_reset')
