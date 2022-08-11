from django.urls import path
from . import views

app_name='encuesta_app'

urlpatterns = [
    path('respuesta/lista/', views.RespuestaListaView.as_view(), name='respuesta_lista'),
    path('lista/NuevaRespuesta/', views.NuevaEncuestaView.as_view(), name='nueva_encuesta'),
    path('respuesta/cliente/actualizar/<pk>/', views.RespuestaClienteActualizar.as_view(), name='respuesta_cliente_actualizar'),
    path('respuesta/cliente/crear/', views.RespuestaClienteCrear.as_view(), name='respuesta_cliente_crear'),
    path('respuesta/detalle/crear/', views.RespuestaDetalleCrear, name='respuesta_detalle_crear'),
    path('encuestar/<int:respuesta_id>/', views.Encuestar.as_view(), name='encuestar'),
    path('encuestar/<int:respuesta_id>/<int:tipo_encuesta>/', views.EncuestarSegundaParte.as_view(), name='encuestar_segunda_parte'),
    path('respuesta/detalle/ver/<pk>/', views.EncuestaDetalleVer.as_view(), name='respuesta_detalle_ver'),


]