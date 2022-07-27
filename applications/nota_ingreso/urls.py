from django.urls import path
from . import views

app_name = 'nota_ingreso_app'

urlpatterns = [

    path('nota-ingreso/detalle/<pk>/', views.NotaIngresoDetailView.as_view(), name='nota_ingreso_detalle'),
    path('nota-ingreso/detalle/tabla/<pk>/', views.NotaIngresoDetailTabla, name='nota_ingreso_detalle_tabla'),

]