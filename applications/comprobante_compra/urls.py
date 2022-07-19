from django.urls import path
from . import views

app_name = 'comprobante_compra_app'

urlpatterns = [

    path('comprobante-compra-pi/lista/', views.ComprobanteCompraPIListView.as_view(), name='comprobante_compra_pi_lista'),

]