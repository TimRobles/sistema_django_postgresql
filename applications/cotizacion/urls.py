from django.urls import path
from . import views

app_name = 'cotizacion_app'

urlpatterns = [ 
    path('cotizacion-venta/',views.CotizacionVentaListView.as_view(),name='cotizacion_venta_inicio'),
    path('cotizacion-venta-tabla/',views.CotizacionVentaTabla,name='cotizacion_venta_tabla'),
    path('cotizacion-venta/registrar/', views.CotizacionVentaCreateView.as_view(), name='cotizacion_venta_registrar'),

    path('cotizacion-venta/cliente/<pk>/', views.ClienteView.as_view(), name='cotizacion_venta_cliente'),


    
]