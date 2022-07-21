from django.urls import path
from . import views

app_name = 'comprobante_compra_app'

urlpatterns = [

    path('comprobante-compra-pi/lista/', views.ComprobanteCompraPIListView.as_view(), name='comprobante_compra_pi_lista'),
    path('comprobante-compra-pi/detalle/<slug>/', views.ComprobanteCompraPIDetailView.as_view(), name='comprobante_compra_pi_detalle'),
    path('comprobante-compra-pi/detalle/tabla/<slug>/', views.ComprobanteCompraPIDetailTabla, name='comprobante_compra_pi_detalle_tabla'),
    path('comprobante-compra-pi/logistico/<slug>/', views.ComprobanteCompraPILogisticoUpdateView.as_view(), name='comprobante_compra_pi_logistico'),
    path('archivo-comprobante-compra-pi/crear/<str:slug>/', views.ArchivoComprobanteCompraPICreateView.as_view(), name='archivo_comprobante_compra_pi_crear'),
    path('archivo-comprobante-compra-pi/eliminar/<pk>/', views.ArchivoComprobanteCompraPIDeleteView.as_view(), name='archivo_comprobante_compra_pi_eliminar'),

]