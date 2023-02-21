from django.urls import path
from . import views

app_name = 'nota_app'

urlNotaCredito = [
    path('nota_credito/',views.NotaCreditoView.as_view(),name='nota_credito_inicio'),
    path('nota_credito/tabla/',views.NotaCreditoTabla,name='nota_credito_tabla'),
    path('nota-credito/detalle/<pk>/', views.NotaCreditoDetailView.as_view(), name='nota_credito_detalle'),
    path('nota-credito/detalle/tabla/<int:id>/', views.NotaCreditoDetailTabla, name='nota_credito_detalle_tabla'),
    path('nota_credito/crear/',views.NotaCreditoCreateView.as_view(),name='nota_credito_crear'),
    path('nota_credito/eliminar/<pk>/',views.NotaCreditoDeleteView.as_view(),name='nota_credito_eliminar'),
    path('nota-credito/direccion/<int:id_nota>/<pk>/', views.NotaCreditoDireccionView.as_view(), name='nota_credito_direccion'),
]


urlpatterns = [

] + urlNotaCredito
