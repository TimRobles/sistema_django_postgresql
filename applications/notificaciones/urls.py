from django.urls import path
from . import views

app_name = 'notificaciones_app'

urlpatterns = [
path('notificaciones/', views.notificaciones, name='notificaciones'),
path('notificaciones/<int:id_notificacion>/marcar-como-leido/', views.marcar_como_leido, name='marcar_como_leido'),]
# path('', views.enviar_mensaje_whatsapp, name='enviar_mensaje_whatsapp'),


