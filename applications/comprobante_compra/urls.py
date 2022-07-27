from django.urls import path
from . import views

app_name = 'comprobante_compra_app'

urlpatterns = [

    path('comprobante-compra-pi/lista/', views.ComprobanteCompraPIListView.as_view(), name='comprobante_compra_pi_lista'),
    path('comprobante-compra-pi/detalle/<slug>/', views.ComprobanteCompraPIDetailView.as_view(), name='comprobante_compra_pi_detalle'),
    path('comprobante-compra-pi/detalle/tabla/<slug>/', views.ComprobanteCompraPIDetailTabla, name='comprobante_compra_pi_detalle_tabla'),
    path('comprobante-compra-pi/logistico/<slug>/', views.ComprobanteCompraPILogisticoUpdateView.as_view(), name='comprobante_compra_pi_logistico'),
    path('comprobante-compra-pi/registrar/<str:slug>/', views.ComprobanteCompraCIRegistrarView.as_view(), name='comprobante_compra_ci_registrar'),
    
    path('archivo-comprobante-compra-pi/crear/<str:slug>/', views.ArchivoComprobanteCompraPICreateView.as_view(), name='archivo_comprobante_compra_pi_crear'),
    path('archivo-comprobante-compra-pi/eliminar/<pk>/', views.ArchivoComprobanteCompraPIDeleteView.as_view(), name='archivo_comprobante_compra_pi_eliminar'),
    
    path('recepcion-comprobante-compra-pi/<str:slug>/', views.RecepcionComprobanteCompraPIView.as_view(), name='recepcion_comprobante_compra_pi'),
    
    path('comprobante-compra-ci/detalle/<slug>/', views.ComprobanteCompraCIDetailView.as_view(), name='comprobante_compra_ci_detalle'),
    path('comprobante-compra-ci/detalle/tabla/<slug>/', views.ComprobanteCompraCIDetailTabla, name='comprobante_compra_ci_detalle_tabla'),
    path('comprobante-compra-ci/finalizar/<slug>/', views.ComprobanteCompraCIFinalizarView.as_view(), name='comprobante_compra_ci_finalizar'),
    path('comprobante-compra-ci/actualizar-material/<pk>/', views.ComprobanteCompraCIDetalleUpdateView.as_view(), name='comprobante_compra_ci_actualizar_material'),

    
]