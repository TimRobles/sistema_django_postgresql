from django.urls import path
from django.contrib import admin
from .import views


app_name='traslado_producto_app'

urlpatterns = [
    path('envio/',views.EnvioTrasladoProductoListView.as_view(), name='envio_inicio'),
    path('envio/tabla/',views.EnvioTrasladoProductoTabla, name='envio_tabla'),
    path('envio/registrar/',views.EnvioTrasladoProductoCrearView, name='envio_registrar'),

    path('envio/ver/<int:id_envio_traslado_producto>/',views.EnvioTrasladoProductoVerView.as_view(), name='envio_ver'),    
    path('envio/ver/tabla/<int:id_envio_traslado_producto>/',views.EnvioTrasladoProductoVerTabla, name='envio_ver_tabla'),
    path('envio/actualizar/<pk>/', views.EnvioTrasladoProductoActualizarView.as_view(), name='envio_actualizar'),
    path('envio/observaciones/<pk>/', views.EnvioTrasladoProductoObservacionesView.as_view(), name='envio_observaciones'),
    path('envio/guardar/<pk>/', views.EnvioTrasladoProductoGuardarView.as_view(), name='envio_guardar'),

    path('envio/agregar-material/<int:id_envio_traslado_producto>/', views.EnvioTrasladoProductoMaterialDetalleView.as_view(), name='envio_agregar_material'),
    path('envio/actualizar-material/<pk>/', views.EnvioTrasladoProductoActualizarMaterialDetalleView.as_view(), name='envio_actualizar_material'),
    path('envio/eliminar-material/<pk>/', views.EnvioTrasladoProductoMaterialDeleteView.as_view(), name='envio_eliminar_material'),


 ]