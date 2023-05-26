from django.urls import path
from . import views

app_name = 'cotizacion_app'

urlpatterns = [
    path('cotizacion-venta/',views.CotizacionVentaListView.as_view(),name='cotizacion_venta_inicio'),
    path('cotizacion-venta-tabla/',views.CotizacionVentaTabla,name='cotizacion_venta_tabla'),
    path('cotizacion-venta/registrar/', views.CotizacionVentaCreateView, name='cotizacion_venta_registrar'),

    path('cotizacion-venta/ver/<int:id_cotizacion>/', views.CotizacionVentaVerView.as_view(), name='cotizacion_venta_ver'),
    path('cotizacion-venta/ver/tabla/<int:id_cotizacion>/', views.CotizacionVentaVerTabla, name='cotizacion_venta_ver_tabla'),
    path('cotizacion-venta/ver/agregar-material/<int:cotizacion_id>/', views.CotizacionVentaMaterialDetalleView.as_view(), name='cotizacion_venta_agregar_material'),
    path('cotizacion-venta/ver/cliente/<pk>/', views.CotizacionVentaClienteView.as_view(), name='cotizacion_venta_cliente'),
    path('cotizacion-venta/eliminar/<pk>/', views.CotizacionVentaDeleteView.as_view(), name='cotizacion_venta_eliminar'),
    path('cotizacion-venta/anular/<pk>/', views.CotizacionVentaAnularView.as_view(), name='cotizacion_venta_anular'),
    path('cotizacion-venta/clonar/<pk>/', views.CotizacionVentaClonarView.as_view(), name='cotizacion_venta_clonar'),
    path('cotizacion-venta/vendedor/<pk>/', views.CotizacionVentaVendedorView.as_view(), name='cotizacion_venta_vendedor'),

    path('cotizacion-venta/soles/ver/<int:id_cotizacion>/', views.CotizacionVentaSolesVerView.as_view(), name='cotizacion_venta_soles_ver'),
    path('cotizacion-venta/soles/ver/tabla/<int:id_cotizacion>/', views.CotizacionVentaSolesVerTabla, name='cotizacion_venta_soles_ver_tabla'),
    
    path('cotizacion-venta/resumen/<pk>/', views.CotizacionVentaResumenView.as_view(), name='cotizacion_venta_resumen'),
    
    path('cotizacion-venta/descuento-global/<pk>/', views.CotizacionDescuentoGlobalUpdateView.as_view(), name='cotizacion_venta_descuento_global'),
    path('cotizacion-venta/descuento-global/guardar/<str:monto>/<int:id_cotizacion>/<str:abreviatura>/', views.GuardarCotizacionDescuentoGlobal, name='guardar_cotizacion_venta_descuento_global'),

    path('cotizacion-venta/observacion/<pk>/', views.CotizacionObservacionUpdateView.as_view(), name='cotizacion_venta_observacion'),
    path('cotizacion-venta/observacion/guardar/<str:texto>/<int:id_cotizacion>/<str:abreviatura>/', views.GuardarCotizacionObservacion, name='guardar_cotizacion_venta_observacion'),

    path('cotizacion-venta/otros-cargos/<pk>/', views.CotizacionOtrosCargosUpdateView.as_view(), name='cotizacion_venta_otros_cargos'),
    path('cotizacion-venta/otros-cargos/guardar/<str:monto>/<int:id_cotizacion>/<str:abreviatura>/', views.GuardarCotizacionOtrosCargos, name='guardar_cotizacion_venta_otros_cargos'),

    path('cotizacion-cliente-interlocutor/<int:id_cliente>/', views.ClienteInterlocutorView, name='cotizacion_cliente_interlocutor'),

    path('cotizacion-venta/sociedad/<pk>/', views.CotizacionSociedadUpdateView.as_view(), name='cotizacion_venta_sociedad'),
    path('cotizacion-venta/sociedad/guardar/<str:cantidad>/<int:item>/<str:abreviatura>/', views.GuardarCotizacionSociedad, name='guardar_cotizacion_venta_sociedad'),

    path('cotizacion-venta/guardar/<pk>/', views.CotizacionVentaGuardarView.as_view(), name='cotizacion_venta_guardar'),
    
    path('cotizacion-venta/reservar/<pk>/', views.CotizacionVentaReservaView.as_view(), name='cotizacion_venta_reservar'),
    path('cotizacion-venta/anular-reserva/<pk>/', views.CotizacionVentaReservaAnularView.as_view(), name='cotizacion_venta_anular_reserva'),

    path('cotizacion-venta/confirmar/<pk>/', views.CotizacionVentaConfirmarView.as_view(), name='cotizacion_venta_confirmar'),
    path('cotizacion-venta/anular-confirmar/<pk>/', views.CotizacionVentaConfirmarAnularView.as_view(), name='cotizacion_venta_anular_confirmar'),

    path('cotizacion-venta/confirmar-anticipo/<pk>/', views.CotizacionVentaConfirmarAnticipoView.as_view(), name='cotizacion_venta_confirmar_anticipo'),
    path('cotizacion-venta/anular-confirmar-anticipo/<pk>/', views.CotizacionVentaConfirmarAnticipoAnularView.as_view(), name='cotizacion_venta_anular_confirmar_anticipo'),

    path('cotizacion-venta/detalle/costeador/<pk>/', views.CotizacionVentaCosteadorDetalleView.as_view(), name='cotizacion_venta_detalle_costeador'),
    path('cotizacion-venta/detalle/eliminar/<pk>/', views.CotizacionVentaDetalleDeleteView.as_view(), name='cotizacion_venta_detalle_eliminar'),
    path('cotizacion-venta/detalle/actualizar/<pk>/', views.CotizacionVentaMaterialDetalleUpdateView.as_view(), name='cotizacion_venta_detalle_actualizar'),
    path('cotizacion-venta/detalle/oferta/<pk>/', views.CotizacionVentaMaterialDetalleOfertaView.as_view(), name='cotizacion_venta_detalle_oferta'),

    path('cotizacion-venta/pdfs/<slug>/', views.CotizacionVentaPdfsView.as_view(), name='cotizacion_venta_pdfs'),
    path('cotizacion-venta/pdf/<str:sociedad>/<slug>/', views.CotizacionVentaSociedadPdfView.as_view(), name='cotizacion_venta_pdf'),
    path('cotizacion-venta/pdf/cuentas/<str:sociedad>/<slug>/', views.CotizacionVentaSociedadCuentasPdfView.as_view(), name='cotizacion_venta_cuentas_pdf'),
    path('cotizacion-venta/pdf/cuentas/soles/<str:sociedad>/<slug>/', views.CotizacionVentaSociedadCuentasSolesPdfView.as_view(), name='cotizacion_venta_cuentas_soles_pdf'),

    path('cotizacion-venta/soles/pdfs/<slug>/', views.CotizacionVentaSolesPdfsView.as_view(), name='cotizacion_venta_soles_pdfs'),
    path('cotizacion-venta/soles/pdf/<str:sociedad>/<slug>/', views.CotizacionVentaSolesSociedadPdfView.as_view(), name='cotizacion_venta_soles_pdf'),
    path('cotizacion-venta/soles/pdf/cuentas/soles/<str:sociedad>/<slug>/', views.CotizacionVentaSolesSociedadCuentasSolesPdfView.as_view(), name='cotizacion_venta_soles_cuentas_soles_pdf'),

    path('confirmacion/ver/<int:id_confirmacion>/', views.ConfirmarVerView.as_view(), name='confirmacion_ver'),
    path('confirmacion/ver/tabla/<int:id_confirmacion>/', views.ConfirmarVerTabla, name='confirmacion_ver_tabla'),
    path('confirmacion/ver/cliente/<pk>/', views.ConfirmacionClienteView.as_view(), name='confirmacion_cliente'),
    path('confirmacion/ver/cuotas/<pk>/', views.ConfirmacionVentaVerCuotaView.as_view(), name='confirmacion_ver_cuotas'),
    path('confirmacion/cuotas/<int:id_confirmacion>/', views.ConfirmacionVentaCuotaView.as_view(), name='confirmacion_cuotas'),
    path('confirmacion/cuotas/tabla/<int:id_confirmacion>/', views.ConfirmacionVentaCuotaTabla, name='confirmacion_cuotas_tabla'),
    path('confirmacion/cuota/generar/<int:id_confirmacion>/',views.ConfirmacionVentaGenerarCuotasFormView.as_view(),name='confirmacion_cuota_generar'),
    path('confirmacion/cuota/agregar/<int:id_confirmacion>/',views.ConfirmacionVentaCuotaCreateView.as_view(),name='confirmacion_cuota_agregar'),
    path('confirmacion/cuota/actualizar/<pk>/',views.ConfirmacionVentaCuotaUpdateView.as_view(),name='confirmacion_cuota_actualizar'),
    path('confirmacion/cuota/eliminar/<pk>/',views.ConfirmacionVentaCuotaDeleteView.as_view(),name='confirmacion_cuota_eliminar'),

    path('confirmacion/',views.ConfirmacionListView.as_view(),name='confirmacion_inicio'),
    path('confirmacion/<int:id_cotizacion>/',views.ConfirmacionListView.as_view(),name='confirmacion_cotizacion_inicio'),
    path('pendiente-salida/',views.ConfirmacionPendienteSalidaView.as_view(),name='pendiente_salida'),
    path('confirmacion/forma-pago/<pk>/',views.ConfirmacionVentaFormaPagoView.as_view(),name='confirmacion_forma_pago'),
    path('confirmacion/orden-compra/<int:id_confirmacion>/',views.ConfirmacionVentaOrdenCompraCrearView.as_view(),name='confirmacion_orden_compra'),
    path('confirmacion/orden-compra/<int:id_confirmacion>/<pk>/',views.ConfirmacionVentaOrdenCompraActualizarView.as_view(),name='confirmacion_orden_compra'),
    path('confirmacion/orden-compra/eliminar/<int:id_confirmacion>/<pk>/',views.ConfirmacionOrdenCompraDeleteView.as_view(),name='confirmacion_orden_compra_eliminar'),

    path('solicitud-credito/<int:id_cotizacion>/',views.SolicitudCreditoView.as_view(),name='solicitud_credito'),
    path('solicitud-credito/tabla/<int:id_cotizacion>/',views.SolicitudCreditoTabla,name='solicitud_credito_tabla'),
    path('solicitud-credito/actualizar/<pk>/',views.SolicitudCreditoUpdateView.as_view(),name='solicitud_credito_actualizar'),
    path('solicitud-credito/eliminar/<pk>/',views.SolicitudCreditoEliminarView.as_view(),name='solicitud_credito_eliminar'),
    path('solicitud-credito/finalizar/<pk>/',views.SolicitudCreditoFinalizarView.as_view(),name='solicitud_credito_finalizar'),
    path('solicitud-credito/aprobar/<pk>/',views.SolicitudCreditoAprobarView.as_view(),name='solicitud_credito_aprobar'),
    path('solicitud-credito/rechazar/<pk>/',views.SolicitudCreditoRechazarView.as_view(),name='solicitud_credito_rechazar'),
    path('solicitud-credito/cuota/generar/<int:id_solicitud>/',views.SolicitudCreditoGenerarCuotasFormView.as_view(),name='solicitud_credito_cuota_generar'),
    path('solicitud-credito/cuota/agregar/<int:id_solicitud>/',views.SolicitudCreditoCuotaCreateView.as_view(),name='solicitud_credito_cuota_agregar'),
    path('solicitud-credito/cuota/actualizar/<pk>/',views.SolicitudCreditoCuotaUpdateView.as_view(),name='solicitud_credito_cuota_actualizar'),
    path('solicitud-credito/cuota/eliminar/<pk>/',views.SolicitudCreditoCuotaDeleteView.as_view(),name='solicitud_credito_cuota_eliminar'),
    
    path('confirmacion/nota-salida/<pk>/',views.ConfirmacionNotaSalidaView.as_view(),name='confirmacion_nota_salida'),
]
