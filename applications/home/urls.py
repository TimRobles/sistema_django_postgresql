from django.urls import path
from applications.home.views import (
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
)

app_name = 'home_app'

urlpatterns = [
    path('', PanelView.as_view(), name='home'),
    path('login/', InicioView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('consulta-ruc/<str:ruc>/', ConsultaRucView, name='consulta_ruc'),
    path('consulta-dni/<str:dni>/', ConsultaDniView, name='consulta_dni'),
    path('olvide-contraseña/', OlvideContrasenaView.as_view(), name='olvide_contraseña'),
    path('recuperar-contraseña/', RecuperarContrasenaView.as_view(), name='recuperar_contraseña'),
    path('prueba-geolocalizacion', PruebaGeolocalizacion.as_view()),
    path('distancia-geolocalizacion/<str:longitud>/<str:latitud>/<int:sede_id>/', DistanciaGeoLocalizacion),
    path('probando/pdf/<pk>/', PruebaPdfView.as_view(), name='probando_pdf'),
]
