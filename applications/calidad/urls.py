from django.urls import path
from .import views

app_name = 'calidad_app'

urlSeries = [

    path('serie/buscar/', views.SerieBuscarView.as_view(), name='serie_buscar'),
    path('serie/buscar/tabla/', views.SerieBuscarTabla, name='serie_buscar_tabla'),
    path('serie/ver/<pk>/', views.SerieDetailView.as_view(), name='serie_ver'),
    
    path('series/detalle/<pk>/', views.NotaControlCalidadStockDetalleView.as_view(), name='series_detalle'),
    path('series/detalle-tabla/<pk>/', views.NotaControlCalidadStockDetalleTabla, name='series_detalle_tabla'),
    path('series/detalle/bueno/registrar/<int:nota_control_calidad_stock_detalle_id>/', views.NotaControlCalidadStockBuenoCreateView.as_view(), name='series_detalle_bueno_registrar'),
    path('series/detalle/malo/registrar/<int:nota_control_calidad_stock_detalle_id>/', views.NotaControlCalidadStockAgregarMaloCreateView.as_view(), name='series_detalle_malo_registrar'),
    path('series/detalle/malo-sin-falla/registrar/<int:nota_control_calidad_stock_detalle_id>/', views.NotaControlCalidadStockAgregarMaloSinFallaCreateView.as_view(), name='series_detalle_malo_sin_falla_registrar'),
    path('series/detalle/solo-falla/registrar/<int:nota_control_calidad_stock_detalle_id>/', views.NotaControlCalidadStockActualizarFallasCreateView.as_view(), name='series_detalle_solo_falla_registrar'),
    path('series/detalle/malo/sin-serie/registrar/<int:nota_control_calidad_stock_detalle_id>/', views.NotaControlCalidadStockAgregarMaloSinSerieCreateView.as_view(), name='series_detalle_malo_sin_serie_registrar'),
    path('series/detalle/eliminar/<pk>/', views.NotaControlCalidadStockSerieCalidadDeleteView.as_view(), name='series_detalle_eliminar'),
    path('series/detalle/bueno/actualizar/<pk>/', views.NotaControlCalidadStockBuenoUpdateView.as_view(), name='series_detalle_bueno_actualizar'),
    path('series/detalle/malo/actualizar/<pk>/', views.NotaControlCalidadStockMaloUpdateView.as_view(), name='series_detalle_malo_actualizar'),
    path('series/detalle/malo/sin-serie/actualizar/<pk>/', views.NotaControlCalidadStockMaloSinSerieUpdateView.as_view(), name='series_detalle_malo_sin_serie_actualizar'),

    path('series/registrar-serie-antigua/<int:id_serie_antigua>/', views.RegistrarSerieAntiguaView.as_view(), name='series_registrar_serie_antigua'),
]

urlNotaControlCalidadStock = [

    path('nota-control-calidad-stock/', views.NotaControlCalidadStockListView.as_view(), name='nota_control_calidad_stock_inicio'),
    path('nota-control-calidad-stock-tabla/', views.NotaControlCalidadStockTabla, name='nota_control_calidad_stock_tabla'),
    path('nota-control-calidad-stock/registrar/', views.NotaControlCalidadStockCreateView.as_view(), name='nota_control_calidad_stock_registrar'),
    path('nota-control-calidad-stock/registrar-transformacion/', views.NotaControlCalidadStockTransformacionProductosCreateView.as_view(), name='nota_control_calidad_stock_registrar_transformacion'),
    path('nota-control-calidad-stock/anular/<pk>/', views.NotaControlCalidadStockDeleteView.as_view(), name='nota_control_calidad_stock_anular'),
    path('nota-control-calidad-stock/concluir/<pk>/', views.NotaControlCalidadStockConcluirView.as_view(), name='nota_control_calidad_stock_concluir'),
    path('nota-control-calidad-stock/registrar/series/<pk>/', views.NotaControlCalidadStockRegistrarSeriesView.as_view(), name='nota_control_calidad_stock_registrar_series'),
    path('nota-control-calidad-stock/detalle/<pk>/', views.NotaControlCalidadStockDetailView.as_view(), name='nota_control_calidad_stock_detalle'),
    path('nota-control-calidad-stock/detalle-tabla/<pk>/', views.NotaControlCalidadStockDetailTabla, name='nota_control_calidad_stock_detalle_tabla'),
    path('nota-control-calidad-stock/detalle/registrar/<int:nota_control_calidad_stock_id>/', views.NotaControlCalidadStockDetalleCreateView.as_view(), name='nota_control_calidad_stock_detalle_registrar'),
    path('nota-control-calidad-stock/detalle/actualizar/<pk>/', views.NotaControlCalidadStockDetalleUpdateView.as_view(), name='nota_control_calidad_stock_detalle_actualizar'),
    path('nota-control-calidad-stock/detalle/eliminar/<pk>/', views.NotaControlCalidadStockDetalleDeleteView.as_view(), name='nota_control_calidad_stock_detalle_eliminar'),
    path('nota-control-calidad-stock/series/pdf/<pk>/', views.NotaControlCalidadStockSeriesPdf.as_view(), name='nota_control_calidad_stock_series_pdf'),
]

urlConsumoInterno = [

    path('solicitud-consumo-interno/', views.SolicitudConsumoInternoListView.as_view(), name='solicitud_consumo_interno_inicio'),
    path('solicitud-consumo-interno-tabla/', views.SolicitudConsumoInternoTabla, name='solicitud_consumo_interno_tabla'),
    path('solicitud-consumo-interno/registrar/', views.SolicitudConsumoInternoCreateView.as_view(), name='solicitud_consumo_interno_registrar'),
    path('solicitud-consumo-interno/actualizar/<pk>', views.SolicitudConsumoInternoUpdateView.as_view(), name='solicitud_consumo_interno_actualizar'),
    path('solicitud-consumo-interno/dar-baja/<pk>/', views.SolicitudConsumoInternoDeleteView.as_view(), name='solicitud_consumo_interno_darbaja'),
    path('solicitud-consumo-interno/concluir/<pk>/', views.SolicitudConsumoInternoConcluirView.as_view(), name='solicitud_consumo_interno_concluir'),
    path('solicitud-consumo-interno/detalle/<pk>/', views.SolicitudConsumoInternoDetailView.as_view(), name='solicitud_consumo_interno_detalle'),
    path('solicitud-consumo-interno/detalle-tabla/<pk>/', views.SolicitudConsumoInternoDetailTabla, name='solicitud_consumo_interno_detalle_tabla'),
    path('solicitud-consumo-interno/detalle/registrar/<int:solicitud_consumo_id>/', views.SolicitudConsumoInternoDetalleCreateView.as_view(), name='solicitud_consumo_interno_detalle_registrar'),
    path('solicitud-consumo-interno/detalle/actualizar/<pk>/', views.SolicitudConsumoInternoDetalleUpdateView.as_view(), name='solicitud_consumo_interno_detalle_actualizar'),
    path('solicitud-consumo-interno/detalle/eliminar/<pk>/', views.SolicitudConsumoInternoDetalleDeleteView.as_view(), name='solicitud_consumo_interno_detalle_eliminar'),
    # path('solicitud-consumo-interno/registrar/series/<pk>/', views.SolicitudConsumoInternoRegistrarSeriesView.as_view(), name='solicitud_consumo_interno_registrar_series'),
    # path('solicitud-consumo-interno/series/pdf/<pk>/', views.SolicitudConsumoInternoSeriesPdf.as_view(), name='solicitud_consumo_interno_series_pdf'),
    
    path('solicitud-consumo-interno/material-unidad/<pk>/', views.MaterialUnidadView, name='material_unidad'),
]

urlConsumoInternoSeries = [

    path('solicitud-consumo/validar-series/detalle/<pk>/', views.ValidarSeriesSolicitudConsumoDetailView.as_view(), name='solicitud_consumo_validar_series_detalle'),
    path('solicitud-consumo/validar-series/detalle-tabla/<pk>/', views.ValidarSeriesSolicitudConsumoDetailTabla, name='solicitud_consumo_validar_series_detalle_tabla'),
    path('solicitud-consumo/validar-series-detalle/eliminar/<pk>/', views.ValidarSeriesSolicitudConsumoDetalleDeleteView.as_view(), name='solicitud_consumo_validar_series_detalle_eliminar'),
]

urlAprobacionConsumoInterno = [
    path('aprobacion-consumo-interno/', views.AprobacionConsumoInternoListView.as_view(), name='aprobacion_consumo_interno_inicio'),
    path('aprobacion-consumo-interno-tabla/', views.AprobacionConsumoInternoTabla, name='aprobacion_consumo_interno_tabla'),
    path('aprobacion-consumo-interno/registrar/', views.AprobacionConsumoInternoCreateView.as_view(), name='aprobacion_consumo_interno_registrar'),
    path('aprobacion-consumo-interno/actualizar/<pk>', views.AprobacionConsumoInternoUpdateView.as_view(), name='aprobacion_consumo_interno_actualizar'),
    path('aprobacion-consumo-interno/detalle/<pk>', views.AprobacionConsumoInternoDetailView.as_view(), name='aprobacion_consumo_interno_detalle'),
    path('aprobacion-consumo-interno/detalle-tabla/<pk>/', views.AprobacionConsumoInternoDetailTabla, name='aprobacion_consumo_interno_detalle_tabla'),
    path('aprobacion-consumo-interno/aprobar/<pk>/', views.AprobacionConsumoInternoAprobarView.as_view(), name='aprobacion_consumo_interno_aprobar'),
    path('aprobacion-consumo-interno/rechazar/<pk>/', views.AprobacionConsumoInternoRechazarView.as_view(), name='aprobacion_consumo_interno_rechazar'),
    # path('aprobacion-consumo-interno/dar-baja/<pk>/', views.AprobacionConsumoInternoDeleteView.as_view(), name='aprobacion_consumo_interno_darbaja'),
]

urlReparacionMaterial = [
    path('reparacion-material/', views.ReparacionMaterialListView.as_view(), name='reparacion_material_inicio'),
    path('reparacion-material-tabla/', views.ReparacionMaterialTabla, name='reparacion_material_tabla'),
    path('reparacion-material/registrar/', views.ReparacionMaterialCreateView.as_view(), name='reparacion_material_registrar'),
    path('reparacion-material/actualizar/<pk>', views.ReparacionMaterialUpdateView.as_view(), name='reparacion_material_actualizar'),
    path('reparacion-material/dar-baja/<pk>/', views.ReparacionMaterialDeleteView.as_view(), name='reparacion_material_dar_baja'),
    path('reparacion-material/concluir/<pk>/', views.ReparacionMaterialConcluirView.as_view(), name='reparacion_material_concluir'),
    path('reparacion-material/detalle/<pk>/', views.ReparacionMaterialDetailView.as_view(), name='reparacion_material_detalle'),
    path('reparacion-material/detalle-tabla/<pk>/', views.ReparacionMaterialDetailTabla, name='reparacion_material_detalle_tabla'),
    path('reparacion-material/detalle/registrar/<int:reparacion_id>/', views.ReparacionMaterialDetalleCreateView.as_view(), name='reparacion_material_detalle_registrar'),
    path('reparacion-material/detalle/actualizar/<pk>/', views.ReparacionMaterialDetalleUpdateView.as_view(), name='reparacion_material_detalle_actualizar'),
    path('reparacion-material/detalle/eliminar/<pk>/', views.ReparacionMaterialDetalleDeleteView.as_view(), name='reparacion_material_detalle_eliminar'),
]

urlReparacionMaterialSeries = [

    path('reparacion-material/validar-series/detalle/<pk>/', views.ValidarSeriesReparacionMaterialDetailView.as_view(), name='reparacion_material_validar_series_detalle'),
    path('reparacion-material/validar-series/detalle-tabla/<pk>/', views.ValidarSeriesReparacionMaterialDetailTabla, name='reparacion_material_validar_series_detalle_tabla'),
    path('reparacion-material/validar-series-detalle/actualizar/<pk>/', views.ValidarSeriesReparacionMaterialDetalleUpdateView.as_view(), name='reparacion_material_validar_series_detalle_actualizar'),
    path('reparacion-material/validar-series-detalle/actualizar-serie/<pk>/', views.ValidarSeriesReparacionMaterialDetalleCambioSerieView.as_view(), name='reparacion_material_validar_series_detalle_actualizar_serie'),
    path('reparacion-material/validar-series-detalle/eliminar/<pk>/', views.ValidarSeriesReparacionMaterialDetalleDeleteView.as_view(), name='reparacion_material_validar_series_detalle_eliminar'),
]

urlFallaMaterial = [

    path('falla-material/',views.FallaMaterialTemplateView.as_view(),name='falla_material'),
    path('falla-material/detalle/<pk>/', views.FallaMaterialDetailView.as_view(), name='falla_material_detalle'),
    path('falla-material/detalle-tabla/<pk>/', views.FallaMaterialDetailTabla, name='falla_material_detalle_tabla'),    
    path('falla-material/detalle/registrar/<int:subfamilia_id>/', views.FallaMaterialCreateView.as_view(), name='falla_material_detalle_registrar'),
    path('falla-material/detalle/actualizar/<pk>/', views.FallaMaterialUpdateView.as_view(), name='falla_material_detalle_actualizar'),
    path('falla-material/detalle/modal/<pk>/', views.FallaMaterialModalDetailView.as_view(), name='falla_material_detalle_modal'),
    path('falla-material/detalle/eliminar/<pk>/', views.FallaMaterialDeleteView.as_view(), name='falla_material_detalle_eliminar'),
]

urlSolucionMaterial = [

    # path('solucion-material/',views.SolucionMaterialTemplateView.as_view(),name='solucion_material'),
    path('solucion-material/detalle/<pk>/', views.SolucionMaterialDetailView.as_view(), name='solucion_material_detalle'),
    path('solucion-material/detalle-tabla/<pk>/', views.SolucionMaterialDetailTabla, name='solucion_material_detalle_tabla'),    
    path('solucion-material/detalle/registrar/<int:falla_material_id>/', views.SolucionMaterialCreateView.as_view(), name='solucion_material_detalle_registrar'),
    path('solucion-material/general/registrar/<int:subfamilia_id>/', views.SolucionMaterialGeneralCreateView.as_view(), name='solucion_material_general_registrar'),
    path('solucion-material/detalle/actualizar/<pk>/', views.SolucionMaterialUpdateView.as_view(), name='solucion_material_detalle_actualizar'),
    path('solucion-material/detalle/modal/<pk>/', views.SolucionMaterialModalDetailView.as_view(), name='solucion_material_detalle_modal'),
    path('solucion-material/detalle/eliminar/<pk>/', views.SolucionMaterialDeleteView.as_view(), name='solucion_material_detalle_eliminar'),
]

urlTransformacionProductos = [
    path('transformacion-productos/', views.TransformacionProductosListView.as_view(), name='transformacion_productos_inicio'),
    path('transformacion-productos-tabla/', views.TransformacionProductosTabla, name='transformacion_productos_tabla'),
    path('transformacion-productos/registrar/', views.TransformacionProductosCreateView.as_view(), name='transformacion_productos_registrar'),
    path('transformacion-productos/actualizar/<pk>', views.TransformacionProductosUpdateView.as_view(), name='transformacion_productos_actualizar'),
    path('transformacion-productos/eliminar/<pk>', views.TransformacionProductosDeleteView.as_view(), name='transformacion_productos_eliminar'),
    path('transformacion-productos/concluir/<pk>/', views.TransformacionProductosConcluirView.as_view(), name='transformacion_productos_concluir'),
    path('transformacion-productos/detalle/<pk>', views.TransformacionProductosDetailView.as_view(), name='transformacion_productos_detalle'),
    path('transformacion-productos/detalle-tabla/<pk>/', views.TransformacionProductosDetailTabla, name='transformacion_productos_detalle_tabla'),

    path('entrada-transformacion-productos/registrar/<int:transformacion_productos_id>/', views.EntradaTransformacionProductosCreateView.as_view(), name='entrada_transformacion_productos_registrar'),
    path('entrada-transformacion-productos/actualizar/<pk>/', views.EntradaTransformacionProductosUpdateView.as_view(), name='entrada_transformacion_productos_actualizar'),
    path('entrada-transformacion-productos/eliminar/<pk>/', views.EntradaTransformacionProductosDeleteView.as_view(), name='entrada_transformacion_productos_eliminar'),
    path('entrada-transformacion-productos/validar-series/detalle/<pk>/', views.ValidarSeriesEntradaTransformacionProductosDetailView.as_view(), name='entrada_transformacion_productos_validar_series_detalle'),
    path('entrada-transformacion-productos/validar-series/detalle-tabla/<pk>/', views.ValidarSeriesEntradaTransformacionProductosDetailTabla, name='entrada_transformacion_productos_validar_series_detalle_tabla'),
    path('entrada-transformacion-productos/validar-series/detalle/eliminar/<pk>/', views.ValidarSeriesEntradaTransformacionProductosDetalleDeleteView.as_view(), name='entrada_transformacion_productos_validar_series_detalle_eliminar'),

    path('salida-transformacion-productos/registrar/<int:transformacion_productos_id>/', views.SalidaTransformacionProductosCreateView.as_view(), name='salida_transformacion_productos_registrar'),
    path('salida-transformacion-productos/actualizar/<pk>/', views.SalidaTransformacionProductosUpdateView.as_view(), name='salida_transformacion_productos_actualizar'),
    path('salida-transformacion-productos/eliminar/<pk>/', views.SalidaTransformacionProductosDeleteView.as_view(), name='salida_transformacion_productos_eliminar'),
    path('salida-transformacion-productos/validar-series/detalle/<pk>/', views.ValidarSeriesSalidaTransformacionProductosDetailView.as_view(), name='salida_transformacion_productos_validar_series_detalle'),
    path('salida-transformacion-productos/validar-series/detalle-tabla/<pk>/', views.ValidarSeriesSalidaTransformacionProductosDetailTabla, name='salida_transformacion_productos_validar_series_detalle_tabla'),
    path('salida-transformacion-productos/validar-series/detalle/eliminar/<pk>/', views.ValidarSeriesSalidaTransformacionProductosDetalleDeleteView.as_view(), name='salida_transformacion_productos_validar_series_detalle_eliminar'),
]

urlpatterns = urlFallaMaterial + urlNotaControlCalidadStock + urlSeries + urlConsumoInterno + urlConsumoInternoSeries + urlAprobacionConsumoInterno + urlReparacionMaterial + urlReparacionMaterialSeries + urlSolucionMaterial + urlTransformacionProductos
