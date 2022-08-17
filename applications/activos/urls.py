from django.urls import path
from . import views

app_name='activos_app'

urlComprobanteCompraActivoDetalle =[
    path('comprobante-compra-activo/detalle/registrar/<int:comprobante_compra_activo_id>/', views.ComprobanteCompraActivoDetalleCreateView.as_view(), name='comprobante_compra_activo_detalle_registrar'),
]

urlComprobanteCompraActivo = [
    path('comprobante-compra-activo/', views.ComprobanteCompraActivoListView.as_view(), name='comprobante_compra_activo_inicio'),
    path('comprobante-compra-activo-tabla/', views.ComprobanteCompraActivoTabla, name='comprobante_compra_activo_tabla'),
    path('comprobante-compra-activo/registrar/', views.ComprobanteCompraActivoCreateView.as_view(), name='comprobante_compra_activo_registrar'),
    path('comprobante-compra-activo/actualizar/<pk>', views.ComprobanteCompraActivoUpdateView.as_view(), name='comprobante_compra_activo_actualizar'),
    path('comprobante-compra-activo/detalle/<pk>/', views.ComprobanteCompraActivoDetailView.as_view(), name='comprobante_compra_activo_detalle'),
    path('comprobante-compra-activo/detalle-tabla/<pk>/', views.ComprobanteCompraActivoDetailTabla, name='comprobante_compra_activo_detalle_tabla'),
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
    path('activo_base/dar_baja/<pk>', views.ActivoBaseDarBajaView.as_view(), name='activo_base_dar_baja'),
    path('activo_base/dar_alta/<pk>', views.ActivoBaseDarAltaView.as_view(), name='activo_base_dar_alta'),
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

] + urlComprobanteCompraActivoDetalle + urlComprobanteCompraActivo + urlActivoUbicacion + urlActivoSociedad + urlActivoBase + urlModelos + urlMarcas