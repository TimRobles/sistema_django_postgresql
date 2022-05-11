from django.urls import path
from applications.datos_globales.views import (
    ProvinciaView,
    DistritoView,
    DepartamentoView,
)

app_name = 'datos_globales_app'

urlpatterns = [
    path('departamento/', DepartamentoView, name='departamento'),
    path('provincia/<str:id_departamento>/', ProvinciaView, name='provincia'),
    path('distrito/<str:id_provincia>/', DistritoView, name='distrito'),
]