from django.urls import path
from . import views

app_name='sorteo_app'

urlpatterns = [
    path('sorteo/', views.SorteoListView.as_view(), name='sorteo_lista'),
    path('sorteo/tabla', views.SorteoTabla, name='sorteo_lista_tabla'),
    path('sorteo/agregar/', views.SorteoCreateView.as_view(), name='sorteo_agregar'),
    path('sorteo/actualizar/<pk>/', views.SorteoUpdateView.as_view(), name='sorteo_actualizar'),
    path('sorteo/ver/<slug>/', views.SorteoDetailView.as_view(), name='sorteo_ver'),
    path('sorteo/ver/tabla/<slug>/', views.SorteoDetailTabla, name='sorteo_ver_tabla'),

    path('ticket/agregar/<int:id_sorteo>/', views.TicketCreateView.as_view(), name='ticket_agregar'),
    
    path('sorteo/iniciar/<slug>/', views.SorteoIniciarView.as_view(), name='sorteo_iniciar'),
    path('sorteo/duplicados/<slug>/', views.EliminarDuplicadosView.as_view(), name='sorteo_duplicados'),
    path('sortear/<slug>/', views.Sortear, name='sortear'),
    path('datos/<slug>/', views.Datos, name='datos'),
    path('excel/<slug>/', views.CargarExcelFormView.as_view(), name='sorteo_webinar_excel'),
    path('reiniciar/<slug>/', views.Reiniciar, name='reiniciar'),
    path('eliminar/<slug>/', views.Eliminar, name='eliminar'),
]