from django.urls import path
from django.contrib import admin
from .import views


app_name='cambio_sociedad_app'

urlSeries = [
    path('validar-series/cambio-sociedad-stock/detalle/<pk>/', views.ValidarSeriesCambioSociedadStockDetailView.as_view(), name='validar_series_cambio_sociedad_stock_detalle'),
    path('validar-series/cambio-sociedad-stock/detalle-tabla/<pk>/', views.ValidarSeriesCambioSociedadStockDetailTabla, name='validar_series_cambio_sociedad_stock_detalle_tabla'),
    path('validar-series/cambio-sociedad-stock/pdf/<pk>/', views.ValidarSeriesCambioSociedadStockSeriesPdf.as_view(), name='validar_series_cambio_sociedad_stock_pdf'),
    path('validar-series-detalle/cambio-sociedad-stock/eliminar/<pk>/', views.ValidarSeriesCambioSociedadStockDetalleDeleteView.as_view(), name='validar_series_cambio_sociedad_stock_detalle_eliminar'),
]

urlpatterns = urlSeries + [
    path('cambio-sociedad-stock/', views.CambioSociedadStockListView.as_view(), name='cambio_sociedad_stock_inicio'),
    path('cambio-sociedad-stock-tabla/', views.CambioSociedadStockTabla, name='cambio_sociedad_stock_tabla'),
    path('cambio-sociedad-stock/registrar/', views.CambioSociedadStockCreateView.as_view(), name='cambio_sociedad_stock_registrar'),
    path('cambio-sociedad-stock/actualizar/<pk>', views.CambioSociedadStockUpdateView.as_view(), name='cambio_sociedad_stock_actualizar'),
    path('cambio-sociedad-stock/concluir/<pk>/', views.CambioSociedadStockConcluirView.as_view(), name='cambio_sociedad_stock_concluir'),
    path('cambio-sociedad-stock/detalle/<pk>/', views.CambioSociedadStockDetailView.as_view(), name='cambio_sociedad_stock_detalle'),
    path('cambio-sociedad-stock/detalle-tabla/<pk>/', views.CambioSociedadStockDetailTabla, name='cambio_sociedad_stock_detalle_tabla'),
    path('cambio-sociedad-stock-detalle/registrar/<int:cambio_sociedad_stock_id>/', views.CambioSociedadStockDetalleCreateView.as_view(), name='cambio_sociedad_stock_detalle_registrar'),
    path('cambio-sociedad-stock-detalle/actualizar/<int:cambio_sociedad_stock_id>/<pk>/', views.CambioSociedadStockDetalleUpdateView.as_view(), name='cambio_sociedad_stock_detalle_actualizar'),
 ]