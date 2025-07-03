from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario,Sala, Horario, Pelicula, Precio, Reserva, Pago

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise forms.ValidationError("El correo no está registrado.")

        user = authenticate(request=self.request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Contraseña incorrecta.")

        self.cleaned_data['user'] = user
        return self.cleaned_data


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.Roles.CLIENTE
        if commit:
            user.save()
        return user

class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = '__all__'

class PrecioForm(forms.ModelForm):
    class Meta:
        model = Precio
        fields = '__all__'

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'