from django.urls import path
from .import views

app_name = 'calidad_app'

urlNotaControlCalidadStock = [

    path('nota-control-calidad-stock/', views.NotaControlCalidadStockListView.as_view(), name='nota_control_calidad_stock_inicio'),
    path('nota-control-calidad-stock-tabla/', views.NotaControlCalidadStockTabla, name='nota_control_calidad_stock_tabla'),
    path('nota-control-calidad-stock/registrar/', views.NotaControlCalidadStockCreateView.as_view(), name='nota_control_calidad_stock_registrar'),
    path('nota-control-calidad-stock/anular/<pk>/', views.NotaControlCalidadStockDeleteView.as_view(), name='nota_control_calidad_stock_anular'),
    path('nota-control-calidad-stock/detalle/<pk>/', views.NotaControlCalidadStockDetailView.as_view(), name='nota_control_calidad_stock_detalle'),
    path('nota-control-calidad-stock/detalle-tabla/<pk>/', views.NotaControlCalidadStockDetailTabla, name='nota_control_calidad_stock_detalle_tabla'),
    path('nota-control-calidad-stock/detalle/registrar/<int:nota_control_calidad_stock_id>/', views.NotaControlCalidadStockDetalleCreateView.as_view(), name='nota_control_calidad_stock_detalle_registrar'),
    path('nota-control-calidad-stock/detalle/actualizar/<pk>/', views.NotaControlCalidadStockDetalleUpdateView.as_view(), name='nota_control_calidad_stock_detalle_actualizar'),
    path('nota-control-calidad-stock/detalle/eliminar/<pk>/', views.NotaControlCalidadStockDetalleDeleteView.as_view(), name='nota_control_calidad_stock_detalle_eliminar'),
]

urlpatterns = [

    path('falla-material/',views.FallaMaterialTemplateView.as_view(),name='falla_material'),
    path('falla-material/detalle/<pk>/', views.FallaMaterialDetailView.as_view(), name='falla_material_detalle'),
    path('falla-material/detalle-tabla/<pk>/', views.FallaMaterialDetailTabla, name='falla_material_detalle_tabla'),    
    path('falla-material/detalle/registrar/<int:subfamilia_id>/', views.FallaMaterialCreateView.as_view(), name='falla_material_detalle_registrar'),
    path('falla-material/detalle/actualizar/<pk>/', views.FallaMaterialUpdateView.as_view(), name='falla_material_detalle_actualizar'),
    path('falla-material/detalle/eliminar/<pk>/', views.FallaMaterialDeleteView.as_view(), name='falla_material_detalle_eliminar'),
] + urlNotaControlCalidadStock