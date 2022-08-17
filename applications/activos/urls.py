from django.urls import path
from . import views

app_name='activos_app'

urlActivoBase = [
    path('activo_base/', views.ActivoBaseListView.as_view(), name='activo_base_inicio'),
    path('activo_base-tabla/', views.ActivoBaseTabla, name='activo_base_tabla'),
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

urlpatterns = [
] + urlActivoBase + urlAsignacionActivo