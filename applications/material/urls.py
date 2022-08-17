from django.urls import path
from . import views

app_name='material_app'

urlpatterns = [
    path('modelo/', views.ModeloListView.as_view(), name='modelo_inicio'),
    path('modelo-tabla/', views.ModeloTabla, name='modelo_tabla'),
    path('modelo/registrar/', views.ModeloCreateView.as_view(), name='modelo_registrar'),
    path('modelo/actualizar/<pk>/', views.ModeloUpdateView.as_view(), name='modelo_actualizar'),

    path('marca/', views.MarcaListView.as_view(), name='marca_inicio'),
    path('marca-tabla/', views.MarcaTabla, name='marca_tabla'),
    path('marca/registrar/', views.MarcaCreateView.as_view(), name='marca_registrar'),
    path('marca/actualizar/<pk>/', views.MarcaUpdateView.as_view(), name='marca_actualizar'),

    path('material/', views.MaterialListView.as_view(), name='material_inicio'),
    path('material-tabla/', views.MaterialTabla, name='material_tabla'),
    path('material/registrar/', views.MaterialCreateView.as_view(), name='material_registrar'),
    path('material/actualizar/<pk>/', views.MaterialUpdateView.as_view(), name='material_actualizar'),
    path('material/baja/<pk>/', views.MaterialDarBajaView.as_view(), name='material_baja'),
    path('material/alta/<pk>/', views.MaterialDarAltaView.as_view(), name='material_alta'),
    path('material/detalle/<pk>/', views.MaterialDetailView.as_view(), name='material_detalle'),
    path('material/detalle-tabla/<pk>/', views.MaterialDetailTabla, name='material_detalle_tabla'),

    path('componente/registrar/<int:material_id>/', views.ComponenteCreateView.as_view(), name='componente_registrar'),
    path('componente/actualizar/<pk>/', views.ComponenteUpdateView.as_view(), name='componente_actualizar'),
    path('componente/eliminar/<pk>/', views.ComponenteDeleteView.as_view(), name='componente_eliminar'),

    path('especificacion/registrar/<int:material_id>/', views.EspecificacionCreateView.as_view(), name='especificacion_registrar'),
    path('especificacion/actualizar/<pk>/', views.EspecificacionUpdateView.as_view(), name='especificacion_actualizar'),
    path('especificacion/eliminar/<pk>/', views.EspecificacionDeleteView.as_view(), name='especificacion_eliminar'),

    path('datasheet/registrar/<int:material_id>/', views.DatasheetCreateView.as_view(), name='datasheet_registrar'),
    path('datasheet/actualizar/<pk>/', views.DatasheetUpdateView.as_view(), name='datasheet_actualizar'),
    path('datasheet/eliminar/<pk>/', views.DatasheetDeleteView.as_view(), name='datasheet_eliminar'),

    path('datos-importacion/actualizar/<pk>/', views.DatosImportacionUpdateView.as_view(), name='datos_importacion_actualizar'),

    path('producto-sunat/actualizar/<pk>/', views.ProductoSunatUpdateView.as_view(), name='producto_sunat_actualizar'),

    path('familia-sunat/<str:id_segmento>/', views.FamiliaSunatView, name='familia_sunat'),
    path('clase-sunat/<str:id_familia>/', views.ClaseSunatView, name='clase_sunat'),
    path('producto-sunat/<str:id_clase>/', views.ProductoSunatView, name='producto_sunat'),

    path('subfamilia/<str:id_familia>/', views.SubfamiliaView, name='subfamilia'),
    path('unidad/<str:id_subfamilia>/', views.UnidadView, name='unidad'),

    path('modelo/<str:id_marca>/', views.ModeloView, name='modelo'),

    path('imagen-material/registrar/<int:material_id>/', views.ImagenMaterialCreateView.as_view(), name='imagen_material_registrar'),
    path('imagen-material/actualizar/<pk>/', views.ImagenMaterialUpdateView.as_view(), name='imagen_material_actualizar'),
    path('imagen-material/baja/<pk>/', views.ImagenMaterialDarBaja.as_view(), name='imagen_material_baja'),
    path('imagen-material/alta/<pk>/', views.ImagenMaterialDarAlta.as_view(), name='imagen_material_alta'),

    path('video-material/registrar/<int:material_id>/', views.VideoMaterialCreateView.as_view(), name='video_material_registrar'),
    path('video-material/actualizar/<pk>/', views.VideoMaterialUpdateView.as_view(), name='video_material_actualizar'),
    path('video-material/baja/<pk>/', views.VideoMaterialDarBaja.as_view(), name='video_material_baja'),
    path('video-material/alta/<pk>/', views.VideoMaterialDarAlta.as_view(), name='video_material_alta'),

    path('equivalencia-unidad-material/registrar/<int:material_id>/', views.EquivalenciaUnidadCreateView.as_view(), name='equivalencia_unidad_material_registrar'),
    path('equivalencia-unidad-material/actualizar/<pk>/', views.EquivalenciaUnidadUpdateView.as_view(), name='equivalencia_unidad_material_actualizar'),
    path('equivalencia-unidad-material/baja/<pk>/', views.EquivalenciaUnidadDarBaja.as_view(), name='equivalencia_unidad_material_baja'),
    path('equivalencia-unidad-material/alta/<pk>/', views.EquivalenciaUnidadDarAlta.as_view(), name='equivalencia_unidad_material_alta'),

    path('proveedor-material/registrar/<int:material_id>/', views.ProveedorMaterialCreateView.as_view(), name='proveedor_material_registrar'),
    path('proveedor-material/actualizar/<pk>/', views.ProveedorMaterialUpdateView.as_view(), name='proveedor_material_actualizar'),
    path('proveedor-material/baja/<pk>/', views.ProveedorMaterialDarBaja.as_view(), name='proveedor_material_baja'),
    path('proveedor-material/alta/<pk>/', views.ProveedorMaterialDarAlta.as_view(), name='proveedor_material_alta'),

    path('idioma-material/registrar/<int:material_id>/', views.IdiomaMaterialCreateView.as_view(), name='idioma_material_registrar'),
    path('idioma-material/actualizar/<pk>/', views.IdiomaMaterialUpdateView.as_view(), name='idioma_material_actualizar'),

    path('precio-material/registrar/<int:material_id>/<int:material_content_type>/', views.PrecioListaMaterialCreateView.as_view(), name='precio_material_registrar'),
    
    # path('precio-material/<int:id_comprobante>/<int:comprobante_content_type>/', views.ComprobanteView, name='comprobante'),
    # path('precio-material/<int:id_comprobante>/', views.ComprobanteView, name='comprobante'),
]
