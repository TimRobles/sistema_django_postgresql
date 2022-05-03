from django.urls import path
from . import views

app_name='recepcion_app'

urlpatterns = [
    path('visita/', views.VisitaListView.as_view(), name='visita_inicio'),
    path('visita-tabla/', views.VisitaTabla, name='visita_tabla'),
    path('visita/registrar/', views.VisitaCreateView.as_view(), name='visita_registrar'),
    path('visita/registrar-salida/<pk>/', views.VisitaRegistrarSalidaView.as_view(), name='visita_registrar_salida'),

    path('asistencia/', views.AsistenciaListView.as_view(), name='asistencia_inicio'),
    path('asistencia-tabla/', views.AsistenciaTabla, name='asistencia_tabla'),
    path('asistencia/registrar/', views.AsistenciaCreateView.as_view(), name='asistencia_registrar'),
    path('asistencia/registrar-salida/<pk>/', views.AsistenciaRegistrarSalidaView.as_view(), name='asistencia_registrar_salida'),
    
]