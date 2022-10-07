from django.urls import path
from . import views

app_name='logistica_app'

urlpatterns = [

    path('solicitud-prestamo-materiales/', views.SolicitudPrestamoMaterialesListView.as_view(), name='solicitud_prestamo_materiales_inicio'),
    path('solicitud-prestamo-materiales-tabla/', views.SolicitudPrestamoMaterialesTabla, name='solicitud_prestamo_materiales_tabla'),
    path('solicitud-prestamo-materiales/registrar/', views.SolicitudPrestamoMaterialesCreateView.as_view(), name='solicitud_prestamo_materiales_registrar'),
    path('solicitud-prestamo-materiales/actualizar/<pk>', views.SolicitudPrestamoMaterialesUpdateView.as_view(), name='solicitud_prestamo_materiales_actualizar'),
    path('solicitud-prestamo-materiales/finalizar/<pk>/', views.SolicitudPrestamoMaterialesFinalizarView.as_view(), name='solicitud_prestamo_materiales_finalizar'),
    path('solicitud-prestamo-materiales/confirmar/<pk>/', views.SolicitudPrestamoMaterialesConfirmarView.as_view(), name='solicitud_prestamo_materiales_confirmar'),
    # path('solicitud-prestamo-materiales/eliminar/<pk>', views.SolicitudPrestamoMaterialesDeleteView.as_view(), name='solicitud-prestamo-materiales_eliminar'),
    path('solicitud-prestamo-materiales/detalle/<pk>/', views.SolicitudPrestamoMaterialesDetailView.as_view(), name='solicitud_prestamo_materiales_detalle'),
    path('solicitud-prestamo-materiales/detalle-tabla/<pk>/', views.SolicitudPrestamoMaterialesDetailTabla, name='solicitud_prestamo_materiales_detalle_tabla'),
    path('solicitud-prestamo-materiales-detalle/registrar/<int:solicitud_prestamo_materiales_id>/', views.SolicitudPrestamoMaterialesDetalleCreateView.as_view(), name='solicitud_prestamo_materiales_detalle_registrar'),
    path('solicitud-prestamo-materiales-detalle/imprimir/<pk>/', views.SolicitudPrestamoMaterialesDetalleImprimirView.as_view(), name='solicitud_prestamo_materiales_detalle_imprimir'),
    path('solicitud-prestamo-materiales-detalle/actualizar/<pk>/', views.SolicitudPrestamoMaterialesDetalleUpdateView.as_view(), name='solicitud_prestamo_materiales_detalle_actualizar'),
    path('solicitud-prestamo-materiales-detalle/eliminar/<pk>/', views.SolicitudPrestamoMaterialesDetalleDeleteView.as_view(), name='solicitud_prestamo_materiales_detalle_eliminar'),
    path('solicitud-prestamo-materiales-detalle/archivo/agregar/<int:solicitud_prestamo_materiales_id>/', views.DocumentoSolicitudPrestamoMaterialesCreateView.as_view(), name='solicitud_prestamo_materiales_documento_agregar'),
    path('solicitud-prestamo-materiales-detalle/archivo/eliminar/<pk>/', views.DocumentoSolicitudPrestamoMaterialesDeleteView.as_view(), name='solicitud_prestamo_materiales_documento_eliminar'),
    path('cliente-interlocutor/<str:id_cliente_interlocutor>/', views.ClienteView, name='cliente_interlocutor'),

    path('despacho/',views.DespachoListView.as_view(),name='despacho_inicio'),
    path('despacho-tabla/',views.DespachoTabla,name='despacho_tabla'),    
    
    path('despacho/detalle/<int:id_despacho>/',views.DespachoDetalleView.as_view(),name='despacho_detalle'),
    path('despacho/detalle/tabla/<int:id_despacho>/',views.DespachoDetalleVerTabla,name='despacho_detalle_tabla'),

]