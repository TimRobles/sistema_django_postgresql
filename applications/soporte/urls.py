from django.urls import path
from . import views

app_name='soporte_app'

urlpatterns = [
    path('problema/', views.ProblemaListView.as_view(), name='problema_inicio'),
    path('problema-tabla/', views.ProblemaTabla, name='problema_tabla'),
    path('problema/registrar/', views.ProblemaCreateView.as_view(), name='problema_registrar'),
    path('problema/actualizar/<pk>/', views.ProblemaUpdateView.as_view(), name='problema_actualizar'),
    path('problema/eliminar/<pk>', views.ProblemaDeleteView.as_view(), name='problema_eliminar'),
    path('problema/notificar/<pk>/', views.ProblemaNotificarView.as_view(), name='problema_notificar'),

    path('problema-detalle/<pk>', views.ProblemaDetailView.as_view(), name='problema_detalle'),
    path('problema-detalle-tabla/<pk>', views.ProblemaDetalleTabla, name='problema_detalle_tabla'),
    path('problema-detalle/registrar/<int:problema_id>/', views.ProblemaDetalleCreateView.as_view(), name='problema_detalle_registrar'),
    path('problema-detalle/eliminar/<pk>/', views.ProblemaDetalleDeleteView.as_view(), name='problema_detalle_eliminar'),
    path('problema-detalle/detalle/actualizar/<pk>/', views.ProblemaDetalleUpdateView.as_view(), name='problema_detalle_actualizar'),
    path('problema-detalle/detalle/notasolucion/<pk>/', views.ProblemaDetalleNotaSolucionView.as_view(), name='problema_detalle_notasolucion'),
    path('problema-detalle/iniciarsolucion/<pk>/', views.ProblemaDetalleIniciarSolucionView.as_view(), name='problema_detalle_iniciar_solucion'),
    path('problema-detalle/finalizarproblema/<pk>/', views.ProblemaDetalleFinalizarProblemaView.as_view(), name='problema_detalle_finalizar_problema'),


    path('solicitud/', views.SolicitudListView.as_view(), name='solicitud_inicio'),
    path('solicitud-tabla/', views.SolicitudTabla, name='solicitud_tabla'),
    path('solicitud/registrar/', views.SolicitudCreateView.as_view(), name='solicitud_registrar'),
    path('solicitud/actualizar/<pk>/', views.SolicitudUpdateView.as_view(), name='solicitud_actualizar'),
    path('solicitud/eliminar/<pk>', views.SolicitudDeleteView.as_view(), name='solicitud_eliminar'),

    path('solicitud-detalle/<pk>', views.SolicitudDetailView.as_view(), name='solicitud_detalle'),
    path('solicitud-detalle-tabla/<pk>', views.SolicitudDetalleTabla, name='solicitud_detalle_tabla'),
    path('solicitud-detalle/registrar/<int:solicitud_id>/', views.SolicitudDetalleCreateView.as_view(), name='solicitud_detalle_registrar'),
    path('solicitud-detalle/eliminar/<pk>/', views.SolicitudDetalleDeleteView.as_view(), name='solicitud_detalle_eliminar'),
    path('solicitud-detalle/detalle/actualizar/<pk>/', views.SolicitudDetalleUpdateView.as_view(), name='solicitud_detalle_actualizar'),
    path('solicitud-detalle/solicitar/<pk>/', views.SolicitudSolicitarView.as_view(), name='solicitud_detalle_solicitar'),
    path('solicitud-detalle/aprobar/<pk>/', views.SolicitudAprobarView.as_view(), name='solicitud_detalle_aprobar'),
    path('solicitud-detalle/rechazar/<pk>/', views.SolicitudRechazarView.as_view(), name='solicitud_detalle_rechazar'),
    path('solicitud-detalle/iniciar/<pk>/', views.SolicitudIniciarView.as_view(), name='solicitud_detalle_iniciar'),
    path('solicitud-detalle/resolver/<pk>/', views.SolicitudResolverView.as_view(), name='solicitud_detalle_resolver'),

] 