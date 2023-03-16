from django.urls import path
from . import views

app_name = 'garantia_app'

urlpatterns = [
    path('ingreso-garantia/',views.IngresoReclamoGarantiaListView.as_view(),name='ingreso_garantia_inicio'),
    path('ingreso-garantia/registrar/', views.IngresoReclamoGarantiaCreateView, name='ingreso_garantia_registrar'),
    path('ingreso-garantia/ver/<int:id_ingreso>/', views.IngresoReclamoGarantiaVerView.as_view(), name='ingreso_garantia_ver'),
    path('ingreso-garantia/ver/tabla/<int:id_ingreso>/', views.IngresoReclamoGarantiaVerTabla, name='ingreso_garantia_ver_tabla'),

    path('ingreso-garantia/eliminar/<pk>/', views.IngresoReclamoGarantiaDeleteView.as_view(), name='ingreso_garantia_eliminar'),

    path('ingreso-garantia/cliente/<pk>/', views.IngresoReclamoGarantiaClienteView.as_view(), name='ingreso_garantia_cliente'),
    path('ingreso-garantia/encargado/<pk>/', views.IngresoReclamoGarantiaEncargadoView.as_view(), name='ingreso_garantia_encargado'),
    path('ingreso-garantia/sociedad/<pk>/', views.IngresoReclamoGarantiaSociedadView.as_view(), name='ingreso_garantia_sociedad'),
    path('ingreso-garantia/almacen/<pk>/', views.IngresoReclamoGarantiaAlmacenView.as_view(), name='ingreso_garantia_almacen'),
    path('ingreso-garantia/observacion/<pk>/', views.IngresoReclamoGarantiaObservacionUpdateView.as_view(), name='ingreso_garantia_observacion'),
    path('ingreso-garantia/guardar/<pk>/', views.IngresoReclamoGarantiaGuardarView.as_view(), name='ingreso_garantia_guardar'),
    path('ingreso-garantia/control/<pk>/', views.IngresoControlCalidadView.as_view(), name='ingreso_garantia_control'),
    path('ingreso-garantia/agregar-material/<int:id_ingreso>/', views.IngresoReclamoGarantiaMaterialView.as_view(), name='ingreso_garantia_agregar_material'),
    path('ingreso-garantia/editar-material/<pk>/', views.IngresoReclamoGarantiaMaterialUpdateView.as_view(), name='ingreso_garantia_editar_material'),
    path('ingreso-garantia/eliminar-material/<pk>/', views.IngresoReclamoGarantiaMaterialDeleteView.as_view(), name='ingreso_garantia_eliminar_material'),
    path('ingreso-garantia/pdf/<int:id_ingreso>/', views.IngresoReclamoGarantiaPdfView.as_view(), name='ingreso_garantia_pdf'),

    path('serie-ingreso-garantia/ver/<int:id_ingreso>/', views.SerieIngresoReclamoGarantiaView.as_view(), name='serie_ingreso_garantia_ver'),
    path('serie-ingreso-garantia/ver/<int:id_ingreso>/<int:id_ingreso_detalle>/', views.SerieIngresoReclamoGarantiaDetalleView.as_view(), name='serie_ingreso_garantia_ver'),
    path('serie-ingreso-garantia/tabla/<int:id_ingreso>/', views.SerieIngresoReclamoGarantiaTabla, name='serie_ingreso_garantia_tabla'),
    path('serie-ingreso-garantia/tabla/<int:id_ingreso>/<int:id_ingreso_detalle>/', views.SerieIngresoReclamoGarantiaTabla, name='serie_ingreso_garantia_tabla'),
    path('serie-ingreso-garantia/comentario/<pk>/', views.SerieIngresoReclamoGarantiaDetalleUpdateView.as_view(), name='serie_ingreso_garantia_comentario'),
    path('serie-ingreso-garantia/eliminar/<pk>/', views.SerieIngresoReclamoGarantiaMaterialDeleteView.as_view(), name='serie_ingreso_garantia_eliminar'),

    path('control-ingreso-garantia/',views.ControlCalidadReclamoGarantiaListView.as_view(),name='control_garantia_inicio'),
    path('control-ingreso-garantia/ver/<int:id_control>/', views.ControlCalidadReclamoGarantiaVerView.as_view(), name='control_garantia_ver'),
    path('control-ingreso-garantia/ver/tabla/<int:id_control>/', views.ControlCalidadReclamoGarantiaVerTabla, name='control_garantia_ver_tabla'),
    path('control-ingreso-garantia/observacion/<pk>/', views.ControlCalidadReclamoGarantiaObservacionUpdateView.as_view(), name='control_garantia_observacion'),
    path('control-ingreso-garantia/salida/<pk>/', views.ControlSalidaGarantiaView.as_view(), name='control_garantia_salida'),
    
    path('serie-control-ingreso-garantia/ver/<int:id_ingreso_detalle>/', views.SerieControlCalidadReclamoGarantiaDetalleView.as_view(), name='serie_contro_ingreso_garantia_ver'),
    path('serie-control-ingreso-garantia/tabla/<int:id_ingreso_detalle>/', views.SerieControlCalidadReclamoGarantiaTabla, name='serie_contro_ingreso_garantia_tabla'),

    path('salida-garantia/<int:id_control>/',views.SalidaReclamoGarantiaListView.as_view(),name='salida_garantia_inicio'),
    path('salida-garantia/ver/<int:id_salida>/', views.SalidaReclamoGarantiaVerView.as_view(), name='salida_garantia_ver'),
    path('salida-garantia/ver/tabla/<int:id_salida>/', views.SalidaReclamoGarantiaVerTabla, name='salida_garantia_ver_tabla'),

    path('salida-garantia/eliminar/<pk>/', views.SalidadReclamoGarantiaDeleteView.as_view(), name='salida_garantia_eliminar'),

    path('salida-garantia/encargado/<pk>/', views.SalidaReclamoGarantiaEncargadoView.as_view(), name='salida_garantia_encargado'),
    path('salida-garantia/observacion/<pk>/', views.SalidaReclamoGarantiaObservacionUpdateView.as_view(), name='salida_garantia_observacion'),

]
