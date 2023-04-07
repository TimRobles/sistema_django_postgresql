from django.urls import path
from . import views

app_name='contabilidad_app'

urlTelecredito = [
    path('telecredito/', views.TelecreditoListView.as_view(), name='telecredito_inicio'),
    path('telecredito-tabla/', views.TelecreditoTabla, name='telecredito_tabla'),
    path('telecredito/registrar/', views.TelecreditoCreateView.as_view(), name='telecredito_registrar'),
    path('telecredito/actualizar/<pk>/', views.TelecreditoUpdateView.as_view(), name='telecredito_actualizar'),
    # path('telecredito/eliminar/<pk>/', views.TelecreditoDeleteView.as_view(), name='telecredito_eliminar'),
    path('telecredito/solicitar/<pk>/', views.TelecreditoSolicitarView.as_view(), name='telecredito_solicitar'),
    path('telecredito/recibir/<pk>/', views.TelecreditoRecibirView.as_view(), name='telecredito_recibir'),
    path('telecredito/pdf/<pk>/', views.TelecreditoRecibosPdfView.as_view(), name='telecredito_pdf'),

    path('telecredito/recibos/<pk>/', views.TelecreditoRecibosListView.as_view(), name='telecredito_recibos_inicio'),
    path('telecredito/recibos-tabla/<pk>/', views.TelecreditoRecibosTabla, name='telecredito_recibos_tabla'),
    path('telecredito/recibos/registrar/<pk>', views.TelecreditoRecibosCreateView.as_view() , name='telecredito_recibos_registrar'),
    path('telecredito/recibos/eliminar/<int:telecredito_id>/<pk>', views.TelecreditoRecibosDeleteView.as_view() , name='telecredito_recibos_eliminar'),
    path('telecredito/recibos/actualizar/<int:telecredito_id>/<pk>', views.TelecreditoRecibosUpdateView.as_view() , name='telecredito_recibos_actualizar'),
    path('telecredito/recibos/pagar/<int:telecredito_id>/<pk>', views.TelecreditoReciboPagarView.as_view() , name='telecredito_recibos_pagar'),
]

urlpatterns = urlTelecredito + [
    path('comision/', views.ComisionFondoPensionesListView.as_view(), name='comision_inicio'),
    path('comision-tabla/', views.ComisionFondoPensionesTabla, name='comision_tabla'),
    path('comision/registrar/', views.ComisionFondoPensionesCreateView.as_view(), name='comision_registrar'),
    path('comision/actualizar/<pk>/', views.ComisionFondoPensionesUpdateView.as_view(), name='comision_actualizar'),
    path('comision/eliminar/<pk>/', views.ComisionFondoPensionesDeleteView.as_view(), name='comision_eliminar'),

    path('datos-planilla/', views.DatosPlanillaListView.as_view(), name='datos_planilla_inicio'),
    path('datos-planilla-tabla/', views.DatosPlanillaTabla, name='datos_planilla_tabla'),
    path('datos-planilla/registrar/', views.DatosPlanillaCreateView.as_view(), name='datos_planilla_registrar'),
    path('datos-planilla/actualizar/<pk>/', views.DatosPlanillaUpdateView.as_view(), name='datos_planilla_actualizar'),    
    path('datos-planilla/baja/<pk>/', views.DatosPlanillaDarBajaView.as_view(), name='datos_planilla_baja'),    

    path('essalud/', views.EsSaludListView.as_view(), name='essalud_inicio'),
    path('essalud-tabla/', views.EsSaludTabla, name='essalud_tabla'),
    path('essalud/registrar/', views.EsSaludCreateView.as_view(), name='essalud_registrar'),
    path('essalud/actualizar/<pk>/', views.EsSaludUpdateView.as_view(), name='essalud_actualizar'),    

    path('boleta-pago/', views.BoletaPagoListView.as_view(), name='boleta_pago_inicio'),
    path('boleta-pago-tabla/', views.BoletaPagoTabla, name='boleta_pago_tabla'),
    path('boleta-pago/registrar/', views.BoletaPagoCreateView.as_view(), name='boleta_pago_registrar'),
    path('boleta-pago/actualizar/<pk>/', views.BoletaPagoUpdateView.as_view(), name='boleta_pago_actualizar'),    
    path('boleta-pago/eliminar/<pk>/', views.BoletaPagoDeleteView.as_view(), name='boleta_pago_eliminar'),    

    path('recibo-boleta-pago/', views.ReciboBoletaPagoListView.as_view(), name='recibo_boleta_pago_inicio'),
    path('recibo-boleta-pago-tabla/', views.ReciboBoletaPagoTabla, name='recibo_boleta_pago_tabla'),
    path('recibo-boleta-pago/registrar/', views.ReciboBoletaPagoCreateView.as_view(), name='recibo_boleta_pago_registrar'),
    path('recibo-boleta-pago/actualizar/<pk>/', views.ReciboBoletaPagoUpdateView.as_view(), name='recibo_boleta_pago_actualizar'),    
    path('recibo-boleta-pago/eliminar/<pk>/', views.ReciboBoletaPagoDeleteView.as_view(), name='recibo_boleta_pago_eliminar'),    

    path('servicio/', views.ServicioListView.as_view(), name='servicio_inicio'),
    path('servicio-tabla/', views.ServicioTabla, name='servicio_tabla'),
    path('servicio/registrar/', views.ServicioCreateView.as_view(), name='servicio_registrar'),
    path('servicio/actualizar/<pk>/', views.ServicioUpdateView.as_view(), name='servicio_actualizar'),    

    path('recibo-servicio/', views.ReciboServicioListView.as_view(), name='recibo_servicio_inicio'),
    path('recibo-servicio-tabla/', views.ReciboServicioTabla, name='recibo_servicio_tabla'),
    path('recibo-servicio/registrar/', views.ReciboServicioCreateView.as_view(), name='recibo_servicio_registrar'),
    path('recibo-servicio/actualizar/<pk>/', views.ReciboServicioUpdateView.as_view(), name='recibo_servicio_actualizar'),    
    path('recibo-servicio/eliminar/<pk>/', views.ReciboServicioDeleteView.as_view(), name='recibo_servicio_eliminar'),    

    path('tipo-servicio/', views.TipoServicioListView.as_view(), name='tipo_servicio_inicio'),
    path('tipo-servicio-tabla/', views.TipoServicioTabla, name='tipo_servicio_tabla'),
    path('tipo-servicio/registrar/', views.TipoServicioCreateView.as_view(), name='tipo_servicio_registrar'),
    path('tipo-servicio/actualizar/<pk>/', views.TipoServicioUpdateView.as_view(), name='tipo_servicio_actualizar'),    

    path('institucion/', views.InstitucionListView.as_view(), name='institucion_inicio'),
    path('institucion-tabla/', views.InstitucionTabla, name='institucion_tabla'),
    path('institucion/registrar/', views.InstitucionCreateView.as_view(), name='institucion_registrar'),
    path('institucion/actualizar/<pk>/', views.InstitucionUpdateView.as_view(), name='institucion_actualizar'),   

    path('medio-pago/', views.MedioPagoListView.as_view(), name='medio_pago_inicio'),
    path('medio-pago-tabla/', views.MedioPagoTabla, name='medio_pago_tabla'),
    path('medio-pago/registrar/', views.MedioPagoCreateView.as_view(), name='medio_pago_registrar'),
    path('medio-pago/actualizar/<pk>/', views.MedioPagoUpdateView.as_view(), name='medio_pago_actualizar'),

    path('cheque/', views.ChequeListView.as_view(), name='cheque_inicio'),
    path('cheque-tabla/', views.ChequeTabla, name='cheque_tabla'),
    path('cheque/registrar/', views.ChequeCreateView.as_view(), name='cheque_registrar'),
    path('cheque/actualizar/<pk>/', views.ChequeUpdateView.as_view(), name='cheque_actualizar'),
    path('cheque/eliminar/<pk>/', views.ChequeDeleteView.as_view(), name='cheque_eliminar'),

    path('cheque/detalle/<pk>/', views.ChequeDetalleView.as_view(), name='cheque_detalle'),
    path('cheque/detalle-tabla/<pk>', views.ChequeDetalleTabla, name='cheque_detalle_tabla'),

    path('cheque/detalle/recibo-boleta-pago/agregar/<int:cheque_id>/', views.ReciboBoletaPagoAgregarView.as_view(), name='cheque_recibo_boleta_pago_agregar'),
    path('cheque/detalle/recibo-boleta-pago/remover/<int:cheque_id>/<pk>/', views.ReciboBoletaPagoRemoverView.as_view(), name='cheque_recibo_boleta_pago_remover'),    
    path('cheque/detalle/recibo-servicio/agregar/<int:cheque_id>/', views.ReciboServicioAgregarView.as_view(), name='cheque_recibo_servicio_agregar'),
    path('cheque/detalle/recibo-servicio/remover/<int:cheque_id>/<pk>/', views.ReciboServicioRemoverView.as_view(), name='cheque_recibo_servicio_remover'),
    path('cheque/detalle/requerimiento/agregar/<int:cheque_id>/', views.RequerimientoAgregarView.as_view(), name='cheque_requerimiento_agregar'),
    path('cheque/detalle/requerimiento/remover/<int:cheque_id>/<pk>/', views.RequerimientoRemoverView.as_view(), name='cheque_requerimiento_remover'),

]