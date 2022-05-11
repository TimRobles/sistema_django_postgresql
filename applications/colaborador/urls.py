from django.urls import path
from . import views

app_name='colaborador_app'

urlpatterns = [
    path('datos-contrato-planilla/', views.DatosContratoPlanillaListView.as_view(), name='datos_contrato_planilla_inicio'),
    path('datos-contrato-planilla-tabla/', views.DatosContratoPlanillaTabla, name='datos_contrato_planilla_tabla'),
    path('datos-contrato-planilla/registrar/', views.DatosContratoPlanillaCreateView.as_view(), name='datos_contrato_planilla_registrar'),    
    path('datos-contrato-planilla/actualizar/<pk>/', views.DatosContratoPlanillaUpdateView.as_view(), name='datos_contrato_planilla_actualizar'),    
    path('datos-contrato-planilla/baja/<pk>/', views.DatosContratoPlanillaDarBajaView.as_view(), name='datos_contrato_planilla_baja'),    

    path('datos-contrato-honorarios/', views.DatosContratoHonorariosListView.as_view(), name='datos_contrato_honorarios_inicio'),
    path('datos-contrato-honorarios-tabla/', views.DatosContratoHonorariosTabla, name='datos_contrato_honorarios_tabla'),
    path('datos-contrato-honorarios/registrar/', views.DatosContratoHonorariosCreateView.as_view(), name='datos_contrato_honorarios_registrar'),    
    path('datos-contrato-honorarios/actualizar/<pk>/', views.DatosContratoHonorariosUpdateView.as_view(), name='datos_contrato_honorarios_actualizar'),    
    path('datos-contrato-honorarios/baja/<pk>/', views.DatosContratoHonorariosDarBajaView.as_view(), name='datos_contrato_honorarios_baja'),    
]