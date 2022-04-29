from django.urls import path
from applications.home.views import (
    PanelView,
    InicioView,
    UserLogoutView,
    OlvideContrasenaView,
    RecuperarContrasenaView
)

app_name = 'home_app'

urlpatterns = [
    path('', PanelView.as_view(), name='home'),
    path('login/', InicioView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('olvide-contraseña/', OlvideContrasenaView.as_view(), name='olvide_contraseña'),
    path('recuperar-contraseña/', RecuperarContrasenaView.as_view(), name='recuperar_contraseña'),
]