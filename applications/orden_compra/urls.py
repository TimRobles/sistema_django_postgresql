from django.urls import path
from . import views

app_name = 'orden_compra_app'

urlpatterns = [ 
    path('orden-compra/', views.OrdenCompraListView.as_view(), name='orden_compra_inicio'),
    path('orden-compra-tabla/', views.OrdenCompraTabla, name='orden_compra_tabla'),
    path('orden-compra/detalle/<pk>/', views.OrdenCompraDetailView.as_view(), name='orden_compra_detalle'),
    path('orden-compra/detalle-tabla/<pk>/', views.OrdenCompraDetailTabla, name='orden_compra_detalle_tabla'),
    path('orden-compra/eliminar/<pk>/', views.OrdenCompraDeleteView.as_view(), name='orden_compra_eliminar'),
    path('orden-compra/pdf-anular/<slug>/', views.OrdenCompraMotivoAnulacionPdfView.as_view(), name='orden_compra_pdf_anular'),
    path('orden-compra/enviar-correo/<int:orden_id>', views.OrdenCompraEnviarCorreoView.as_view(), name='orden_compra_enviar_correo'),
    path('orden-compra/pdf/<slug>/', views.OrdenCompraPdfView.as_view(), name='orden_compra_pdf'),
    
 ]