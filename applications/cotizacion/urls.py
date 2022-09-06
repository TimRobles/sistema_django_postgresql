from django.urls import path
from . import views

app_name = 'cotizacion_app'

urlpatterns = [ 
    path('cotizacion-venta/',views.CotizacionVentaListView.as_view(),name='cotizacion_venta_inicio'),
    path('cotizacion-venta-tabla/',views.CotizacionVentaTabla,name='cotizacion_venta_tabla'),
    path('cotizacion-venta/registrar/', views.CotizacionVentaCreateView, name='cotizacion_venta_registrar'),
    path('cotizacion-venta/ver/<int:id_cotizacion>/', views.CotizacionVentaVerView.as_view(), name='cotizacion_venta_ver'),
    path('cotizacion-venta/ver/tabla/<int:id_cotizacion>/', views.CotizacionVentaVerTabla, name='cotizacion_venta_ver_tabla'),

    path('cotizacion-venta/cliente/<pk>/', views.CotizacionVentaClienteView.as_view(), name='cotizacion_venta_cliente'),
    path('cotizacion-cliente-interlocutor/<int:id_cliente>/', views.ClienteInterlocutorView, name='cotizacion_cliente_interlocutor'),

    path('cotizacion-venta-detalle-tabla/<int:cotizacion_id>/', views.CotizacionVentaDetalleTabla, name='cotizacion_venta_detalle_tabla'),
    path('cotizacion-venta/agregar-material/<int:cotizacion_id>/', views.CotizacionVentaMaterialDetalleView.as_view(), name='cotizacion_venta_agregar_material'),
    
    path('cotizacion-venta/sociedad/<pk>/', views.CotizacionSociedadUpdateView.as_view(), name='cotizacion_venta_sociedad'),
    path('cotizacion-venta/sociedad/guardar/<int:cantidad>/<int:item>/<str:abreviatura>/', views.GuardarCotizacionSociedad, name='guardar_cotizacion_venta_sociedad'),
    
]