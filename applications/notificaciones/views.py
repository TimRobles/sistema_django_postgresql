from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Notificaciones
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def notificaciones(request):
    notificaciones = Notificaciones.objects.filter(usuario=request.user).order_by('-created_at')
    no_leidas = notificaciones.filter(leido=False).count()
    return render(request, 'notificaciones/notificaciones.html', {'notificaciones': notificaciones, 'no_leidas': no_leidas})

@login_required
def marcar_como_leido(request, id_notificacion):
    notification = Notificaciones.objects.get(id=id_notificacion, usuario=request.user)
    #notification = get_object_or_404(Notificaciones, id=id_notificacion, usuario=request.user)
    notification.leido = True
    notification.save()
    #return redirect('notificaciones')
    return render(request, 'notificaciones/notificaciones.html')


# poner la función 'enviar_notificacion' en los programas
def enviar_notificacion(usuario, titulo, mensaje, url): 
    notificacion = Notificaciones.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensaje=mensaje,
        url=url
    )
    notificacion.save()



### prueba de mensaje:
import pywhatkit


def enviar_mensaje_whatsapp(request):
    id_grupo = "HE3omy3KoKj5FAYSfigJ0i"
    pywhatkit.sendwhatmsg_to_group(id_grupo, "mensaje prueba", 12, 6)
    return render(request, 'whatsapp/index.html', {})