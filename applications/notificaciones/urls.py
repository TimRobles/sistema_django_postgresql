from django.urls import path
from . import views

app_name = 'notificaciones_app'

urlpatterns = [
path('notificaciones/', views.notificaciones, name='notificaciones'),
path('notificaciones/marcar-como-leido/int:id_notificacion', views.marcar_como_leido, name='marcar_como_leido'),
path('notificaciones/crear/', views.crear_notificacion, name='crear_notificacion'),
]