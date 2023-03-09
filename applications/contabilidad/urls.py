from django.urls import path
from . import views

app_name='contabilidad_app'

urlpatterns = [
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

]