from django.urls import path
from .import views

app_name = 'caja_chica_app'

url_requerimiento = [
    path('requerimiento/', views.RequerimientoListView.as_view(), name='requerimiento_inicio'),
    path('requerimiento-tabla/', views.RequerimientoTabla, name='requerimiento_tabla'),
    path('requerimiento-recibido/', views.RequerimientoRecibidoListView.as_view(), name='requerimiento_recibido_inicio'),
    path('requerimiento-recibido-tabla/', views.RequerimientoRecibidoTabla, name='requerimiento_recibido_tabla'),
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
    path('requerimiento/vouchers/<pk>/', views.RequerimientoVouchersView.as_view(), name='requerimiento_vouchers'),

    path('requerimiento/vuelto-extra/agregar/<int:requerimiento_id>/', views.RequerimientoVueltoExtraCreateView.as_view(), name='requerimiento_vuelto_extra_agregar'),
    path('requerimiento/vuelto-extra/editar/<pk>/', views.RequerimientoVueltoExtraUpdateView.as_view(), name='requerimiento_vuelto_extra_editar'),
    path('requerimiento/vuelto-extra/eliminar/<pk>/', views.RequerimientoVueltoExtraDeleteView.as_view(), name='requerimiento_vuelto_extra_eliminar'),

    path('requerimiento/documento/registrar/<int:requerimiento_id>/', views.RequerimientoDocumentoCreateView.as_view(), name='requerimiento_documento_registrar'),
    path('requerimiento/documento/actualizar/<pk>/', views.RequerimientoDocumentoUpdateView.as_view(), name='requerimiento_documento_actualizar'),
    path('requerimiento/documento/eliminar/<pk>/', views.RequerimientoDocumentoDeleteView.as_view(), name='requerimiento_documento_eliminar'),
    path('requerimiento/documento/detalle/<pk>/', views.RequerimientoDocumentoDetailView.as_view(), name='requerimiento_documento_detalle'),
    path('requerimiento/documento/detalle-tabla/<pk>/', views.RequerimientoDocumentoDetailTabla, name='requerimiento_documento_detalle_tabla'),

    path('requerimiento/documento/detalle/crear/<pk>/', views.RequerimientoDocumentoDetalleCreateView.as_view(), name='requerimiento_documento_detalle_crear'),
    path('requerimiento/documento/detalle/actualizar/<pk>/', views.RequerimientoDocumentoDetalleUpdateView.as_view(), name='requerimiento_documento_detalle_actualizar'),
    path('requerimiento/documento/detalle/eliminar/<pk>/', views.RequerimientoDocumentoDetalleDeleteView.as_view(), name='requerimiento_documento_detalle_eliminar'),
]

url_caja_chica = [
    path('caja-chica/', views.CajaChicaListView.as_view(), name='caja_chica_inicio'),
    path('caja-chica-tabla/', views.CajaChicaTabla, name='caja_chica_tabla'),
    path('caja-chica/crear/', views.CajaChicaCreateView.as_view(), name='caja_chica_crear'),
    path('caja-chica/actualizar/<pk>/', views.CajaChicaUpdateView.as_view(), name='caja_chica_actualizar'),
    path('caja-chica/eliminar/<pk>/', views.CajaChicaDeleteView.as_view(), name='caja_chica_eliminar'),
    path('caja-chica/detalle/<pk>/', views.CajaChicaDetalleView.as_view(), name='caja_chica_detalle'),
    path('caja-chica/detalle-tabla/<pk>/', views.CajaChicaDetalleTabla, name='caja_chica_detalle_tabla'),
    path('caja_chica/pdf/<pk>/', views.CajaChicaPdfView.as_view(), name='caja_chica_pdf'),
    path('caja-chica/cerrar/<pk>/', views.CajaChicaCierreView.as_view(), name='caja_chica_cerrar'), 
    path('caja-chica/abrir/<pk>/', views.CajaChicaAbrirView.as_view(), name='caja_chica_abrir'), 

    path('caja-chica/recibo/<int:cajachica_id>/', views.CajaChicaReciboCreateView.as_view(), name='caja_chica_recibo'),
    path('caja-chica/recibo/eliminar/<pk>/<int:cajachica_id>/', views.CajaChicaReciboDeleteView.as_view(), name='caja_chica_recibo_eliminar'),
    path('caja-chica/recibo/pendiente/<pk>/<int:cajachica_id>/', views.CajaChicaReciboPendienteView.as_view(), name='caja_chica_recibo_pendiente'),
    path('caja-chica/recibo/actualizar/<pk>/<int:cajachica_id>/', views.CajaChicaReciboUpdateView.as_view(), name='caja_chica_recibo_actualizar'),

    path('caja-chica/detalle/recibo-servicio/agregar/<int:cajachica_id>/', views.CajaChicaReciboServicioAgregarView.as_view(), name='caja_chica_recibo_servicio_agregar'),
    path('caja-chica/detalle/recibo-servicio/actualizar/<pk>/<int:cajachica_id>/', views.CajaChicaReciboServicioUpdateView.as_view() , name='caja_chica_recibo_servicio_actualizar'),
    # path('caja-chica/detalle/recibo-servicio/remover/<pk>/<int:cajachica_id>/', views.ChequeReciboServicioRemoverView.as_view(), name='caja_chica_recibo_servicio_remover'),

    path('prestamo/', views.CajaChicaPrestamoListView.as_view(), name='prestamo_inicio'),
    path('prestamo-tabla/', views.CajaChicaPrestamoTabla, name='prestamo_tabla'),
    path('prestamo/crear/', views.CajaChicaPrestamoCreateView.as_view(), name='prestamo_crear'),
    path('prestamo/actualizar/<pk>/', views.CajaChicaPrestamoUpdateView.as_view(), name='prestamo_actualizar'),
    path('prestamo/eliminar/<pk>/', views.CajaChicaPrestamoDeleteView.as_view(), name='prestamo_eliminar'),

    path('recibo/', views.ReciboCajaChicaListView.as_view(), name='recibo_inicio'),
    path('recibo-tabla/', views.ReciboCajaChicaTabla, name='recibo_tabla'),
    path('recibo/crear/', views.ReciboCajaChicaCreateView.as_view(), name='recibo_crear'),
    path('recibo/actualizar/<pk>/', views.ReciboCajaChicaUpdateView.as_view(), name='recibo_actualizar'),
    path('recibo/eliminar/<pk>/', views.ReciboCajaChicaDeleteView.as_view(), name='recibo_eliminar'),
]

urlpatterns = url_requerimiento + url_caja_chica