from unicodedata import name
from django.urls import path
from django.contrib import admin

from applications.usuario.views import(
    DatosUsuarioView,
    HistoricoUserCreateView,
    HistoricoUserTabla,
    UserPasswordView,
    HistoricoUserDarBajaView,
    HistoricoUserListView,
    HistoricoUserDarAltaView,
    HistoricoDetailView,
)

app_name='usuario_app'

urlpatterns = [
    path('actualizar-datos/',DatosUsuarioView.as_view(), name='actualizar_datos'),   
    path('actualizar-contraseña/',UserPasswordView.as_view(), name='actualizar_contraseña'),

    path('historico-usuarios/', HistoricoUserListView.as_view(),name='historico_usuarios'),
    path('historico-usuarios-tabla/', HistoricoUserTabla,name='historico_usuarios_tabla'),
    path('historico-usuarios-detalle/<pk>/', HistoricoDetailView.as_view(),name='historico_usuarios_detalle'),
    path('historico-usuarios/registrar/', HistoricoUserCreateView.as_view(),name='historico_usuarios_registrar'),

    path('baja-usuarios/<pk>/', HistoricoUserDarBajaView.as_view(),name='baja_usuarios'),
    path('alta-usuarios/<int:usuario>/', HistoricoUserDarAltaView.as_view(),name='alta_usuarios'),

]