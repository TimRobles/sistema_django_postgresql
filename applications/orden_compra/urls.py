from django.urls import path
from . import views

app_name = 'orden_compra_app'

urlpatterns = [ 

    path('orden-compra/', views.OrdenCompraListView.as_view(), name='orden_compra_inicio'),
    path('orden-compra-tabla/', views.OrdenCompraTabla, name='orden_compra_tabla'),
    path('orden-compra/anular/<pk>/', views.OrdenCompraAnularView.as_view(), name='orden_compra_anular'),
    
    path('orden-compra/detalle/<slug>/', views.OrdenCompraDetailView.as_view(), name='orden_compra_detalle'),
    path('orden-compra/detalle-tabla/<slug>/', views.OrdenCompraDetailTabla, name='orden_compra_detalle_tabla'),
    path('orden-compra/pdf-anular/<slug>/', views.OrdenCompraMotivoAnulacionPdfView.as_view(), name='orden_compra_pdf_anular'),
    path('orden-compra/enviar-correo/<slug>/', views.OrdenCompraEnviarCorreoView.as_view(), name='orden_compra_enviar_correo'),
    path('orden-compra/pdf/<slug>/', views.OrdenCompraPdfView.as_view(), name='orden_compra_pdf'),
    path('orden-compra/nueva-version/<pk>/', views.OrdenCompraNuevaVersionView.as_view(), name='orden_compra_nueva_version'),
    path('orden-compra/crear/', views.OrdenCompraCreateView.as_view(), name='orden_compra_crear'),
    path('orden-compra/actualizar/<slug>/', views.OrdenCompraProveedorView.as_view(), name='orden_compra_actualizar'),
    path('orden-compra/actualizar-material/<pk>/', views.OrdenCompraProveedorDetalleUpdateView.as_view(), name='orden_compra_actualizar_material'),
    path('orden-compra/eliminar-material/<pk>/', views.OrdenCompraProveedorDetalleDeleteView.as_view(), name='orden_compra_eliminar_material'),
    path('orden-compra/agregar-material/<pk>/', views.OrdenCompraProveedorlDetalleCreateView.as_view(), name='orden_compra_agregar_material'),

    path('orden-compra/generar-comprobante-compra-total/<slug>/', views.OrdenCompraGenerarComprobanteTotalView.as_view(), name='orden_compra_generar_comprobante_compra_total'),
 ]