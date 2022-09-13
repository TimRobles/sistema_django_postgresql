from django.urls import path
from . import views

app_name = 'cobranza_app'

urlpatterns = [

    path('linea-credito/',views.LineaCreditoView.as_view(),name='linea_credito_inicio'),
    path('linea-credito-tabla/',views.LineaCreditoTabla,name='linea_credito_tabla'),
    path('linea-credito/registrar/', views.LineaCreditoCreateView.as_view(), name='linea_credito_registrar'),
    path('linea-credito/actualizar/<pk>/', views.LineaCreditoUpdateView.as_view(), name='linea_credito_actualizar'),

 ]