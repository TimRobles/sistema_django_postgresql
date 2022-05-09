from django.urls import path
from . import views

app_name='colaborador_app'

urlpatterns = [
    path('datos-contrato-planilla/', views.DatosContratoPlanillaListView.as_view(), name='datos_contrato_planilla_inicio'),
    path('datos-contrato-planilla-tabla/', views.DatosContratoPlanillaTabla, name='datos_contrato_planilla_tabla'),
    path('datos-contrato-planilla/registrar/', views.DatosContratoPlanillaCreateView.as_view(), name='datos_contrato_planilla_registrar'),    
]