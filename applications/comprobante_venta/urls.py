from django.urls import path
from . import views

app_name = 'comprobante_venta_app'

urlpatterns = [ 
    path('factura-venta/',views.FacturaVentaListView.as_view(),name='factura_venta_inicio'),
    path('factura-venta-tabla/',views.FacturaVentaTabla,name='factura_venta_tabla'),

    path('factura-venta/detalle/<int:id_factura_venta>/', views.FacturaVentaDetalleView.as_view(), name='factura_venta_detalle'),
    path('factura-venta/detalle/tabla/<int:id_factura_venta>/', views.FacturaVentaDetalleVerTabla, name='factura_venta_detalle_tabla'),
    
    path('factura-venta-detalle/actualizar/<pk>/', views.FacturaVentaDetalleUpdateView.as_view(), name='factura_venta_detalle_actualizar'),
    
    path('factura-venta/crear/<pk>/', views.FacturaVentaCrearView.as_view(), name='factura_venta_crear'),
    path('factura-venta/anticipo/crear/<pk>/', views.FacturaVentaAnticipoCrearView.as_view(), name='factura_venta_anticipo_crear'),
    path('factura-venta/anticipo/regularizar/crear/<pk>/', views.FacturaVentaAnticipoRegularizarCrearView.as_view(), name='factura_venta_anticipo_regularizar_crear'),
    path('factura-venta/serie/<pk>/', views.FacturaVentaSerieUpdateView.as_view(), name='factura_venta_serie'),
    path('factura-venta/direccion/<int:id_factura>/<pk>/', views.FacturaVentaDireccionView.as_view(), name='factura_venta_direccion'),
    path('factura-venta/guardar/<pk>/', views.FacturaVentaGuardarView.as_view(), name='factura_venta_guardar'),
    path('factura-venta/anular/<pk>/', views.FacturaVentaAnularView.as_view(), name='factura_venta_anular'),
    path('factura-venta/eliminar/<pk>/', views.FacturaVentaEliminarView.as_view(), name='factura_venta_eliminar'),

    path('factura-venta/nubefact/enviar/<pk>/', views.FacturaVentaNubeFactEnviarView.as_view(), name='factura_venta_nubefact_enviar'),
    path('factura-venta/nubefact/anular/<pk>/', views.FacturaVentaNubeFactAnularView.as_view(), name='factura_venta_nubefact_anular'),
    path('factura-venta/nubefact/detalle/<pk>/', views.FacturaVentaNubefactRespuestaDetailView.as_view(), name='factura_venta_nubefact_detalle'),
    path('factura-venta/nubefact/consultar/<pk>/', views.FacturaVentaNubefactConsultarView.as_view(), name='factura_venta_nubefact_consultar'),

    path('boleta-venta/',views.BoletaVentaListView.as_view(),name='boleta_venta_inicio'),
    path('boleta-venta-tabla/',views.BoletaVentaTabla,name='boleta_venta_tabla'),

    path('boleta-venta/detalle/<int:id_boleta_venta>/', views.BoletaVentaDetalleView.as_view(), name='boleta_venta_detalle'),
    path('boleta-venta/detalle/tabla/<int:id_boleta_venta>/', views.BoletaVentaDetalleVerTabla, name='boleta_venta_detalle_tabla'),

    path('boleta-venta/crear/<pk>/', views.BoletaVentaCrearView.as_view(), name='boleta_venta_crear'),
    path('boleta-venta/serie/<pk>/', views.BoletaVentaSerieUpdateView.as_view(), name='boleta_venta_serie'),
    path('boleta-venta/guardar/<pk>/', views.BoletaVentaGuardarView.as_view(), name='boleta_venta_guardar'),
    path('boleta-venta/anular/<pk>/', views.BoletaVentaAnularView.as_view(), name='boleta_venta_anular'),
    path('boleta-venta/eliminar/<pk>/', views.BoletaVentaEliminarView.as_view(), name='boleta_venta_eliminar'),
    
    path('boleta-venta/nubefact/enviar/<pk>/', views.BoletaVentaNubeFactEnviarView.as_view(), name='boleta_venta_nubefact_enviar'),
    path('boleta-venta/nubefact/anular/<pk>/', views.BoletaVentaNubeFactAnularView.as_view(), name='boleta_venta_nubefact_anular'),
    path('boleta-venta/nubefact/detalle/<pk>/', views.BoletaVentaNubefactRespuestaDetailView.as_view(), name='boleta_venta_nubefact_detalle'),
    path('boleta-venta/nubefact/consultar/<pk>/', views.BoletaVentaNubefactConsultarView.as_view(), name='boleta_venta_nubefact_consultar'),
]