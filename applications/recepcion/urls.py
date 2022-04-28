from django.urls import path
from . import views

app_name='visita_app'

urlpatterns = [
    path('visita/', views.VisitaListView.as_view(), name='visita_inicio'),
    path('visita-tabla/', views.VisitaTabla, name='visita_tabla'),
    path('visita/registrar/', views.VisitaCreateView.as_view(), name='visita_registrar'),
    path('visita/registrar-salida/<pk>/', views.VisitaRegistrarSalidaView.as_view(), name='visita_registrar_salida'),
]