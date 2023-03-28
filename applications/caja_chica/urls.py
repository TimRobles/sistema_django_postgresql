from django.urls import path
from .import views

app_name = 'caja_chica_app'

urlpatterns = [
    path('requerimiento/', views.RequerimientoListView.as_view(), name='requerimiento_inicio'),
    path('requerimiento-tabla/', views.RequerimientoTabla, name='requerimiento_tabla'),
    path('requerimiento/crear/', views.RequerimientoCreateView.as_view(), name='requerimiento_crear'),
    path('requerimiento/actualizar/<pk>/', views.RequerimientoUpdateView.as_view(), name='requerimiento_actualizar'),
    path('requerimiento/eliminar/<pk>/', views.RequerimientoDeleteView.as_view(), name='requerimiento_eliminar'),
    path('requerimiento/solicitar/<pk>/', views.RequerimientoSolicitarView.as_view(), name='requerimiento_solicitar'),
    path('requerimiento/editar/<pk>/', views.RequerimientoEditarView.as_view(), name='requerimiento_editar'),
    path('requerimiento/aprobar/<pk>/', views.RequerimientoAprobarView.as_view(), name='requerimiento_aprobar'),
    path('requerimiento/retroceder/<pk>/', views.RequerimientoRetrocederView.as_view(), name='requerimiento_retroceder'),
    path('requerimiento/rechazar/<pk>/', views.RequerimientoRechazarView.as_view(), name='requerimiento_rechazar'),
    path('requerimiento/finalizar-rendicion/<pk>/', views.RequerimientoFinalizarRendicionView.as_view(), name='requerimiento_finalizar_rendicion'),
    path('requerimiento/editar-rendicion/<pk>/', views.RequerimientoEditarRendicionView.as_view(), name='requerimiento_editar_rendicion'),
    path('requerimiento/aprobar-rendicion/<pk>/', views.RequerimientoAprobarRendicionView.as_view(), name='requerimiento_aprobar_rendicion'),
    path('requerimiento/rechazar-rendicion/<pk>/', views.RequerimientoRechazarRendicionView.as_view(), name='requerimiento_rechazar_rendicion'),
    path('requerimiento/retroceder-rendicion/<pk>/', views.RequerimientoRetrocederRendicionView.as_view(), name='requerimiento_retroceder_rendicion'),
    path('requerimiento/detalle/<pk>/', views.RequerimientoDetalleView.as_view(), name='requerimiento_detalle'),
    path('requerimiento/detalle-tabla/<pk>', views.RequerimientoDetalleTabla, name='requerimiento_detalle_tabla'),

    path('requerimiento/documento/registrar/<int:requerimiento_id>/', views.RequerimientoDocumentoCreateView.as_view(), name='requerimiento_documento_registrar'),
    path('requerimiento/documento/actualizar/<pk>/', views.RequerimientoDocumentoUpdateView.as_view(), name='requerimiento_documento_actualizar'),
    path('requerimiento/documento/eliminar/<pk>/', views.RequerimientoDocumentoDeleteView.as_view(), name='requerimiento_documento_eliminar'),
    path('requerimiento/documento/detalle/<pk>/', views.RequerimientoDocumentoDetailView.as_view(), name='requerimiento_documento_detalle'),
    path('requerimiento/documento/detalle-tabla/<pk>/', views.RequerimientoDocumentoDetailTabla, name='requerimiento_documento_detalle_tabla'),

    path('requerimiento/documento/detalle/crear/<pk>/', views.RequerimientoDocumentoDetalleCreateView.as_view(), name='requerimiento_documento_detalle_crear'),
    path('requerimiento/documento/detalle/actualizar/<pk>/', views.RequerimientoDocumentoDetalleUpdateView.as_view(), name='requerimiento_documento_detalle_actualizar'),
    path('requerimiento/documento/detalle/eliminar/<pk>/', views.RequerimientoDocumentoDetalleDeleteView.as_view(), name='requerimiento_documento_detalle_eliminar'),

    path('caja-chica/', views.CajaChicaListView.as_view(), name='caja_chica_inicio'),
    path('caja-chica-tabla/', views.CajaChicaTabla, name='caja_chica_tabla'),
    path('caja-chica/crear/', views.CajaChicaCreateView.as_view(), name='caja_chica_crear'),
    path('caja-chica/actualizar/<pk>/', views.CajaChicaUpdateView.as_view(), name='caja_chica_actualizar'),
    path('caja-chica/eliminar/<pk>/', views.CajaChicaDeleteView.as_view(), name='caja_chica_eliminar'),

]