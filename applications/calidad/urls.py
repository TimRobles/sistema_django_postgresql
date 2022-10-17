from django.urls import path
from .import views

app_name = 'calidad_app'

urlpatterns = [
    path('falla-material/',views.FallaMaterialListView.as_view(),name='falla_material'),
    path('falla-material-tabla/',views.FallaMaterialTabla,name='falla_material_tabla'),  
   
    path('falla-material/detalle/<int:id_sub_familia>/',views.FallaMaterialDetalleView.as_view(),name='falla_material_detalle'),
    
    path('falla-material/registrar/<int:id_sub_familia>/', views.FallaMaterialCreateView.as_view(), name='falla_material_registrar'),
    path('falla-material/actualizar/<pk>/', views.FallaMaterialUpdateView.as_view(), name='falla_material_actualizar'),
    path('falla-material/eliminar/<pk>/', views.FallaMaterialDeleteView.as_view(), name='falla_material_eliminar'),

]