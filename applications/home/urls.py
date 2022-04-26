from django.urls import path
from applications.home.views import (
    ConsultaDniView,
    ConsultaRucView,
    PanelView,
    InicioView,
    UserLogoutView,
)

app_name = 'home_app'

urlpatterns = [
    path('', PanelView.as_view(), name='home'),
    path('login/', InicioView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('consulta-ruc/<int:ruc>/', ConsultaRucView, name='consulta_ruc'),
    path('consulta-dni/<int:dni>/', ConsultaDniView, name='consulta_dni'),
]