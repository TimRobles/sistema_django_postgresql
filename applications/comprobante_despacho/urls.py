from django.urls import path
from . import views

app_name = 'comprobante_despacho_app'

urlpatterns = [
    path('guia/',views.GuiaListView.as_view(),name='guia_inicio'),
    path('guia-tabla/',views.GuiaTabla,name='guia_tabla'),

    path('guia/detalle/<int:id_guia>/',views.GuiaDetalleView.as_view(),name='guia_detalle'),
    path('guia/detalle/tabla/<int:id_guia>/',views.GuiaDetalleVerTabla,name='guia_detalle_tabla'),

    path('guia/crear/<pk>/', views.GuiaCrearView.as_view(), name='guia_crear'),
    path('guia/guardar/<pk>/', views.GuiaGuardarView.as_view(), name='guia_guardar'),
    path('guia/anular/<pk>/', views.GuiaAnularView.as_view(), name='guia_anular'),

    path('guia/motivo-traslado/<pk>/', views.GuiaMotivoTrasladoView.as_view(), name='guia_motivo_traslado'),
    path('guia/fecha-traslado/<pk>/', views.GuiaFechaTrasladoView.as_view(), name='guia_fecha_traslado'),
    path('guia/transportista/<pk>/', views.GuiaTransportistaView.as_view(), name='guia_transportista'),
    path('guia/partida/<pk>/', views.GuiaPartidaView.as_view(), name='guia_partida'),
    path('guia/destino/<pk>/', views.GuiaDestinoView.as_view(), name='guia_destino'),
    path('guia/bultos/<pk>/', views.GuiaBultosView.as_view(), name='guia_bultos'),
    path('guia/conductor/<pk>/', views.GuiaConductorView.as_view(), name='guia_conductor'),
    path('guia/cliente/<pk>/', views.GuiaClienteView.as_view(), name='guia_cliente'),
    path('guia/serie/<pk>/', views.GuiaSerieUpdateView.as_view(), name='guia_serie'),
    path('guia/cliente-interlocutor/<int:id_cliente>/', views.ClienteInterlocutorView, name='guia_cliente_interlocutor'),
    
    path('guia/nubefact/enviar/<pk>/', views.GuiaNubeFactEnviarView.as_view(), name='guia_nubefact_enviar'),
    path('guia/nubefact/detalle/<pk>/', views.GuiaNubefactRespuestaDetailView.as_view(), name='guia_nubefact_detalle'),

]
