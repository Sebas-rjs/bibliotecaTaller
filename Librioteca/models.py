from django.db import models
from django.contrib.auth.models import User  # Usamos el modelo User de Django

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    cantidad_disponible = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionado con el modelo User
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"Prestamo de '{self.libro}' a {self.usuario.username}"


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el modelo User
    rut = models.CharField(max_length=12, unique=True)  # RUT del usuario
    telefono = models.CharField(max_length=15)  # Teléfono del usuario
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección opcional
    correo = models.EmailField(unique=True)  # Correo electrónico único del usuario

    def __str__(self):
        return f'{self.user.username} - {self.rut}'