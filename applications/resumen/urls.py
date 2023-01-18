from django.urls import path
from . import views

app_name = 'resumen_app'

urlpatterns = [
    path('resumen-total/', views.ListaRequerimientoMaterialListView.as_view(), name='resumen_total'),
    path('resumen-facturas-rechazadas/', views.ListaRequerimientoMaterialListView.as_view(), name='resumen_facturas_rechazadas'),
]
