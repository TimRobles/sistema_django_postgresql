from django.urls import path
from . import views

app_name = 'nota_app'

urlNotaCredito = [
    path('nota_credito/',views.NotaCreditoView.as_view(),name='nota_credito_inicio'),
    path('nota-credito/detalle/<pk>/', views.NotaCreditoDetailView.as_view(), name='nota_credito_detalle'),
    path('nota-credito/detalle/tabla/<int:id>/', views.NotaCreditoDetailTabla, name='nota_credito_detalle_tabla'),

]


urlpatterns = [

] + urlNotaCredito
