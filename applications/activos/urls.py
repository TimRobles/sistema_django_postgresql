from django.urls import path
from . import views

app_name='activos_app'

urlInventarioActivo =[
    path('inventario-activo/', views.InventarioActivoListView.as_view(), name='inventario_activo_inicio'),
    path('inventario-activo-tabla/', views.InventarioActivoTabla, name='inventario_activo_tabla'),
    path('inventario-activo/registrar/', views.InventarioActivoCreateView.as_view(), name='inventario_activo_registrar'),
    path('inventario-activo/actualizar/<pk>', views.InventarioActivoUpdateView.as_view(), name='inventario_activo_actualizar'),
    path('inventario-activo/eliminar/<pk>', views.InventarioActivoDeleteView.as_view(), name='inventario_activo_eliminar'),
    path('inventario-activo/detalle/<pk>/', views.InventarioActivoDetailView.as_view(), name='inventario_activo_detalle'),
    path('inventario-activo/detalle-tabla/<pk>/', views.InventarioActivoDetailTabla, name='inventario_activo_detalle_tabla'),
]

urlComprobanteCompraActivo = [
    path('comprobante-compra-activo/', views.ComprobanteCompraActivoListView.as_view(), name='comprobante_compra_activo_inicio'),
    path('comprobante-compra-activo-tabla/', views.ComprobanteCompraActivoTabla, name='comprobante_compra_activo_tabla'),
    path('comprobante-compra-activo/registrar/', views.ComprobanteCompraActivoCreateView.as_view(), name='comprobante_compra_activo_registrar'),
    path('comprobante-compra-activo/actualizar/<pk>', views.ComprobanteCompraActivoUpdateView.as_view(), name='comprobante_compra_activo_actualizar'),
    path('comprobante-compra-activo/detalle/<pk>/', views.ComprobanteCompraActivoDetailView.as_view(), name='comprobante_compra_activo_detalle'),
    path('comprobante-compra-activo/detalle-tabla/<pk>/', views.ComprobanteCompraActivoDetailTabla, name='comprobante_compra_activo_detalle_tabla'),
    path('comprobante-compra-activo/detalle/registrar/<int:comprobante_compra_activo_id>/', views.ComprobanteCompraActivoDetalleCreateView.as_view(), name='comprobante_compra_activo_detalle_registrar'),
    path('comprobante-compra-activo/detalle/actualizar/<pk>', views.ComprobanteCompraActivoDetalleUpdateView.as_view(), name='comprobante_compra_activo_detalle_actualizar'),
    path('comprobante-compra-activo/detalle/eliminar/<pk>/', views.ComprobanteCompraActivoDetalleDeleteView.as_view(), name='comprobante_compra_activo_detalle_eliminar'),
    path('comprobante-compra-activo/archivo/agregar/<int:comprobante_compra_activo_id>/', views.ArchivoComprobanteCompraActivoCreateView.as_view(), name='comprobante_compra_activo_archivo_agregar'),
    path('comprobante-compra-activo/archivo/eliminar/<pk>/', views.ArchivoComprobanteCompraActivoDeleteView.as_view(), name='comprobante_compra_activo_archivo_eliminar'),
]

urlActivoUbicacion = [
    path('activo-ubicacion/relacionar/<int:activo_id>/', views.ActivoUbicacionCreateView.as_view(), name='activo_ubicacion_relacionar'),
    path('activo-ubicacion/actualizar/<pk>/', views.ActivoUbicacionUpdateView.as_view(), name='activo_ubicacion_actualizar'),  
]

urlActivoSociedad = [
    path('activo-sociedad/relacionar/<int:activo_id>/', views.ActivoSociedadCreateView.as_view(), name='activo_sociedad_relacionar'),
    path('activo-sociedad/actualizar/<pk>/', views.ActivoSociedadUpdateView.as_view(), name='activo_sociedad_actualizar'),  
]

urlActivoBase = [
    path('activo_base/', views.ActivoBaseListView.as_view(), name='activo_base_inicio'),
    path('activo_base-tabla/', views.ActivoBaseTabla, name='activo_base_tabla'),
    path('activo_base/registrar/', views.ActivoBaseCreateView.as_view(), name='activo_base_registrar'),
    path('activo_base/actualizar/<pk>', views.ActivoBaseUpdateView.as_view(), name='activo_base_actualizar'),
    path('activo_base/actualizar_sunat/<pk>', views.ProductoSunatActivoUpdateView.as_view(), name='activo_base_actualizar_sunat'),
    path('activo_base/dar_baja/<pk>', views.ActivoBaseDarBajaView.as_view(), name='activo_base_dar_baja'),
    path('activo_base/dar_alta/<pk>', views.ActivoBaseDarAltaView.as_view(), name='activo_base_dar_alta'),

    path('subfamilia_activo/<str:id_familia>/', views.SubFamiliaActivoView, name='sub_familia_activo'),

    path('familia-sunat_activo/<str:id_segmento>/', views.FamiliaSunatActivoView, name='familia_sunat'),
    path('clase-sunat_activo/<str:id_familia>/', views.ClaseSunatActivoView, name='clase_sunat'),
    path('producto-sunat_activo/<str:id_clase>/', views.ProductoSunatActivoView, name='producto_sunat'),
]


urlAsignacionActivo = [
    path('asignacion_activo/', views.AsignacionActivoListView.as_view(), name='asignacion_activo_inicio'),
    path('asignacion_activo-tabla/', views.AsignacionActivoTabla, name='asignacion_activo_tabla'),
    path('asignacion_activo/registrar/', views.AsignacionActivoCreateView.as_view(), name='asignacion_activo_registrar'),
    path('asignacion_activo/actualizar/<pk>', views.AsignacionActivoUpdateView.as_view(), name='asignacion_activo_actualizar'),
    path('asignacion_activo/dar_baja/<pk>', views.AsignacionActivoDarBajaView.as_view(), name='asignacion_activo_dar_baja'),
    path('asignacion_activo/concluir_sin_asignar/<pk>', views.AsignacionActivoConcluirView.as_view(), name='asignacion_activo_concluir_sin_asignar'),
    path('asignacion_activo/pdf/<pk>', views.AsignacionActivoPdfView.as_view(), name='asignacion_activo_pdf'),
    
    path('asignacion_activo/agregar-archivo/<int:asignacion_id>', views.ArchivoAsignacionActivoCreateView.as_view(), name='asignacion_activo_agregar_archivo'),
    path('asignacion_activo/eliminar-archivo/<pk>', views.ArchivoAsignacionActivoDeleteView.as_view(), name='asignacion_activo_eliminar_archivo'),
    # path('asignacion_activo/tabla-archivos/<int:asignacion_id>', views.ArchivoAsignacionActivoTabla, name='asignacion_activo_tabla_archivo'),

    path('asignacion_activo_detalle/<pk>', views.AsignacionActivoDetailView.as_view(), name='asignacion_activo_detalle_inicio'),
    path('asignacion_activo_detalle-tabla/<pk>', views.AsignacionActivoDetalleTabla, name='asignacion_activo_detalle_tabla'),
    path('asignacion_activo_detalle/registrar/<int:asignacion_id>/', views.AsignacionDetalleActivoCreateView.as_view(), name='asignacion_activo_detalle_registrar'),
    path('asignacion_activo_detalle/eliminar/<pk>', views.AsignacionDetalleActivoDeleteView.as_view(), name='asignacion_activo_detalle_eliminar'),
]

urlModelos = [
    path('modelo-activo/', views.ModeloActivoListView.as_view(), name='modelo_activo_inicio'),
    path('modelo-activo-tabla/', views.ModeloActivoTabla, name='modelo_activo_tabla'),
    path('modelo-activo/registrar/', views.ModeloActivoCreateView.as_view(), name='modelo_activo_registrar'),
    path('modelo-activo/actualizar/<pk>/', views.ModeloActivoUpdateView.as_view(), name='modelo_activo_actualizar'),
]

urlMarcas = [
    path('marca-activo/', views.MarcaActivoListView.as_view(), name='marca_activo_inicio'),
    path('marca-activo-tabla/', views.MarcaActivoTabla, name='marca_activo_tabla'),
    path('marca-activo/registrar/', views.MarcaActivoCreateView.as_view(), name='marca_activo_registrar'),
    path('marca-activo/actualizar/<pk>/', views.MarcaActivoUpdateView.as_view(), name='marca_activo_actualizar'),
]

urlpatterns = [

    path('activo/', views.ActivoListView.as_view(), name='activo_inicio'),
    path('activo-tabla/', views.ActivoTabla, name='activo_tabla'),
    path('activo/registrar/', views.ActivoCreateView.as_view(), name='activo_registrar'),
    path('activo/actualizar/<pk>', views.ActivoUpdateView.as_view(), name='activo_actualizar'),
    path('activo/eliminar/<pk>', views.ActivoDeleteView.as_view(), name='activo_eliminar'),
    path('activo/detalle/<pk>/', views.ActivoDetailView.as_view(), name='activo_detalle'),
    path('activo/detalle-tabla/<pk>/', views.ActivoDetailTabla, name='activo_detalle_tabla'),

] + urlInventarioActivo + urlComprobanteCompraActivo + urlActivoUbicacion + urlActivoSociedad + urlActivoBase + urlModelos + urlMarcas + urlActivoBase + urlAsignacionActivo
