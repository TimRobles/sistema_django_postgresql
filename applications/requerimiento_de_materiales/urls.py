from django.urls import path
from . import views

app_name = 'requerimiento_material_app'

urlpatterns = [
    path('requerimiento-material/', views.RequerimientoMaterialListView.as_view(), name='requerimiento_material_inicio'),
    path('requerimiento-material-tabla/', views.RequerimientoMaterialTabla, name='requerimiento_material_tabla'),

    path('requerimiento-material/registrar/', views.RequerimientoMaterialCreateView.as_view(), name='requerimiento_material_registrar'),
    path('requerimiento-material-detalle-tabla/<int:requerimiento_id>/', views.RequerimientoMaterialDetalleTabla, name='requerimiento_material_detalle_tabla'),
    
    path('requerimiento-material/actualizar/<pk>/', views.RequerimientoMaterialUpdateView.as_view(), name='requerimiento_material_actualizar'),
   
    path('requerimiento-material/agregar-material/<int:requerimiento_id>/', views.RequerimientoMaterialDetalleCreateView.as_view(), name='requerimiento_material_agregar_material'),
    path('requerimiento-material/actualizar-material/<pk>/', views.RequerimientoMaterialDetalleUpdateView.as_view(), name='requerimiento_material_actualizar_material'),
    path('requerimiento-material/eliminar/<pk>/', views.RequerimientoMaterialDetalleDeleteView.as_view(), name='requerimiento_material_eliminar_material'),



    path('proveedor-interlocutor/<str:id_interlocutor_proveedor>/', views.ProveedorView, name='proveedor_interlocutor'),
]