from django.urls import path
from . import views

app_name = 'comprobante_despacho_app'

urlpatterns = [ 
    path('guia/',views.GuiaListView.as_view(),name='guia_inicio'),
    path('guia-tabla/',views.GuiaTabla,name='guia_tabla'),    
    
    path('guia/detalle/<int:id_guia>/',views.GuiaDetalleView.as_view(),name='guia_detalle'),
    path('guia/detalle/tabla/<int:id_guia>/',views.GuiaDetalleVerTabla,name='guia_detalle_tabla'),

    path('guia/crear/<pk>/', views.GuiaCrearView.as_view(), name='guia_crear'),

    path('guia/transportista/<pk>/', views.GuiaTransportistaView.as_view(), name='guia_transportista'),
    path('guia/partida/<pk>/', views.GuiaPartidaView.as_view(), name='guia_partida'),
    path('guia/destino/<pk>/', views.GuiaDestinoView.as_view(), name='guia_destino'),

]