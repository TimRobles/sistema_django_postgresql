from django.urls import path
from . import views

app_name='clientes_app'

urlCliente = [
    path('cliente/', views.ClienteListView.as_view(), name='cliente_inicio'),
    path('cliente-tabla/', views.ClienteTabla, name='cliente_tabla'),
    path('cliente/registrar/', views.ClienteCreateView.as_view(), name='cliente_registrar'),
    path('cliente/actualizar/<pk>/', views.ClienteUpdateView.as_view(), name='cliente_actualizar'),
    path('cliente/baja/<pk>/', views.ClienteDarBajaView.as_view(), name='cliente_baja'),
    path('cliente/alta/<pk>/', views.ClienteDarAltaView.as_view(), name='cliente_alta'),
    path('cliente/detalle/<pk>/', views.ClienteDetailView.as_view(), name='cliente_detalle'),
    path('cliente/detalle-tabla/<pk>/', views.ClienteDetailTabla, name='cliente_detalle_tabla'),
]

urlpatterns = [
    path('interlocutor/registrar/<int:cliente_id>/', views.InterlocutorClienteCreateView.as_view(), name='interlocutor_registrar'),
    path('interlocutor/actualizar/<pk>/', views.InterlocutorClienteUpdateView.as_view(), name='interlocutor_actualizar'),
    path('interlocutor/baja/<pk>/', views.InterlocutorClienteDarBajaView.as_view(), name='interlocutor_baja'),
    path('interlocutor/alta/<pk>/', views.InterlocutorClienteDarAltaView.as_view(), name='interlocutor_alta'),
    # path('interlocutor/detalle/<pk>/', views.InterlocutorClienteDetailView.as_view(), name='interlocutor_detalle'),
    # path('interlocutor/detalle-tabla/<pk>/', views.InterlocutorClienteDetailTabla, name='interlocutor_detalle_tabla'),
] + urlCliente