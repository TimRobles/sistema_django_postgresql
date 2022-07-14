from django.urls import path
from . import views

app_name = 'oferta_proveedor_app'

urlpatterns = [

    path('oferta-proveedor/', views.OfertaProveedorListView.as_view(), name='oferta_proveedor_inicio'),
    path('oferta-proveedor-tabla/', views.OfertaProveedorTabla, name='oferta_proveedor_tabla'),
    # path('oferta-proveedor/registrar/<int:lista_id>', views.OfertaProveedorCreateView.as_view(), name='oferta_proveedor_registrar'),
    path('oferta-proveedor/actualizar/<pk>/', views.OfertaProveedorUpdateView.as_view(), name='oferta_proveedor_actualizar'),
    # path('oferta-proveedor/eliminar-lista/<pk>/', views.OfertaProveedorDeleteView.as_view(), name='oferta_proveedor_eliminar'),
    path('oferta-proveedor/detalle/<pk>/', views.OfertaProveedorDetailView.as_view(), name='oferta_proveedor_detalle'),
    path('oferta-proveedor/detalle-tabla/<pk>/', views.OfertaProveedorDetailTabla, name='oferta_proveedor_detalle_tabla'),
    # path('oferta-proveedor/duplicar/<int:requerimiento_id>', views.OfertaProveedorDuplicarView.as_view(), name='oferta_proveedor_duplicar'),
    path('oferta-proveedor/actualizar-material/<pk>/', views.OfertaProveedorDetalleUpdateView.as_view(), name='oferta_proveedor_actualizar_material'),
    # path('oferta-proveedor/eliminar-material/<pk>/', views.OfertaProveedorDetalleDeleteView.as_view(), name='oferta_proveedor_eliminar_material'),
    # path('oferta-proveedor/agregar-material/<int:requerimiento_id>/', views.OfertaProveedorDetalleCreateView.as_view(), name='oferta_proveedor_agregar_material'),
    # path('oferta-proveedor/enviar_correo/<int:requerimiento_id>', views.OfertaProveedorEnviarCorreoView.as_view(), name='oferta_proveedor_enviar_correo'),
    # path('oferta-proveedor/pdf/<slug>/', views.OfertaProveedorPdfView.as_view(), name='oferta_proveedor_pdf'),


    # path('proveedor-interlocutor/<str:id_interlocutor_proveedor>/', views.ProveedorView, name='proveedor_interlocutor'),

]