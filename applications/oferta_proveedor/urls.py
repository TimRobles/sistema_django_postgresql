from django.urls import path
from . import views

app_name = 'oferta_proveedor_app'

urlpatterns = [

    path('oferta-proveedor/', views.OfertaProveedorListView.as_view(), name='oferta_proveedor_inicio'),
    path('oferta-proveedor-tabla/', views.OfertaProveedorTabla, name='oferta_proveedor_tabla'),
    # path('oferta-proveedor/registrar/<int:lista_id>', views.OfertaProveedorCreateView.as_view(), name='oferta_proveedor_registrar'),
    path('oferta-proveedor/finalizar/<pk>/', views.OfertaProveedorFinalizarView.as_view(), name='oferta_proveedor_finalizar'),
    path('oferta-proveedor/rechazar/<pk>/', views.OfertaProveedorRechazarView.as_view(), name='oferta_proveedor_rechazar'),
    path('oferta-proveedor/detalle/<slug>/', views.OfertaProveedorDetailView.as_view(), name='oferta_proveedor_detalle'),
    path('oferta-proveedor/detalle-tabla/<slug>/', views.OfertaProveedorDetailTabla, name='oferta_proveedor_detalle_tabla'),
    # path('oferta-proveedor/duplicar/<int:requerimiento_id>', views.OfertaProveedorDuplicarView.as_view(), name='oferta_proveedor_duplicar'),
    path('oferta-proveedor/actualizar-material/<pk>/', views.OfertaProveedorDetalleUpdateView.as_view(), name='oferta_proveedor_actualizar_material'),
    path('oferta-proveedor/agregar-archivo/<str:oferta_proveedor_slug>/', views.ArchivoOfertaProveedorCreateView.as_view(), name='oferta_proveedor_agregar_archivo'),
    path('oferta-proveedor/eliminar-archivo/<pk>/', views.ArchivoOfertaProveedorDeleteView.as_view(), name='oferta_proveedor_eliminar_archivo'),
    # path('oferta-proveedor/agregar-material/<int:oferta_proveedor_id>/', views.MaterialOfertaProveedorDetalleCreateView.as_view(), name='oferta_proveedor_agregar_material'),
    # path('oferta-proveedor/enviar_correo/<int:requerimiento_id>', views.OfertaProveedorEnviarCorreoView.as_view(), name='oferta_proveedor_enviar_correo'),
    # path('oferta-proveedor/pdf/<slug>/', views.OfertaProveedorPdfView.as_view(), name='oferta_proveedor_pdf'),


    # path('proveedor-interlocutor/<str:id_interlocutor_proveedor>/', views.ProveedorView, name='proveedor_interlocutor'),

]