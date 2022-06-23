from django.urls import path
from . import views

app_name='sorteo_app'

urlpatterns = [
    path('lista/', views.TicketListView.as_view(), name='lista'),
    path('sorteo/', views.SorteoView.as_view(), name='sorteo'),
    path('perdedor/', views.Perdedor, name='perdedor'),
    path('ganador/', views.Ganador, name='ganador'),
    path('datos/<str:ticket>', views.Datos, name='datos'),
    path('ganador-formulario/', views.GanadorFormView.as_view(), name='ganador_formulario'),
    path('reiniciar/', views.Reiniciar, name='reiniciar'),
]