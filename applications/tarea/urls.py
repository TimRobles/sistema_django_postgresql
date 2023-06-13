from django.urls import path
from . import views

app_name = 'tarea_app'

urlpatterns = [
    path('tipo-tarea/', views.TipoTareaListView.as_view(), name='tipo_tarea_inicio'),
    path('tipo-tarea-tabla/', views.TipoTareaTabla, name='tipo_tarea_tabla'),
    path('tipo-tarea/registrar/', views.TipoTareaCreateView.as_view(), name='tipo_tarea_registrar'),
    path('tipo-tarea/actualizar/<pk>/', views.TipoTareaUpdateView.as_view(), name='tipo_tarea_actualizar'),

    path('tarea/', views.TareaListView.as_view(), name='tarea_inicio'),
    path('tarea-tabla/', views.TareaTabla, name='tarea_tabla'),
    path('tarea/registrar/', views.TareaCreateView.as_view(), name='tarea_registrar'),
    path('tarea/actualizar/<pk>/', views.TareaUpdateView.as_view(), name='tarea_actualizar'),

    path('tarea/detalle/<pk>/', views.TareaDetailView.as_view(), name='tarea_detalle'),
    path('tarea/detalle-tabla/<pk>/', views.TareaDetailTabla, name='tarea_detalle_tabla'),
    
    path('tarea/detalle/descripcion/<pk>/', views.TareaDetalleDescripcionView.as_view(), name='tarea_detalle_descripcion'),
    path('tarea/detalle/comentario/<int:tarea_id>/', views.TareaDetalleHistorialComentarioCreateView.as_view(), name='tarea_detalle_comentario'),
    path('tarea/detalle/comentario/actualizar/<pk>/', views.TareaDetalleHistorialComentarioUpdateView.as_view(), name='tarea_detalle_comentario_actualizar'),
    path('tarea/detalle/comentario/eliminar/<pk>/', views.TareaDetalleHistorialComentarioDeleteView.as_view(), name='tarea_detalle_comentario_eliminar'),
    path('tarea/detalle/asignar/<pk>/', views.TareaAsignarView.as_view(), name='tarea_detalle_asignar'),
    path('tarea/detalle/culminar/<pk>/', views.TareaCulminarUpdateView.as_view(), name='tarea_detalle_culminar'),
]

