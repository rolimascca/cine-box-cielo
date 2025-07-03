from django.contrib.auth.hashers import make_password
from cineBox.models import Usuario

# Encripta las contraseñas de los usuarios
usuarios = Usuario.objects.all()
for user in usuarios:
    if not user.password.startswith('pbkdf2_sha256$'):  # Verifica si ya está encriptada
        user.password = make_password(user.password)  # Encripta la contraseña
        user.save()
