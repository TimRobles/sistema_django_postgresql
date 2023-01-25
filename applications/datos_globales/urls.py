from django.urls import path
from applications.datos_globales.views import (
    DistritoJsonView,
    ProvinciaView,
    DistritoView,
    DepartamentoView,
)
from . import views

app_name = 'datos_globales_app'

urlpatterns = [
    path('departamento/', DepartamentoView, name='departamento'),
    path('provincia/<str:id_departamento>/', ProvinciaView, name='provincia'),
    path('distrito/<str:id_provincia>/', DistritoView, name='distrito'),
    path('distrito-json/', DistritoJsonView, name='distrito_json'),
    
    path('tipo-cambio/', views.TipoCambioListView.as_view(), name='tipo_cambio_inicio'),
    path('tipo-cambio-tabla/', views.TipoCambioTabla, name='tipo_cambio_tabla'),
    path('tipo-cambio/registrar/', views.TipoCambioCreateView.as_view(), name='tipo_cambio_registrar'),
    path('tipo-cambio/actualizar/<pk>/', views.TipoCambioUpdateView.as_view(), name='tipo_cambio_actualizar'),
    path('tipo-cambio/baja/<pk>/', views.TipoCambioDeleteView.as_view(), name='tipo_cambio_eliminar'),
    
    path('tipo-cambio-sunat/', views.TipoCambioSunatView.as_view(), name='tipo_cambio_sunat_inicio'),
]