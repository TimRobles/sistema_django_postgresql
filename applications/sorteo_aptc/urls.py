from django.urls import path
from . import views

app_name='sorteo_aptc_app'

urlpatterns = [
    path('sorteo-aptc/lista/', views.UsuarioAPTCListView.as_view(), name='respuesta_lista'),
    path('sorteo-aptc/tabla/', views.UsuarioAPTCTabla, name='respuesta_tabla'),
    path('sorteo-aptc/crear/', views.UsuarioAPTCCreateView.as_view(), name='respuesta_usuarioaptc_crear'),
    path('sorteo-aptc/actualizar/<pk>/', views.UsuarioAPTCUpdateView.as_view(), name='respuesta_usuarioaptc_actualizar'),
    path('sorteo-aptc/ruleta/',views.SorteoView.as_view(),name='respuesta_ruleta'),
    path('sorteo-aptc/sortear/', views.Sortear, name='respuesta_sortear'),
]