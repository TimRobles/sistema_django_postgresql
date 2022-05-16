from django.urls import path
from . import views

app_name='material_app'

urlpatterns = [
    path('modelo/', views.ModeloListView.as_view(), name='modelo_inicio'),
    path('modelo-tabla/', views.ModeloTabla, name='modelo_tabla'),
    path('modelo/registrar/', views.ModeloCreateView.as_view(), name='modelo_registrar'),
    path('modelo/actualizar/<pk>/', views.ModeloUpdateView.as_view(), name='modelo_actualizar'),

    path('marca/', views.MarcaListView.as_view(), name='marca_inicio'),
    path('marca-tabla/', views.MarcaTabla, name='marca_tabla'),
    path('marca/registrar/', views.MarcaCreateView.as_view(), name='marca_registrar'),
    path('marca/actualizar/<pk>/', views.MarcaUpdateView.as_view(), name='marca_actualizar'),
]
