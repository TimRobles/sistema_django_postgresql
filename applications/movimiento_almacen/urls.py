from django.urls import path
from . import views

app_name = 'movimiento_almacen_app'

urlpatterns = [
    path('ver-movimiento/<int:id_registro>/<pk>/', views.MovimientoMaterialView.as_view(), name='ver_movimiento'),
    path('ver-stock/<int:id_registro>/<pk>/', views.StockMaterialView.as_view(), name='ver_stock'),
]