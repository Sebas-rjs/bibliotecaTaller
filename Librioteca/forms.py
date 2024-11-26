from django import forms
from django.contrib.auth.models import User  # Esto es si usas el modelo User por defecto
from .models import Libro, Prestamo, Usuario

# Formulario para agregar o editar libros
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn', 'cantidad_disponible']

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario', 'fecha_devolucion']
        widgets = {
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),  # Widget para la fecha
        }

# Formulario para registrar o editar usuarios (Django User model o un modelo personalizado)
class UsuarioForm(forms.ModelForm):
    # Añadimos los campos del modelo User
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Contraseña")

    class Meta:
        model = Usuario  # Usamos el modelo Usuario personalizado
        fields = ['user', 'rut', 'telefono', 'direccion', 'correo']  # Campos del modelo Usuario
        widgets = {
            'correo': forms.EmailInput(attrs={'type': 'email'}),  # Widget para correo electrónico
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el formulario es para editar, no pedimos la contraseña
        if self.instance.pk:
            self.fields['password'].required = False

    def save(self, commit=True):
        # Guardamos el objeto Usuario y el User asociado
        usuario = super().save(commit=False)
        
        # Si se ha proporcionado una nueva contraseña, la asignamos al usuario
        if self.cleaned_data['password']:
            user = self.cleaned_data['user']
            user.set_password(self.cleaned_data['password'])
            user.save()

        if commit:
            usuario.save()  # Guardamos el usuario
        return usuario

    # Aseguramos que el campo 'user' sea un campo de selección de usuarios existentes
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Seleccionar Usuario")