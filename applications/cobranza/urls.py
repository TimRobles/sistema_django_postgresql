from django.urls import path
from . import views

app_name = 'cobranza_app'

urlpatterns = [

    path('linea-credito/',views.LineaCreditoView.as_view(),name='linea_credito_inicio'),
    path('linea-credito-tabla/',views.LineaCreditoTabla,name='linea_credito_tabla'),
    path('linea-credito/registrar/', views.LineaCreditoCreateView.as_view(), name='linea_credito_registrar'),

    path('deudores/',views.DeudoresView.as_view(),name='deudores_inicio'),
    path('deudores/detalle/<int:id_cliente>/',views.DeudaView.as_view(),name='deudores_detalle'),
    path('deudores/detalle/tabla/<int:id_cliente>/',views.DeudaTabla,name='deudores_detalle_tabla'),
    
    path('deudores/pagar/deuda/<int:id_cliente>/<int:id_deuda>/',views.DeudaPagarCreateView.as_view(),name='deudores_pagar_deuda'),
    path('deudores/cancelar/deuda/<int:id_cliente>/<pk>/',views.DeudaCancelarView.as_view(),name='deudores_cancelar_deuda'),
    path('deudores/eliminar/redondeo/<int:id_cliente>/<pk>/',views.RedondeoDeleteView.as_view(),name='deudores_eliminar_redondeo'),
    
    path('deudores/eliminar/pago/<int:id_cliente>/<pk>/',views.DeudaPagarDeleteView.as_view(),name='deudores_eliminar_pago'),
    path('deudores/actualizar/pago/<int:id_cliente>/<int:id_deuda>/<pk>/',views.DeudaPagarUpdateView.as_view(),name='deudores_actualizar_pago'),

    path('cuenta-bancaria/depositos/',views.DepositosView.as_view(),name='cuenta_bancaria_depositos_inicio'),
    path('cuenta-bancaria/depositos/tabla/',views.DepositosTabla,name='cuenta_bancaria_depositos_tabla'),
    path('cuenta-bancaria/depositos/eliminar/pago/<int:id_cuenta_bancaria>/<pk>/',views.DepositosPagarDeleteView.as_view(),name='cuenta_bancaria_depositos_eliminar_pago'),

    path('cuenta-bancaria/',views.CuentaBancariaView.as_view(),name='cuenta_bancaria_inicio'),
    path('cuenta-bancaria/detalle/<pk>/',views.CuentaBancariaDetalleView.as_view(),name='cuenta_bancaria_detalle'),
    path('cuenta-bancaria/detalle/tabla/<pk>/',views.CuentaBancariaDetalleTabla,name='cuenta_bancaria_detalle_tabla'),
    path('cuenta-bancaria/agregar/ingreso/<int:id_cuenta_bancaria>/',views.CuentaBancariaIngresoView.as_view(),name='cuenta_bancaria_agregar_ingreso'),
    path('cuenta-bancaria/agregar/ingreso/efectivo/<int:id_cuenta_bancaria>/',views.CuentaBancariaEfectivoIngresoView.as_view(),name='cuenta_bancaria_agregar_ingreso_efectivo'),
    path('cuenta-bancaria/cambiar/ingreso/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoCambiarUpdateView.as_view(),name='cuenta_bancaria_cambiar_ingreso'),
    path('cuenta-bancaria/actualizar/ingreso/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoUpdateView.as_view(),name='cuenta_bancaria_actualizar_ingreso'),
    path('cuenta-bancaria/actualizar/ingreso/efectivo/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaEfectivoIngresoUpdateView.as_view(),name='cuenta_bancaria_actualizar_ingreso_efectivo'),
    path('cuenta-bancaria/ver-voucher/ingreso/<pk>/',views.CuentaBancariaIngresoVerVoucherView.as_view(),name='cuenta_bancaria_ver_voucher_ingreso'),
    path('cuenta-bancaria/eliminar/ingreso/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoDeleteView.as_view(),name='cuenta_bancaria_eliminar_ingreso'),
    
    path('cuenta-bancaria/pagar/deuda/<int:id_cuenta_bancaria>/<int:id_ingreso>/',views.CuentaBancariaIngresoPagarCreateView.as_view(),name='cuenta_bancaria_pagar_deuda'),
    path('cuenta-bancaria/cancelar/deuda/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoCancelarView.as_view(),name='cuenta_bancaria_cancelar_deuda'),
    
    path('cuenta-bancaria/eliminar/pago/<int:id_cuenta_bancaria>/<pk>/',views.CuentaBancariaIngresoPagarDeleteView.as_view(),name='cuenta_bancaria_eliminar_pago'),
    path('cuenta-bancaria/actualizar/pago/<int:id_cuenta_bancaria>/<int:id_ingreso>/<pk>/',views.CuentaBancariaIngresoPagarUpdateView.as_view(),name='cuenta_bancaria_actualizar_pago'),
 ]