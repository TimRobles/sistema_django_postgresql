from django.urls import path
from . import views

app_name='merchandising_app'

urlInventarioMerchandising = [
    path('inventario-merchandising/', views.InventarioMerchandisingListView.as_view(), name='inventario_merchandising_inicio'),
    path('inventario-merchandising-tabla/', views.InventarioMerchandisingTabla, name='inventario_merchandising_tabla'),
    path('inventario-merchandising/registrar/', views.InventarioMerchandisingCreateView.as_view(), name='inventario_merchandising_registrar'),
    path('inventario-merchandising/actualizar/<pk>', views.InventarioMerchandisingUpdateView.as_view(), name='inventario_merchandising_actualizar'),
    path('inventario-merchandising/concluir/<pk>/', views.InventarioMerchandisingConcluirView.as_view(), name='inventario_merchandising_concluir'),
    path('inventario-merchandising/detalle/<pk>/', views.InventarioMerchandisingDetailView.as_view(), name='inventario_merchandising_detalle'),
    path('inventario-merchandising/detalle-tabla/<pk>/', views.InventarioMerchandisingDetailTabla, name='inventario_merchandising_detalle_tabla'),
    path('inventario-merchandising/detalle/registrar/<int:inventario_merchandising_id>/', views.InventarioMerchandisingDetalleCreateView.as_view(), name='inventario_merchandising_detalle_registrar'),
    path('inventario-merchandising/detalle/actualizar/<pk>/', views.InventarioMerchandisingDetalleUpdateView.as_view(), name='inventario_merchandising_detalle_actualizar'),
    path('inventario-merchandising/detalle/eliminar/<pk>/', views.InventarioMerchandisingDetalleDeleteView.as_view(), name='inventario_merchandising_detalle_eliminar'),
]

urlAjusteInventarioMerchandising = [
    path('ajuste-inventario-merchandising/', views.AjusteInventarioMerchandisingListView.as_view(), name='ajuste_inventario_merchandising_inicio'),
    path('ajuste-inventario-merchandising-tabla/', views.AjusteInventarioMerchandisingTabla, name='ajuste_inventario_merchandising_tabla'),
    path('ajuste-inventario-merchandising/actualizar/<pk>', views.AjusteInventarioMerchandisingUpdateView.as_view(), name='ajuste_inventario_merchandising_actualizar'),
    path('ajuste-inventario-merchandising/concluir/<pk>/', views.AjusteInventarioMerchandisingConcluirView.as_view(), name='ajuste_inventario_merchandising_concluir'),
    path('ajuste-inventario-merchandising/detalle/<pk>/', views.AjusteInventarioMerchandisingDetailView.as_view(), name='ajuste_inventario_merchandising_detalle'),
    path('ajuste-inventario-merchandising/detalle-tabla/<pk>/', views.AjusteInventarioMerchandisingDetailTabla, name='ajuste_inventario_merchandising_detalle_tabla'),
    path('ajuste-inventario-merchandising/detalle/registrar/<int:ajuste_inventario_merchandising_id>/', views.AjusteInventarioMerchandisingDetalleCreateView.as_view(), name='ajuste_inventario_merchandising_detalle_registrar'),
    # path('ajuste-inventario-merchandising/detalle/actualizar/<pk>/', views.AjusteInventarioMerchandisingDetalleUpdateView.as_view(), name='ajuste_inventario_merchandising_detalle_actualizar'),
    path('ajuste-inventario-merchandising/detalle/eliminar/<pk>/', views.AjusteInventarioMerchandisingDetalleDeleteView.as_view(), name='ajuste_inventario_merchandising_detalle_eliminar'),
]

urlpatterns = [
    path('modelo-merchandising/', views.ModeloMerchandisingListView.as_view(), name='modelo_merchandising_inicio'),
    path('modelo-merchandising-tabla/', views.ModeloMerchandisingTabla, name='modelo_merchandising_tabla'),
    path('modelo-merchandising/registrar/', views.ModeloMerchandisingCreateView.as_view(), name='modelo_merchandising_registrar'),
    path('modelo-merchandising/actualizar/<pk>/', views.ModeloMerchandisingUpdateView.as_view(), name='modelo_merchandising_actualizar'),

    path('marca-merchandising/', views.MarcaMerchandisingListView.as_view(), name='marca_merchandising_inicio'),
    path('marca-merchandising-tabla/', views.MarcaMerchandisingTabla, name='marca_merchandising_tabla'),
    path('marca-merchandising/registrar/', views.MarcaMerchandisingCreateView.as_view(), name='marca_merchandising_registrar'),
    path('marca-merchandising/actualizar/<pk>/', views.MarcaMerchandisingUpdateView.as_view(), name='marca_merchandising_actualizar'),

    path('merchandising/', views.MerchandisingListView.as_view(), name='merchandising_inicio'),
    path('merchandising-tabla/', views.MerchandisingTabla, name='merchandising_tabla'),
    path('merchandising/registrar/', views.MerchandisingCreateView.as_view(), name='merchandising_registrar'),
    path('merchandising/actualizar/<pk>/', views.MerchandisingUpdateView.as_view(), name='merchandising_actualizar'),
    path('merchandising/baja/<pk>/', views.MerchandisingDarBajaView.as_view(), name='merchandising_baja'),
    path('merchandising/alta/<pk>/', views.MerchandisingDarAltaView.as_view(), name='merchandising_alta'),
    path('merchandising/detalle/<pk>/', views.MerchandisingDetailView.as_view(), name='merchandising_detalle'),
    path('merchandising/detalle-tabla/<pk>/', views.MerchandisingDetailTabla, name='merchandising_detalle_tabla'),
    path('merchandising/info/<id_merchandising>/', views.MerchandisingView, name='merchandising_info'),
    
    # path('precio-lista/', views.PrecioListaPdfView.as_view(), name='precio_lista'),
    # path('precio-lista-stock/', views.PrecioListaStockPdfView.as_view(), name='precio_lista_stock'),

    path('componente-merchandising/registrar/<int:merchandising_id>/', views.ComponenteMerchandisingCreateView.as_view(), name='componente_merchandising_registrar'),
    path('componente-merchandising/actualizar/<pk>/', views.ComponenteMerchandisingUpdateView.as_view(), name='componente_merchandising_actualizar'),
    path('componente-merchandising/eliminar/<pk>/', views.ComponenteMerchandisingDeleteView.as_view(), name='componente_merchandising_eliminar'),

    path('especificacion-merchandising/registrar/<int:merchandising_id>/', views.EspecificacionMerchandisingCreateView.as_view(), name='especificacion_merchandising_registrar'),
    path('especificacion-merchandising/actualizar/<pk>/', views.EspecificacionMerchandisingUpdateView.as_view(), name='especificacion_merchandising_actualizar'),
    path('especificacion-merchandising/eliminar/<pk>/', views.EspecificacionMerchandisingDeleteView.as_view(), name='especificacion_merchandising_eliminar'),

    path('datasheet-merchandising/registrar/<int:merchandising_id>/', views.DatasheetMerchandisingCreateView.as_view(), name='datasheet_merchandising_registrar'),
    path('datasheet-merchandising/actualizar/<pk>/', views.DatasheetMerchandisingUpdateView.as_view(), name='datasheet_merchandising_actualizar'),
    path('datasheet-merchandising/eliminar/<pk>/', views.DatasheetMerchandisingDeleteView.as_view(), name='datasheet_merchandising_eliminar'),

    path('datos-importacion-merchandising/actualizar/<pk>/', views.DatosImportacionMerchandisingUpdateView.as_view(), name='datos_importacion_merchandising_actualizar'),

    path('producto-sunat-merchandising/actualizar/<pk>/', views.ProductoSunatMerchandisingUpdateView.as_view(), name='producto_sunat_merchandising_actualizar'),
    path('producto-sunat-merchandising/buscar/<pk>/', views.ProductoSunatMerchandisingBuscarView.as_view(), name='producto_sunat_merchandising_buscar'),
    path('producto-sunat-merchandising/', views.ProductoSunatJsonView, name='producto_sunat_merchandising_json'),

    path('familia-sunat/<str:id_segmento>/', views.FamiliaSunatView, name='familia_sunat'),
    path('clase-sunat/<str:id_familia>/', views.ClaseSunatView, name='clase_sunat'),
    path('producto-sunat/<str:id_clase>/', views.ProductoSunatView, name='producto_sunat'),

    path('subfamilia/<str:id_familia>/', views.SubfamiliaMerchandisingView, name='subfamilia'),
    path('unidad/<str:id_subfamilia>/', views.UnidadView, name='unidad'),
    path('unidad/merchandising/<str:id_merchandising>/', views.UnidadMerchandisingView, name='unidad_merchandising'),

    path('modelo-merchandising/<str:id_marca>/', views.ModeloMerchandisingView, name='modelo_merchandising'),

    path('imagen-merchandising/registrar/<int:merchandising_id>/', views.ImagenMerchandisingCreateView.as_view(), name='imagen_merchandising_registrar'),
    path('imagen-merchandising/actualizar/<pk>/', views.ImagenMerchandisingUpdateView.as_view(), name='imagen_merchandising_actualizar'),
    path('imagen-merchandising/baja/<pk>/', views.ImagenMerchandisingDarBaja.as_view(), name='imagen_merchandising_baja'),
    path('imagen-merchandising/alta/<pk>/', views.ImagenMerchandisingDarAlta.as_view(), name='imagen_merchandising_alta'),

    path('video-merchandising/registrar/<int:merchandising_id>/', views.VideoMerchandisingCreateView.as_view(), name='video_merchandising_registrar'),
    path('video-merchandising/actualizar/<pk>/', views.VideoMerchandisingUpdateView.as_view(), name='video_merchandising_actualizar'),
    path('video-merchandising/baja/<pk>/', views.VideoMerchandisingDarBaja.as_view(), name='video_merchandising_baja'),
    path('video-merchandising/alta/<pk>/', views.VideoMerchandisingDarAlta.as_view(), name='video_merchandising_alta'),

    path('equivalencia-unidad-merchandising/registrar/<int:merchandising_id>/', views.EquivalenciaUnidadCreateView.as_view(), name='equivalencia_unidad_merchandising_registrar'),
    path('equivalencia-unidad-merchandising/actualizar/<pk>/', views.EquivalenciaUnidadUpdateView.as_view(), name='equivalencia_unidad_merchandising_actualizar'),
    path('equivalencia-unidad-merchandising/baja/<pk>/', views.EquivalenciaUnidadDarBaja.as_view(), name='equivalencia_unidad_merchandising_baja'),
    path('equivalencia-unidad-merchandising/alta/<pk>/', views.EquivalenciaUnidadDarAlta.as_view(), name='equivalencia_unidad_merchandising_alta'),

    path('proveedor-merchandising/registrar/<int:merchandising_id>/', views.ProveedorMerchandisingCreateView.as_view(), name='proveedor_merchandising_registrar'),
    path('proveedor-merchandising/actualizar/<pk>/', views.ProveedorMerchandisingUpdateView.as_view(), name='proveedor_merchandising_actualizar'),
    path('proveedor-merchandising/baja/<pk>/', views.ProveedorMerchandisingDarBaja.as_view(), name='proveedor_merchandising_baja'),
    path('proveedor-merchandising/alta/<pk>/', views.ProveedorMerchandisingDarAlta.as_view(), name='proveedor_merchandising_alta'),
    path('proveedor-merchandising/info/<id_merchandising>/', views.ProveedorMerchandisingView, name='proveedor_merchandising_info'),

    path('idioma-merchandising/registrar/<int:merchandising_id>/', views.IdiomaMerchandisingCreateView.as_view(), name='idioma_merchandising_registrar'),
    path('idioma-merchandising/actualizar/<pk>/', views.IdiomaMerchandisingUpdateView.as_view(), name='idioma_merchandising_actualizar'),

    # path('precio-merchandising/registrar/<int:merchandising_id>/<int:merchandising_content_type>/', views.PrecioListaMerchandisingCreateView.as_view(), name='precio_merchandising_registrar'),
    
    # path('precio-merchandising/<int:id_comprobante>/<int:comprobante_content_type>/<int:id_merchandising>/<int:merchandising_content_type>/', views.ComprobanteView, name='comprobante'),
    
    # path('precio-lista/<int:id_merchandising>/', views.PrecioListaView, name='precio_lista'),

    path('stock/<int:id_merchandising>/', views.StockView, name='stock'),
    path('stock/<int:id_merchandising>/<int:id_sociedad>/', views.StockSociedadView, name='stock'),
    path('stock/<int:id_merchandising>/<int:id_sociedad>/<int:id_almacen>/', views.StockSociedadAlmacenView, name='stock'),
    
    path('stock/sede/<int:id_merchandising>/<int:id_sociedad>/<int:id_sede>/', views.StockSedeView, name='stock_sede'),
    path('stock/sede/<int:id_merchandising>/<int:id_sociedad>/<int:id_sede>/<int:id_tipo_stock>/', views.StockSedeTipoStockView, name='stock_sede_tipo_stock'),

    path('stock/disponible/<int:id_merchandising>/', views.StockDisponibleView, name='stock_disponible'),
    path('stock/disponible/<int:id_merchandising>/<int:id_sociedad>/', views.StockDisponibleSociedadView, name='stock_disponible'),
    path('stock/disponible/<int:id_merchandising>/<int:id_sociedad>/<int:id_almacen>/', views.StockDisponibleSociedadAlmacenView, name='stock_disponible'),
    
    path('stock/disponible/sede/<int:id_merchandising>/<int:id_sociedad>/<int:id_sede>/', views.StockSedeDisponibleView, name='stock_disponible_sede'),
    
    path('stock/tipo_stock/<int:id_merchandising>/<int:id_sociedad>/<int:id_almacen>/<int:id_tipo_stock>/', views.StockTipoStockView, name='stock_tipo_stock'),

    # path('series/<pk>/', views.MerchandisingSeriesView.as_view(), name='series'),
] + urlInventarioMerchandising + urlAjusteInventarioMerchandising