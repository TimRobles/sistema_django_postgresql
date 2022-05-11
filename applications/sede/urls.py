from django.urls import path
from . import views

app_name='sede_app'

urlpatterns = [
    path('sede/', views.SedeListView.as_view(), name='sede_inicio'),
    path('sede-tabla/', views.SedeTabla, name='sede_tabla'),
    path('sede/registrar/', views.SedeCreateView.as_view(), name='sede_registrar'),
    path('sede/actualizar/<pk>/', views.SedeUpdateView.as_view(), name='sede_actualizar'),
    path('sede/baja/<pk>/', views.SedeDarBajaView.as_view(), name='sede_baja'),
    path('sede/alta/<pk>/', views.SedeDarAltaView.as_view(), name='sede_alta'),
]