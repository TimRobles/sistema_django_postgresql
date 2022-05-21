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

]
