from django.urls import path
from . import views

app_name = 'oferta_proveedor_app'

urlpatterns = [

    path('oferta-proveedor/', views.OfertaProveedorListView.as_view(), name='oferta_proveedor_inicio'),
    path('oferta-proveedor-tabla/', views.OfertaProveedorTabla, name='oferta_proveedor_tabla'),
    path('oferta-proveedor/finalizar/<pk>/', views.OfertaProveedorFinalizarView.as_view(), name='oferta_proveedor_finalizar'),
    path('oferta-proveedor/rechazar/<pk>/', views.OfertaProveedorRechazarView.as_view(), name='oferta_proveedor_rechazar'),
    path('oferta-proveedor/detalle/<slug>/', views.OfertaProveedorDetailView.as_view(), name='oferta_proveedor_detalle'),
    path('oferta-proveedor/detalle-tabla/<slug>/', views.OfertaProveedorDetailTabla, name='oferta_proveedor_detalle_tabla'),
    path('oferta-proveedor/actualizar-moneda/<slug>/', views.OfertaProveedorMonedaView.as_view(), name='oferta_proveedor_actualizar_moneda'),
    path('oferta-proveedor/actualizar-material/<pk>/', views.OfertaProveedorDetalleUpdateView.as_view(), name='oferta_proveedor_actualizar_material'),
    path('oferta-proveedor/proveedor-material/<int:detalle_id>/', views.OfertaProveedorDetalleProveedorMaterialUpdateView.as_view(), name='oferta_proveedor_proveedor_material'),
    path('oferta-proveedor/eliminar-material/<pk>/', views.OfertaProveedorDetalleDeleteView.as_view(), name='oferta_proveedor_eliminar_material'),
    path('oferta-proveedor/agregar-material/<str:oferta_proveedor_slug>/', views.MaterialOfertaProveedorAgregarView.as_view(), name='oferta_proveedor_agregar_material'),
    path('oferta-proveedor/crear-material/<str:oferta_proveedor_slug>/', views.MaterialOfertaProveedorCrearView.as_view(), name='oferta_proveedor_crear_material'),
    path('oferta-proveedor/agregar-archivo/<str:oferta_proveedor_slug>/', views.ArchivoOfertaProveedorCreateView.as_view(), name='oferta_proveedor_agregar_archivo'),
    path('oferta-proveedor/eliminar-archivo/<pk>/', views.ArchivoOfertaProveedorDeleteView.as_view(), name='oferta_proveedor_eliminar_archivo'),
    path('oferta-proveedor/generar-nuevo-requerimiento/<slug>/', views.OfertaProveedorGenerarNuevoRequerimientoView.as_view(), name='oferta_proveedor_generar_nuevo_requerimiento'),
    path('oferta-proveedor/generar-orden-compra/<str:slug_oferta>/', views.OfertaProveedorGenerarOrdenCompraView.as_view(), name='oferta_proveedor_generar_orden_compra'),

]