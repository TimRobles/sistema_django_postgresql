from django.urls import path
from . import views

app_name='sorteo_aptc_app'

urlpatterns = [
    path('sorteoaptc/lista/', views.UsuarioAPTCListView.as_view(), name='respuesta_lista'),
    path('sorteoaptc/usuarioaptc/crear/', views.UsarioAPTCCreateView.as_view(), name='respuesta_usuarioaptc_crear'),
    path('sorteoaptc/usuarioaptc/actualizar/<pk>/', views.UsuarioAPTCUpdateView.as_view(), name='respuesta_usuarioaptc_actualizar'),
    path('sorteoaptc/ruleta/',views.SorteoView.as_view(),name='respuesta_ruleta'),
    path('sorteoaptc/sortear/', views.Sortear, name='respuesta_sortear'),
]