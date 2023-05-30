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
    
    path('tarea/descripcion/<pk>/', views.TareaDescripcionView.as_view(), name='tarea_descripcion'),
    path('tarea/comentario/<int:tarea_id>/', views.HistorialComentarioTareaCreateView.as_view(), name='tarea_comentario'),
    path('tarea/comentario/actualizar/<pk>/', views.HistorialComentarioTareaUpdateView.as_view(), name='tarea_comentario_actualizar'),
    path('tarea/comentario/eliminar/<pk>/', views.HistorialComentarioTareaDeleteView.as_view(), name='tarea_comentario_eliminar'),

]

