from django.urls import path
from . import views

app_name = 'nota_app'

urlNotaCredito = [
    path('nota_credito/',views.NotaCreditoView.as_view(),name='nota_credito_inicio'),
    path('nota_credito/tabla/',views.NotaCreditoTabla,name='nota_credito_tabla'),
    path('nota-credito/detalle/<pk>/', views.NotaCreditoDetailView.as_view(), name='nota_credito_detalle'),
    path('nota-credito/detalle/tabla/<int:id>/', views.NotaCreditoDetailTabla, name='nota_credito_detalle_tabla'),
    path('nota_credito/crear/',views.NotaCreditoCreateView.as_view(),name='nota_credito_crear'),
    path('nota_credito/eliminar/<pk>/',views.NotaCreditoDeleteView.as_view(),name='nota_credito_eliminar'),
    path('nota-credito/direccion/<int:id_nota>/<pk>/', views.NotaCreditoDireccionView.as_view(), name='nota_credito_direccion'),
    path('nota-credito/serie/<pk>/', views.NotaCreditoSerieUpdateView.as_view(), name='nota_credito_serie'),
    path('nota-credito/tipo/<pk>/', views.NotaCreditoTipoUpdateView.as_view(), name='nota_credito_tipo'),
    path('nota-credito/guardar/<pk>/', views.NotaCreditoGuardarView.as_view(), name='nota_credito_guardar'),
    path('nota-credito/anular/<pk>/', views.NotaCreditoAnularView.as_view(), name='nota_credito_anular'),
    path('nota-credito/nubefact/enviar/<pk>/', views.NotaCreditoNubeFactEnviarView.as_view(), name='nota_credito_nubefact_enviar'),
    path('nota-credito/nubefact/anular/<pk>/', views.NotaCreditoNubeFactAnularView.as_view(), name='nota_credito_nubefact_anular'),
    path('nota-credito/nubefact/detalle/<pk>/', views.NotaCreditoNubefactRespuestaDetailView.as_view(), name='nota_credito_nubefact_detalle'),
    path('nota-credito/nubefact/consultar/<pk>/', views.NotaCreditoNubefactConsultarView.as_view(), name='nota_credito_nubefact_consultar'),
    path('nota-credito/observacion/<pk>/', views.NotaCreditoObservacionUpdateView.as_view(), name='nota_credito_observacion'),

    path('nota-credito/ver/cuotas/<pk>/', views.NotaCreditoVerCuotaView.as_view(), name='nota_credito_ver_cuotas'),
    path('nota-credito/cuotas/<int:id_nota_credito>/', views.NotaCreditoCuotaView.as_view(), name='nota_credito_cuotas'),
    path('nota-credito/cuotas/tabla/<int:id_nota_credito>/', views.NotaCreditoCuotaTabla, name='nota_credito_cuotas_tabla'),
    path('nota-credito/cuota/generar/<int:id_nota_credito>/',views.NotaCreditoGenerarCuotasFormView.as_view(),name='nota_credito_cuota_generar'),
    path('nota-credito/cuota/agregar/<int:id_nota_credito>/',views.NotaCreditoCuotaCreateView.as_view(),name='nota_credito_cuota_agregar'),
    path('nota-credito/cuota/actualizar/<pk>/',views.NotaCreditoCuotaUpdateView.as_view(),name='nota_credito_cuota_actualizar'),
    path('nota-credito/cuota/eliminar/<pk>/',views.NotaCreditoCuotaDeleteView.as_view(),name='nota_credito_cuota_eliminar'),

    path('nota-devolucion/generar/<pk>/',views.GenerarNotaDevolucionView.as_view(),name='nota_devolucion_generar'),
    path('nota-devolucion/finalizar/<pk>/',views.FinalizarNotaDevolucionView.as_view(),name='nota_devolucion_finalizar'),
    path('nota-devolucion/inicio/',views.NotaDevolucionView.as_view(),name='nota_devolucion_inicio'),
    path('nota-devolucion/tabla/',views.NotaDevolucionTabla,name='nota_devolucion_tabla'),
    path('nota-devolucion/lista/<pk>/',views.NotaDevolucionListaView.as_view(),name='nota_devolucion_lista'),
    path('nota-devolucion/detalle/<pk>/', views.NotaDevolucionDetailView.as_view(), name='nota_devolucion_detalle'),
    path('nota-devolucion/detalle/tabla/<int:id>/', views.NotaDevolucionDetailTabla, name='nota_devolucion_detalle_tabla'),
    path('nota-devolucion/observacion/<pk>/',views.NotaDevolucionObservacionesUpdateView.as_view(),name='nota_devolucion_observacion'),
    path('nota-devolucion/eliminar/<pk>/',views.NotaDevolucionDeleteView.as_view(),name='nota_devolucion_eliminar'),
    
    path('nota-devolucion/detalle/actualizar/<pk>/',views.NotaDevolucionDetalleUpdateView.as_view(),name='nota_devolucion_detalle_actualizar'),
    
]

urlNotaCreditoDetalle = [
    path('nota-credito/agregar-material/<int:nota_id>/', views.NotaCreditoMaterialDetalleView.as_view(), name='nota_credito_agregar_material'),
    path('nota-credito-detalle/actualizar/<pk>/', views.NotaCreditoDetalleUpdateView.as_view(), name='nota_credito_detalle_actualizar'),
    path('nota-credito-detalle/actualizar/descripcion/<pk>/', views.NotaCreditoDescripcionUpdateView.as_view(), name='nota_credito_detalle_actualizar_descripcion'),
    path('nota-credito-detalle/eliminar/<pk>/', views.NotaCreditoDetalleDeleteView.as_view(), name='nota_credito_detalle_eliminar'),
]


urlpatterns = [

] + urlNotaCredito + urlNotaCreditoDetalle
