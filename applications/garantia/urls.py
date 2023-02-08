from django.urls import path
from . import views

app_name = 'garantia_app'

urlpatterns = [
    path('ingreso-garantia/',views.IngresoGarantiaListView.as_view(),name='ingreso_garantia_inicio'),
    path('ingreso-garantia-tabla/',views.IngresoGarantiaTabla,name='ingreso_garantia_tabla'),


]
