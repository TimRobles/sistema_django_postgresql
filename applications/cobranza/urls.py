from django.urls import path
from . import views

app_name = 'cobranza_app'

urlpatterns = [

    path('linea-credito/',views.LineaCreditoView.as_view(),name='linea_credito_inicio'),
    path('linea-credito-tabla/',views.LineaCreditoTabla,name='linea_credito_tabla'),
    path('linea-credito/registrar/', views.LineaCreditoCreateView.as_view(), name='linea_credito_registrar'),

    path('deudores/',views.DeudoresView.as_view(),name='deudores_inicio'),
    path('deudores/detalle/<int:id_cliente>/',views.DeudaView.as_view(),name='deudores_detalle'),

    path('cuenta-bancaria/',views.CuentaBancariaView.as_view(),name='cuenta_bancaria_inicio'),
    path('cuenta-bancaria/detalle/<pk>/',views.CuentaBancariaDetalleView.as_view(),name='cuenta_bancaria_detalle'),
    path('cuenta-bancaria/agregar/ingreso/<int:id_cuenta_bancaria>/',views.CuentaBancariaIngresoView.as_view(),name='cuenta_bancaria_agregar_ingreso'),
    path('cuenta-bancaria/actualizar/ingreso/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoUpdateView.as_view(),name='cuenta_bancaria_actualizar_ingreso'),
    path('cuenta-bancaria/eliminar/ingreso/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoDeleteView.as_view(),name='cuenta_bancaria_eliminar_ingreso'),
    
    path('cuenta-bancaria/pagar/deuda/<int:id_cuenta_bancaria>/<int:id_ingreso>/',views.CuentaBancariaIngresoPagarView.as_view(),name='cuenta_bancaria_pagar_deuda'),
 ]