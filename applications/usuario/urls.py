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
    VacacionesCreateView,
    HistoricoDetailTabla,
    VacacionesListView,
    VacacionesTabla,
    VacacionesDetailView,
    VacacionesDetailTabla,
    VacacionesDetalleCreateView,
    VacacionesDetalleUpdateView,
    VacacionesDetalleDeleteView,
    VacacionesActualizarView,
    VacacionesTerminarView,
)

app_name='usuario_app'

urlpatterns = [
    path('actualizar-datos/',DatosUsuarioView.as_view(), name='actualizar_datos'),   
    path('actualizar-contraseña/',UserPasswordView.as_view(), name='actualizar_contraseña'),

    path('historico-usuarios/', HistoricoUserListView.as_view(),name='historico_usuarios'),
    path('historico-usuarios-tabla/', HistoricoUserTabla,name='historico_usuarios_tabla'),
    path('historico-usuarios-detalle/<pk>/', HistoricoDetailView.as_view(),name='historico_usuarios_detalle'),
    path('historico-usuarios-detalle-tabla/<pk>/', HistoricoDetailTabla, name='historico_usuarios_detalle_tabla'),

    path('historico-usuarios/registrar/', HistoricoUserCreateView.as_view(),name='historico_usuarios_registrar'),
    path('baja-usuarios/<pk>/', HistoricoUserDarBajaView.as_view(),name='baja_usuarios'),
    path('alta-usuarios/<int:usuario>/', HistoricoUserDarAltaView.as_view(),name='alta_usuarios'),

    path('vacaciones/', VacacionesListView.as_view(), name='vacaciones_inicio'),
    path('vacaciones-tabla/', VacacionesTabla, name='vacaciones_tabla'),
    path('vacaciones/registrar/', VacacionesCreateView.as_view(), name='vacaciones_registrar'),
    path('vacaciones/actualizar/<pk>/', VacacionesActualizarView.as_view(), name='vacaciones_actualizar'),

    path('vacaciones/detalle/<pk>/', VacacionesDetailView.as_view(), name='vacaciones_detalle'),
    path('vacaciones/detalle-tabla/<pk>/', VacacionesDetailTabla, name='vacaciones_detalle_tabla'),
    path('vacaciones/detalle/registrar/<pk>/', VacacionesDetalleCreateView.as_view(), name='vacaciones_detalle_registrar'),
    path('vacaciones/detalle/actualizar/<pk>/', VacacionesDetalleUpdateView.as_view(), name='vacaciones_detalle_actualizar'),
    path('vacaciones/detalle/eliminar/<pk>/', VacacionesDetalleDeleteView.as_view(), name='vacaciones_detalle_eliminar'),
    
    path('vacaciones/terminar/<pk>/', VacacionesTerminarView.as_view(), name='vacaciones_terminar'),
    
]