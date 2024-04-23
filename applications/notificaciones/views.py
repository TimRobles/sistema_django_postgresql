from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Notificaciones
from django.contrib.auth.decorators import login_required

@login_required
def notificaciones(request):
    notificaciones = Notificaciones.objects.filter(usuario=request.user).order_by('-created_at')
    no_leidas = notificaciones.filter(leido=False).count()
    return render(request, 'notificaciones/notificaciones.html', {'notificaciones': notificaciones, 'no_leidas': no_leidas})

@login_required
def marcar_como_leido(request, id_notificacion):
    notification = Notificaciones.objects.get(id=id_notificacion, usuario=request.user)
    notification.leido = True
    notification.save()
    return redirect('notificaciones')


def enviar_notificacion(usuario, titulo, mensaje):
    notificacion = Notificaciones.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensaje=mensaje
    )
    notificacion.save()
    # Aquí puedes agregar lógica adicional para enviar la notificación
    # por push, email, etc.

# En tu otro programa, llamas a esta función cuando ocurre la acción
#def realizar_accion():
#    usuario = User.objects.get(username='john_doe')
#    enviar_notificacion(usuario, 'Nueva Acción', 'Se ha realizado una nueva acción en el sistema.')

@login_required
def crear_notificacion(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        mensaje = request.POST['mensaje']
        notificacion = Notificaciones.objects.create(usuario=request.user, titulo=titulo, mensaje=mensaje)
        return redirect('notificaciones')
    return render(request, 'notificaciones/crear_notificacion.html')

