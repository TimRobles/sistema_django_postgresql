from django.urls import path
from . import views

app_name = 'recepcion_compra_app'

urlpatterns = [

    path('recepcion-compra/detalle/<pk>/', views.RecepcionCompraDetailView.as_view(), name='recepcion_compra_detalle'),
    path('recepcion-compra/detalle/tabla/<pk>/', views.RecepcionCompraDetailTabla, name='recepcion_compra_detalle_tabla'),

    path('archivo-recepcion-compra/crear/<int:pk>/', views.ArchivoRecepcionCompraCreateView.as_view(), name='archivo_recepcion_compra_crear'),
    path('archivo-recepcion-compra/eliminar/<pk>/', views.ArchivoRecepcionCompraDeleteView.as_view(), name='archivo_recepcion_compra_eliminar'),
    
    path('foto-recepcion-compra/crear/<int:pk>/', views.FotoRecepcionCompraCreateView.as_view(), name='foto_recepcion_compra_crear'),
    path('foto-recepcion-compra/eliminar/<pk>/', views.FotoRecepcionCompraDeleteView.as_view(), name='foto_recepcion_compra_eliminar'),
    
    path('recepcion-compra/generar-nota-ingreso/<int:pk>/', views.RecepcionCompraGenerarNotaIngresoView.as_view(), name='recepcion_compra_generar_nota_credito'),
]