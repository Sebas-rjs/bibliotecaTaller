from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Login será la página principal
    path('inicio/', views.inicio, name='inicio'),
    path('lista-libros/', views.lista_libros, name='lista_libros'),
    path('agregar-libro/', views.agregar_libro, name='agregar_libro'),
    path('editar-libro/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('eliminar-libro/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('registrar-prestamo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('registrar-devolucion/<int:prestamo_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('lista-usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
