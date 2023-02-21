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
    path('ingreso-garantia/observacion/<pk>/', views.IngresoReclamoGarantiaObservacionUpdateView.as_view(), name='ingreso_garantia_observacion'),

    path('ingreso-garantia/agregar-material/<int:id_ingreso>/', views.IngresoReclamoGarantiaMaterialView.as_view(), name='ingreso_garantia_agregar_material'),


]
