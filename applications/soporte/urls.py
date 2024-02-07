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

    path('problema_detalle/<pk>', views.ProblemaDetailView.as_view(), name='problema_detalle'),
    path('problema_detalle-tabla/<pk>', views.ProblemaDetalleTabla, name='problema_detalle_tabla'),
    path('problema_detalle/registrar/<int:problema_id>/', views.ProblemaDetalleCreateView.as_view(), name='problema_detalle_registrar'),
    path('problema_detalle/eliminar/<pk>/', views.ProblemaDetalleDeleteView.as_view(), name='problema_detalle_eliminar'),
    path('problema_detalle/detalle/actualizar/<pk>/', views.ProblemaDetalleUpdateView.as_view(), name='problema_detalle_actualizar'),

    path('solicitud/', views.SolicitudListView.as_view(), name='solicitud_inicio'),
    path('solicitud-tabla/', views.SolicitudTabla, name='solicitud_tabla'),
    path('solicitud/registrar/', views.SolicitudCreateView.as_view(), name='solicitud_registrar'),
    path('solicitud/actualizar/<pk>/', views.SolicitudUpdateView.as_view(), name='solicitud_actualizar'),
    path('solicitud/eliminar/<pk>', views.SolicitudDeleteView.as_view(), name='solicitud_eliminar'),

    path('solicitud_detalle/<pk>', views.SolicitudDetailView.as_view(), name='solicitud_detalle'),
    path('solicitud_detalle-tabla/<pk>', views.SolicitudDetalleTabla, name='solicitud_detalle_tabla'),
    path('solicitud_detalle/registrar/<int:solicitud_id>/', views.SolicitudDetalleCreateView.as_view(), name='solicitud_detalle_registrar'),
    path('solicitud_detalle/eliminar/<pk>/', views.SolicitudDetalleDeleteView.as_view(), name='solicitud_detalle_eliminar'),
    path('solicitud_detalle/detalle/actualizar/<pk>/', views.SolicitudDetalleUpdateView.as_view(), name='solicitud_detalle_actualizar'),

] 