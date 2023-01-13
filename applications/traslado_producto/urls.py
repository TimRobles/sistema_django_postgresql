from django.urls import path
from django.contrib import admin
from .import views


app_name='traslado_producto_app'

urlSeries = [

    path('validar-series/envio-traslado-producto/detalle/<pk>/', views.ValidarSeriesEnvioTrasladoProductoDetailView.as_view(), name='validar_series_envio_traslado_producto_detalle'),
    path('validar-series/envio-traslado-producto/detalle-tabla/<pk>/', views.ValidarSeriesEnvioTrasladoProductoDetailTabla, name='validar_series_envio_traslado_producto_detalle_tabla'),
    path('validar-series-detalle/envio-traslado-producto/eliminar/<pk>/', views.ValidarSeriesEnvioTrasladoProductoDetalleDeleteView.as_view(), name='validar_series_envio_traslado_producto_detalle_eliminar'),

    path('validar-series/traspaso-stock/detalle/<pk>/', views.ValidarSeriesTraspasoStockDetailView.as_view(), name='validar_series_traspaso_stock_detalle'),
    path('validar-series/traspaso-stock/detalle-tabla/<pk>/', views.ValidarSeriesTraspasoStockDetailTabla, name='validar_series_traspaso_stock_detalle_tabla'),
    path('validar-series-detalle/traspaso-stock/eliminar/<pk>/', views.ValidarSeriesTraspasoStockDetalleDeleteView.as_view(), name='validar_series_traspaso_stock_detalle_eliminar'),
]

urlpatterns = urlSeries + [
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


    path('recepcion/',views.RecepcionTrasladoProductoListView.as_view(), name='recepcion_inicio'),
    path('recepcion/<int:id_envio>/',views.RecepcionTrasladoProductoListView.as_view(), name='recepcion_inicio'),
    path('recepcion/tabla/',views.RecepcionTrasladoProductoTabla, name='recepcion_tabla'),
    path('recepcion/registrar/',views.RecepcionTrasladoProductoCrearView.as_view(), name='recepcion_registrar'),
 
    path('recepcion/ver/<int:id_recepcion_traslado_producto>/',views.RecepcionTrasladoProductoVerView.as_view(), name='recepcion_ver'),    
    path('recepcion/ver/tabla/<int:id_recepcion_traslado_producto>/',views.RecepcionTrasladoProductoVerTabla, name='recepcion_ver_tabla'),
    path('recepcion/actualizar/<pk>/', views.RecepcionTrasladoProductoActualizarView.as_view(), name='recepcion_actualizar'),
    path('recepcion/observaciones/<pk>/', views.RecepcionTrasladoProductoObservacionesView.as_view(), name='recepcion_observaciones'),
    path('recepcion/guardar/<pk>/', views.RecepcionTrasladoProductoGuardarView.as_view(), name='recepcion_guardar'),

    path('recepcion/agregar-material/<int:id_recepcion_traslado_producto>/', views.RecepcionTrasladoProductoMaterialDetalleView.as_view(), name='recepcion_agregar_material'),
    path('recepcion/actualizar-material/<pk>/', views.RecepcionTrasladoProductoActualizarMaterialDetalleView.as_view(), name='recepcion_actualizar_material'),
    path('recepcion/eliminar-material/<pk>/', views.RecepcionTrasladoProductoMaterialDeleteView.as_view(), name='recepcion_eliminar_material'),

    path('motivo-traslado/crear/', views.MotivoTrasladoCreateView.as_view(), name='motivo_traslado_crear'),

    path('stock/<int:id_recepcion_traslado_producto_detalle>/', views.StockView, name='stock'),
    path('stock/<int:id_recepcion_traslado_producto_detalle>/<int:id_sociedad>/<int:id_almacen>/', views.StockSociedadAlmacenView, name='stock'),
    path('unidad/material/<str:id_recepcion_traslado_producto_detalle>/', views.UnidadMaterialView, name='unidad_material'),
    
    path('traspaso-stock/', views.TraspasoStockListView.as_view(), name='traspaso_stock_inicio'),
    path('traspaso-stock-tabla/', views.TraspasoStockTabla, name='traspaso_stock_tabla'),
    path('traspaso-stock/registrar/', views.TraspasoStockCreateView.as_view(), name='traspaso_stock_registrar'),
    path('traspaso-stock/actualizar/<pk>', views.TraspasoStockUpdateView.as_view(), name='traspaso_stock_actualizar'),
    path('traspaso-stock/concluir/<pk>/', views.TraspasoStockConcluirView.as_view(), name='traspaso_stock_concluir'),
    path('traspaso-stock/detalle/<pk>/', views.TraspasoStockDetailView.as_view(), name='traspaso_stock_detalle'),
    path('traspaso-stock/detalle-tabla/<pk>/', views.TraspasoStockDetailTabla, name='traspaso_stock_detalle_tabla'),
    path('traspaso-stock-detalle/registrar/<int:traspaso_stock_id>/', views.TraspasoStockDetalleCreateView.as_view(), name='traspaso_stock_detalle_registrar'),
    path('traspaso-stock-detalle/actualizar/<int:traspaso_stock_id>/<pk>/', views.TraspasoStockDetalleUpdateView.as_view(), name='traspaso_stock_detalle_actualizar'),
 ]