from django.urls import path
from . import views

app_name = 'requerimiento_material_app'

urlpatterns = [
    path('lista-requerimiento-material/', views.ListaRequerimientoMaterialListView.as_view(), name='lista_requerimiento_material_inicio'),
    path('lista-requerimiento-material-tabla/', views.ListaRequerimientoMaterialTabla, name='lista_requerimiento_material_tabla'),
    path('lista-requerimiento-material/registrar/', views.ListaRequerimientoMaterialCreateView.as_view(), name='lista_requerimiento_material_registrar'),
    path('lista-requerimiento-material-detalle-tabla/<int:requerimiento_id>/', views.ListaRequerimientoMaterialDetalleTabla, name='lista_requerimiento_material_detalle_tabla'),
    path('lista-requerimiento-material/actualizar/<pk>/', views.ListaRequerimientoMaterialUpdateView.as_view(), name='lista_requerimiento_material_actualizar'),
    path('lista-requerimiento-material/agregar-material/<int:requerimiento_id>/', views.ListaRequerimientoMaterialDetalleCreateView.as_view(), name='lista_requerimiento_material_agregar_material'),
    path('lista-requerimiento-material/actualizar-material/<pk>/', views.ListaRequerimientoMaterialDetalleUpdateView.as_view(), name='lista_requerimiento_material_actualizar_material'),
    path('lista-requerimiento-material/eliminar/<pk>/', views.ListaRequerimientoMaterialDetalleDeleteView.as_view(), name='lista_requerimiento_material_eliminar_material'),
    path('lista-requerimiento-material/eliminar-lista/<pk>/', views.ListaRequerimientoMaterialDeleteView.as_view(), name='lista_requerimiento_material_eliminar'),


    path('requerimiento-material-proveedor/', views.RequerimientoMaterialProveedorListView.as_view(), name='requerimiento_material_proveedor_inicio'),
    path('requerimiento-material-proveedor-tabla/', views.RequerimientoMaterialProveedorTabla, name='requerimiento_material_proveedor_tabla'),
    path('requerimiento-material-proveedor/registrar/<int:lista_id>', views.RequerimientoMaterialProveedorCreateView.as_view(), name='requerimiento_material_proveedor_registrar'),
    path('requerimiento-material-proveedor/actualizar/<pk>/', views.RequerimientoMaterialProveedorUpdateView.as_view(), name='requerimiento_material_proveedor_actualizar'),
    path('requerimiento-material-proveedor/eliminar-lista/<pk>/', views.RequerimientoMaterialProveedorDeleteView.as_view(), name='requerimiento_material_proveedor_eliminar'),
    path('requerimiento-material-proveedor/detalle/<pk>/', views.RequerimientoMaterialProveedorDetailView.as_view(), name='requerimiento_material_proveedor_detalle'),
    path('requerimiento-material-proveedor/detalle-tabla/<pk>/', views.RequerimientoMaterialProveedorDetailTabla, name='requerimiento_material_proveedor_detalle_tabla'),
    path('requerimiento-material-proveedor/duplicar/<int:requerimiento_id>', views.RequerimientoMaterialProveedorDuplicarView.as_view(), name='requerimiento_material_proveedor_duplicar'),
    path('requerimiento-material-proveedor/actualizar-material/<pk>/', views.RequerimientoMaterialProveedorDetalleUpdateView.as_view(), name='requerimiento_material_proveedor_actualizar_material'),
    path('requerimiento-material-proveedor/eliminar-material/<pk>/', views.RequerimientoMaterialProveedorDetalleDeleteView.as_view(), name='requerimiento_material_proveedor_eliminar_material'),
    path('requerimiento-material-proveedor/agregar-material/<int:requerimiento_id>/', views.RequerimientoMaterialProveedorDetalleCreateView.as_view(), name='requerimiento_material_proveedor_agregar_material'),
    path('requerimiento-material-proveedor/pdf/<pk>/', views.RequerimientoMaterialProveedorPdfView.as_view(), name='requerimiento_material_proveedor_pdf'),


    path('requerimiento-material/', views.RequerimientoMaterialListView.as_view(), name='requerimiento_material_inicio'),
    path('requerimiento-material-tabla/', views.RequerimientoMaterialTabla, name='requerimiento_material_tabla'),
    path('requerimiento-material/registrar/', views.RequerimientoMaterialCreateView.as_view(), name='requerimiento_material_registrar'),
    path('requerimiento-material-detalle-tabla/<int:requerimiento_id>/', views.RequerimientoMaterialDetalleTabla, name='requerimiento_material_detalle_tabla'),
    path('requerimiento-material/actualizar/<pk>/', views.RequerimientoMaterialUpdateView.as_view(), name='requerimiento_material_actualizar'),
    path('requerimiento-material/agregar-material/<int:requerimiento_id>/', views.RequerimientoMaterialDetalleCreateView.as_view(), name='requerimiento_material_agregar_material'),
    path('requerimiento-material/actualizar-material/<pk>/', views.RequerimientoMaterialDetalleUpdateView.as_view(), name='requerimiento_material_actualizar_material'),
    path('requerimiento-material/eliminar/<pk>/', views.RequerimientoMaterialDetalleDeleteView.as_view(), name='requerimiento_material_eliminar_material'),


    path('proveedor-interlocutor/<str:id_interlocutor_proveedor>/', views.ProveedorView, name='proveedor_interlocutor'),

]
