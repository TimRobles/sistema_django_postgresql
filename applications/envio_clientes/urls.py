from django.urls import path
from . import views

app_name='transportistas_app'

urlpatterns = [
    path('transportista/', views.TransportistaListView.as_view(), name='transportista_inicio'),
    path('transportista-tabla/', views.TransportistaTabla, name='transportista_tabla'),
    path('transportista/registrar/', views.TransportistaCreateView.as_view(), name='transportista_registrar'),
    path('transportista/actualizar/<pk>/', views.TransportistaUpdateView.as_view(), name='transportista_actualizar'),
]