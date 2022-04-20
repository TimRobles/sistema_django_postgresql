from unicodedata import name
from django.urls import path
from django.contrib import admin

from applications.usuario.views import(
    DatosUsuarioView,
    HistoricoUserTabla,
    UserPasswordView,
    HistoricoUserDarBajaView,
    HistoricoUserListView,
    HistoricoUserDarAltaView,
)

app_name='usuario'

urlpatterns = [
    path('actualizar-datos/',DatosUsuarioView.as_view(), name='actualizar_datos'),   
    path('actualizar-contraseña/',UserPasswordView.as_view(), name='actualizar_contraseña'),

    path('historico-usuarios/', HistoricoUserListView.as_view(),name='historico_usuarios'),
    path('historico-usuarios-tabla/', HistoricoUserTabla,name='historico_usuarios_tabla'),
    path('baja-usuarios/<pk>/', HistoricoUserDarBajaView.as_view(),name='baja_usuarios'),
    path('alta-usuarios/<int:usuario>/', HistoricoUserDarAltaView.as_view(),name='alta_usuarios'),

]