from django.urls import path
from . import views

app_name = 'logistica_app'

urlSeries = [

    path('validar-series/detalle/<pk>/', views.ValidarSeriesNotaSalidaDetailView.as_view(), name='validar_series_detalle'),
    path('validar-series/detalle-tabla/<pk>/', views.ValidarSeriesNotaSalidaDetailTabla, name='validar_series_detalle_tabla'),
    path('validar-series-detalle/eliminar/<pk>/', views.ValidarSeriesNotaSalidaDetalleDeleteView.as_view(), name='validar_series_nota_salida_detalle_eliminar'),
]

urlNotaSalida = [
    path('nota-salida/', views.NotaSalidaListView.as_view(), name='nota_salida_inicio'),
    path('nota-salida/<int:id_solicitud_prestamo>/', views.NotaSalidaListView.as_view(), name='nota_salida_inicio'),
    path('nota-salida/confirmacion/<int:id_confirmacion>/', views.NotaSalidaListView.as_view(), name='nota_salida_confirmacion'),
    path('nota-salida-tabla/', views.NotaSalidaTabla, name='nota_salida_tabla'),
    path('nota-salida/actualizar/<pk>', views.NotaSalidaUpdateView.as_view(), name='nota_salida_actualizar'),
    path('nota-salida/concluir/<pk>/', views.NotaSalidaConcluirView.as_view(), name='nota_salida_concluir'),
    path('nota-salida/anular/<pk>/', views.NotaSalidaAnularView.as_view(), name='nota_salida_anular'),
    path('nota-salida/detalle/<pk>/', views.NotaSalidaDetailView.as_view(), name='nota_salida_detalle'),
    path('nota-salida/detalle-tabla/<pk>/', views.NotaSalidaDetailTabla, name='nota_salida_detalle_tabla'),
    path('nota-salida-detalle/registrar/<int:nota_salida_id>/', views.NotaSalidaDetalleCreateView.as_view(), name='nota_salida_detalle_registrar'),
    path('nota-salida-detalle/actualizar/<pk>/', views.NotaSalidaDetalleUpdateView.as_view(), name='nota_salida_detalle_actualizar'),
    path('nota-salida-detalle/eliminar/<pk>/', views.NotaSalidaDetalleDeleteView.as_view(), name='nota_salida_detalle_eliminar'),
    path('nota-salida-detalle/generar-despacho/<pk>/', views.NotaSalidaGenerarDespachoView.as_view(), name='nota_salida_generar_despacho'),
    
    path('almacen/<str:id_sede>/', views.AlmacenView, name='almacen'),
    path('nota-salida-series/pdf/<pk>/', views.NotaSalidaSeriesPdf.as_view(), name='nota_salida_series_pdf'),
]

urlDespacho = [
    path('despacho/', views.DespachoListView.as_view(), name='despacho_inicio'),
    path('despacho/<int:id_nota_salida>/', views.DespachoListView.as_view(), name='despacho_inicio'),
    path('despacho-tabla/', views.DespachoTabla, name='despacho_tabla'),
    path('despacho/actualizar/<pk>', views.DespachoUpdateView.as_view(), name='despacho_actualizar'),
    path('despacho/concluir/<pk>/', views.DespachoConcluirView.as_view(), name='despacho_concluir'),
    path('despacho/finalizar-sin-guia/<pk>/', views.DespachoFinalizarSinGuiaView.as_view(), name='despacho_finalizar_sin_guia'),
    path('despacho/anular/<pk>/', views.DespachoAnularView.as_view(), name='despacho_anular'),
    path('despacho/corregir/<pk>/', views.DespachoCorregirView.as_view(), name='despacho_corregir'),
    path('despacho/detalle/<pk>/', views.DespachoDetailView.as_view(), name='despacho_detalle'),
    path('despacho/detalle-tabla/<pk>/', views.DespachoDetailTabla, name='despacho_detalle_tabla'),
    path('despacho/generar-guia/<pk>/', views.DespachoGenerarGuiaView.as_view(), name='despacho_generar_guia'),

    path('despacho/imagen/agregar/<int:id_despacho>/', views.ImagenesDespachoCreateView.as_view(), name='despacho_imagen_agregar'),
    path('despacho/imagen/eliminar/<pk>/', views.ImagenesDespachoDeleteView.as_view(), name='despacho_imagen_eliminar'),
]

urlInventarioMateriales = [
    path('inventario-materiales/', views.InventarioMaterialesListView.as_view(), name='inventario_materiales_inicio'),
    path('inventario-materiales-tabla/', views.InventarioMaterialesTabla, name='inventario_materiales_tabla'),
    path('inventario-materiales/registrar/', views.InventarioMaterialesCreateView.as_view(), name='inventario_materiales_registrar'),
    path('inventario-materiales/actualizar/<pk>', views.InventarioMaterialesUpdateView.as_view(), name='inventario_materiales_actualizar'),
    path('inventario-materiales/concluir/<pk>/', views.InventarioMaterialesConcluirView.as_view(), name='inventario_materiales_concluir'),
    path('inventario-materiales/detalle/<pk>/', views.InventarioMaterialesDetailView.as_view(), name='inventario_materiales_detalle'),
    path('inventario-materiales/detalle-tabla/<pk>/', views.InventarioMaterialesDetailTabla, name='inventario_materiales_detalle_tabla'),
    path('inventario-materiales/detalle/registrar/<int:inventario_materiales_id>/', views.InventarioMaterialesDetalleCreateView.as_view(), name='inventario_materiales_detalle_registrar'),
    path('inventario-materiales/detalle/actualizar/<pk>/', views.InventarioMaterialesDetalleUpdateView.as_view(), name='inventario_materiales_detalle_actualizar'),
    path('inventario-materiales/detalle/eliminar/<pk>/', views.InventarioMaterialesDetalleDeleteView.as_view(), name='inventario_materiales_detalle_eliminar'),
]

urlAjusteInventarioMateriales = [
    path('ajuste-inventario-materiales/', views.AjusteInventarioMaterialesListView.as_view(), name='ajuste_inventario_materiales_inicio'),
    path('ajuste-inventario-materiales-tabla/', views.AjusteInventarioMaterialesTabla, name='ajuste_inventario_materiales_tabla'),
    path('ajuste-inventario-materiales/actualizar/<pk>', views.AjusteInventarioMaterialesUpdateView.as_view(), name='ajuste_inventario_materiales_actualizar'),
    path('ajuste-inventario-materiales/concluir/<pk>/', views.AjusteInventarioMaterialesConcluirView.as_view(), name='ajuste_inventario_materiales_concluir'),
    path('ajuste-inventario-materiales/detalle/<pk>/', views.AjusteInventarioMaterialesDetailView.as_view(), name='ajuste_inventario_materiales_detalle'),
    path('ajuste-inventario-materiales/detalle-tabla/<pk>/', views.AjusteInventarioMaterialesDetailTabla, name='ajuste_inventario_materiales_detalle_tabla'),
    path('ajuste-inventario-materiales/detalle/registrar/<int:ajuste_inventario_materiales_id>/', views.AjusteInventarioMaterialesDetalleCreateView.as_view(), name='ajuste_inventario_materiales_detalle_registrar'),
    # path('ajuste-inventario-materiales/detalle/actualizar/<pk>/', views.AjusteInventarioMaterialesDetalleUpdateView.as_view(), name='ajuste_inventario_materiales_detalle_actualizar'),
    path('ajuste-inventario-materiales/detalle/eliminar/<pk>/', views.AjusteInventarioMaterialesDetalleDeleteView.as_view(), name='ajuste_inventario_materiales_detalle_eliminar'),
]

urlDevolucionPrestamo = [
    path('devolucion-prestamo/actualizar/<pk>', views.DevolucionPrestamoMaterialesUpdateView.as_view(), name='devolucion_prestamo_actualizar'),
    path('devolucion-prestamo/concluir/<pk>/', views.DevolucionPrestamoMaterialesConcluirView.as_view(), name='devolucion_prestamo_concluir'),
    path('devolucion-prestamo/detalle/<pk>/', views.DevolucionPrestamoMaterialesDetailView.as_view(), name='devolucion_prestamo_detalle'),
    path('devolucion-prestamo/detalle-tabla/<pk>/', views.DevolucionPrestamoMaterialesDetailTabla, name='devolucion_prestamo_detalle_tabla'),
    path('devolucion-prestamo/detalle/actualizar/<pk>', views.DevolucionPrestamoMaterialesDetalleUpdateView.as_view(), name='devolucion_prestamo_detalle_actualizar'),
    path('devolucion-prestamo-series/pdf/<pk>/', views.DevolucionPrestamoMaterialesSeriesPdf.as_view(), name='devolucion_prestamo_series_pdf'),

    path('validar-series/devolucion-prestamo/detalle/<pk>/', views.ValidarSeriesDevolucionPrestamoMaterialesDetailView.as_view(), name='validar_series_devolucion_prestamo_detalle'),
    path('validar-series/devolucion-prestamo/detalle-tabla/<pk>/', views.ValidarSeriesDevolucionPrestamoMaterialesDetailTabla, name='validar_series_devolucion_prestamo_detalle_tabla'),
    path('validar-series/devolucion-prestamo/detalle-eliminar/<pk>/', views.ValidarSeriesDevolucionPrestamoMaterialesDetalleDeleteView.as_view(), name='validar_series_devolucion_prestamo_detalle_eliminar'),

]

urlpatterns = [
    path('solicitud-prestamo-materiales/', views.SolicitudPrestamoMaterialesListView.as_view(), name='solicitud_prestamo_materiales_inicio'),
    path('solicitud-prestamo-materiales-tabla/', views.SolicitudPrestamoMaterialesTabla, name='solicitud_prestamo_materiales_tabla'),
    path('solicitud-prestamo-materiales/registrar/', views.SolicitudPrestamoMaterialesCreateView.as_view(), name='solicitud_prestamo_materiales_registrar'),
    path('solicitud-prestamo-materiales/actualizar/<pk>', views.SolicitudPrestamoMaterialesUpdateView.as_view(), name='solicitud_prestamo_materiales_actualizar'),
    path('solicitud-prestamo-materiales/finalizar/<pk>/', views.SolicitudPrestamoMaterialesFinalizarView.as_view(), name='solicitud_prestamo_materiales_finalizar'),
    path('solicitud-prestamo-materiales/confirmar/<pk>/', views.SolicitudPrestamoMaterialesConfirmarView.as_view(), name='solicitud_prestamo_materiales_confirmar'),
    path('solicitud-prestamo-materiales/anular/<pk>/', views.SolicitudPrestamoMaterialesAnularView.as_view(), name='solicitud_prestamo_materiales_anular'),
    path('solicitud-prestamo-materiales/detalle/<pk>/', views.SolicitudPrestamoMaterialesDetailView.as_view(), name='solicitud_prestamo_materiales_detalle'),
    path('solicitud-prestamo-materiales/detalle-tabla/<pk>/', views.SolicitudPrestamoMaterialesDetailTabla, name='solicitud_prestamo_materiales_detalle_tabla'),
    path('solicitud-prestamo-materiales-detalle/registrar/<int:solicitud_prestamo_materiales_id>/', views.SolicitudPrestamoMaterialesDetalleCreateView.as_view(), name='solicitud_prestamo_materiales_detalle_registrar'),
    path('solicitud-prestamo-materiales-detalle/imprimir/<pk>/', views.SolicitudPrestamoMaterialesDetalleImprimirView.as_view(), name='solicitud_prestamo_materiales_detalle_imprimir'),
    path('solicitud-prestamo-materiales-detalle/actualizar/<pk>/', views.SolicitudPrestamoMaterialesDetalleUpdateView.as_view(), name='solicitud_prestamo_materiales_detalle_actualizar'),
    path('solicitud-prestamo-materiales-detalle/eliminar/<pk>/', views.SolicitudPrestamoMaterialesDetalleDeleteView.as_view(), name='solicitud_prestamo_materiales_detalle_eliminar'),
    path('solicitud-prestamo-materiales-detalle/archivo/agregar/<int:solicitud_prestamo_materiales_id>/', views.DocumentoSolicitudPrestamoMaterialesCreateView.as_view(), name='solicitud_prestamo_materiales_documento_agregar'),
    path('solicitud-prestamo-materiales-detalle/archivo/eliminar/<pk>/', views.DocumentoSolicitudPrestamoMaterialesDeleteView.as_view(), name='solicitud_prestamo_materiales_documento_eliminar'),
    path('solicitud-prestamo-materiales-detalle/generar-nota-salida/<pk>/', views.SolicitudPrestamoMaterialesGenerarNotaSalidaView.as_view(), name='solicitud_prestamo__materiales_generar_nota_salida'),
    path('solicitud-prestamo-materiales-detalle/generar-devolucion-prestamo/<pk>/', views.SolicitudPrestamoMaterialesGenerarDevolucionPrestamoMaterialesView.as_view(), name='solicitud_prestamo__materiales_generar_devolucion_prestamo'),
] + urlSeries + urlNotaSalida + urlDespacho + urlInventarioMateriales + urlAjusteInventarioMateriales + urlDevolucionPrestamo