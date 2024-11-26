from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Libro, Prestamo, Usuario
from .forms import LibroForm, PrestamoForm, UsuarioForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required




@login_required
def inicio(request):
    # Obtén los préstamos activos (no devueltos)
    prestamos_activos = Prestamo.objects.filter(devuelto=False).select_related('libro', 'usuario')
    
    # Renderiza la plantilla con los préstamos activos
    return render(request, 'biblioteca/inicio.html', {'prestamos': prestamos_activos})

# Vista para listar libros
def lista_libros(request):
    query = request.GET.get('q', '')  # Si no hay query, tomamos una cadena vacía
    if query:
        libros = Libro.objects.filter(titulo__icontains=query)
    else:
        libros = Libro.objects.all()
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})

# Vista para agregar un libro
def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'biblioteca/agregar_libro.html', {'form': form})

def registrar_prestamo(request):
    libros = Libro.objects.all()
    usuarios = User.objects.all()  # Obtenemos todos los usuarios

    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)  # No guardamos todavía, necesitamos agregar la fecha y usuario
            prestamo.fecha_prestamo = timezone.now()  # Asignamos la fecha del préstamo automáticamente
            
            # Aquí, corregimos la asignación del usuario, asegurándonos de que sea un ID y no un objeto User
            usuario_id = form.cleaned_data['usuario']  # Obtenemos el ID del usuario desde el formulario
            prestamo.usuario = User.objects.get(id=usuario_id)  # Asignamos el usuario al préstamo correctamente
            
            prestamo.save()  # Ahora guardamos el préstamo

            # Actualizamos la cantidad disponible del libro
            libro = prestamo.libro
            if libro.cantidad_disponible > 0:
                libro.cantidad_disponible -= 1
                libro.save()
                messages.success(request, f'Préstamo registrado para el libro: {libro.titulo}.')
                return redirect('lista_libros')
            else:
                messages.error(request, f'El libro "{libro.titulo}" no tiene disponibilidad.')
                return redirect('registrar_prestamo')
    else:
        form = PrestamoForm()

    return render(request, 'biblioteca/registrar_prestamo.html', {
        'form': form,
        'libros': libros,
        'usuarios': usuarios,
    })


# Vista para editar un libro
def editar_libro(request, libro_id):
    libro = Libro.objects.get(id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/editar_libro.html', {'form': form})

# Vista para eliminar un libro
def eliminar_libro(request, libro_id):
    libro = Libro.objects.get(id=libro_id)
    if request.method == 'POST':
        libro.delete()
        return redirect('lista_libros')
    return render(request, 'biblioteca/eliminar_libro.html', {'libro': libro})

# Vista para registrar una devolución de libro
def registrar_devolucion(request, prestamo_id):
    prestamo = Prestamo.objects.get(id=prestamo_id)
    if request.method == 'POST':
        libro = prestamo.libro
        libro.cantidad_disponible += 1  # Aumentar cantidad disponible del libro
        libro.save()
        prestamo.devuelto = True  # Marcar el préstamo como devuelto
        prestamo.save()
        return redirect('lista_libros')  # O cualquier otra redirección apropiada

    return render(request, 'biblioteca/registrar_devolucion.html', {'prestamo': prestamo})

# Vista para agregar un usuario
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()  # Guarda el usuario
            messages.success(request, "Usuario agregado exitosamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'biblioteca/agregar_usuario.html', {'form': form})

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)  # Obtiene el usuario con el id proporcionado
    user = usuario.user  # Obtén el modelo User relacionado

    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=user)  # El formulario de User
        if user_form.is_valid():
            user_form.save()  # Guarda los cambios en el usuario
            usuario.telefono = request.POST.get('telefono', usuario.telefono)  # Actualiza el teléfono
            usuario.save()

            messages.success(request, f'Usuario {user.username} actualizado exitosamente.')
            return redirect('lista_usuarios')  # Redirige a la lista de usuarios

    else:
        user_form = UsuarioForm(instance=user)  # Carga el formulario con el usuario actual

    return render(request, 'biblioteca/editar_usuario.html', {
        'user_form': user_form,
        'usuario': usuario
    })


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        user = usuario.user
        user.delete() 
        messages.success(request, f'Usuario {usuario.user.username} eliminado exitosamente.')
        return redirect('lista_usuarios')  # Redirige a la lista de usuarios

    return render(request, 'biblioteca/eliminar_usuario.html', {'usuario': usuario})


# Vista para listar usuarios
# Vista para listar usuarios
def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'biblioteca/lista_usuarios.html', {'usuarios': usuarios})



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'biblioteca/login.html')  