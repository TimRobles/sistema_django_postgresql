from django.urls import path
from . import views

app_name = 'comprobante_venta_app'

urlpatterns = [ 
    path('factura-venta/',views.FacturaVentaListView.as_view(),name='factura_venta_inicio'),
    path('factura-venta-tabla/',views.FacturaVentaTabla,name='factura_venta_tabla'),

]