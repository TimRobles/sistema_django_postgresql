from unicodedata import name
from django.urls import path
from django.contrib import admin

from . import views

app_name='usuario_app'

urlpatterns = [
    path('actualizar-datos/', views.DatosUsuarioView.as_view(), name='actualizar_datos'),   
    path('actualizar-contraseña/', views.UserPasswordView.as_view(), name='actualizar_contraseña'),

    path('historico-usuarios/', views.HistoricoUserListView.as_view(),name='historico_usuarios'),
    path('historico-usuarios-tabla/', views.HistoricoUserTabla,name='historico_usuarios_tabla'),
    path('historico-usuarios-detalle/<pk>/', views.HistoricoDetailView.as_view(),name='historico_usuarios_detalle'),
    path('historico-usuarios-detalle-tabla/<pk>/', views.HistoricoDetailTabla, name='historico_usuarios_detalle_tabla'),

    path('historico-usuarios/registrar/', views.HistoricoUserCreateView.as_view(),name='historico_usuarios_registrar'),
    path('baja-usuarios/<pk>/', views.HistoricoUserDarBajaView.as_view(),name='baja_usuarios'),
    path('alta-usuarios/<int:usuario>/', views.HistoricoUserDarAltaView.as_view(),name='alta_usuarios'),

    path('vacaciones/', views.VacacionesListView.as_view(), name='vacaciones_inicio'),
    path('vacaciones-tabla/', views.VacacionesTabla, name='vacaciones_tabla'),
    path('vacaciones/registrar/', views.VacacionesCreateView.as_view(), name='vacaciones_registrar'),

    path('vacaciones/detalle/<pk>/', views.VacacionesDetailView.as_view(), name='vacaciones_detalle'),
    path('vacaciones/detalle-tabla/<pk>/', views.VacacionesDetailTabla, name='vacaciones_detalle_tabla'),
    path('vacaciones/detalle/registrar/<pk>/', views.VacacionesDetalleCreateView.as_view(), name='vacaciones_detalle_registrar'),
    path('vacaciones/detalle/actualizar/<pk>/', views.VacacionesDetalleUpdateView.as_view(), name='vacaciones_detalle_actualizar'),
    
    path('vacaciones/detalle/eliminar/<pk>/', views.VacacionesDetalleDeleteView.as_view(), name='vacaciones_detalle_eliminar'),

]