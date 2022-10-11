from django.urls import path
from . import views

app_name='sorteo_webinar_app'

urlpatterns = [
    path('lista/', views.ParticipanteListView.as_view(), name='sorteo_webinar_lista'),
    path('ruleta/',views.SorteoView.as_view(),name='sorteo_webinar_ruleta'),
    path('sortear/', views.Sortear, name='sorteo_webinar_sortear'),
    path('datos/', views.Datos, name='sorteo_webinar_datos'),
    path('limpiar/', views.Limpiar, name='sorteo_webinar_limpiar'),
    path('eliminar/', views.Eliminar, name='sorteo_webinar_eliminar'),
    path('excel/', views.CargarExcelFormView.as_view(), name='sorteo_webinar_excel'),
]