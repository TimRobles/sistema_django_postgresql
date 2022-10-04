from django.urls import path
from applications.home.views import (
    CalculoItemLineaView,
    ConsultaDniView,
    ConsultaRucView,
    DistanciaGeoLocalizacion,
    PanelView,
    InicioView,
    PruebaGeolocalizacion,
    UserLogoutView,
    OlvideContrasenaView,
    RecuperarContrasenaView,
    PruebaPdfView,
    consulta,
)

app_name = 'home_app'

urlpatterns = [
    path('', PanelView.as_view(), name='home'),
    path('consulta/', consulta, name='consulta'),
    path('login/', InicioView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('consulta-ruc/<str:ruc>/', ConsultaRucView, name='consulta_ruc'),
    path('consulta-dni/<str:dni>/', ConsultaDniView, name='consulta_dni'),
    path('olvide-contraseña/', OlvideContrasenaView.as_view(), name='olvide_contraseña'),
    path('recuperar-contraseña/', RecuperarContrasenaView.as_view(), name='recuperar_contraseña'),
    path('prueba-geolocalizacion', PruebaGeolocalizacion.as_view()),
    path('distancia-geolocalizacion/<str:longitud>/<str:latitud>/<int:sede_id>/', DistanciaGeoLocalizacion),
    path('probando/pdf/<pk>/', PruebaPdfView.as_view(), name='probando_pdf'),
    path('calculo-item-linea/<str:cantidad>/<str:precio_unitario_con_igv>/<str:precio_final_con_igv>/<str:valor_igv>/<int:tipo_igv>/', CalculoItemLineaView, name='calculo_item_linea'),
]
