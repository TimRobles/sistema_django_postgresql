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

urlInterlocutor = [
    path('interlocutor/registrar/<int:cliente_id>/', views.InterlocutorClienteCreateView.as_view(), name='interlocutor_registrar'),
    path('interlocutor/actualizar/<pk>/', views.InterlocutorClienteUpdateView.as_view(), name='interlocutor_actualizar'),
    path('interlocutor/baja/<pk>/', views.InterlocutorClienteDarBajaView.as_view(), name='interlocutor_baja'),
    path('interlocutor/alta/<pk>/', views.InterlocutorClienteDarAltaView.as_view(), name='interlocutor_alta'),
    path('interlocutor/detalle/<pk>/', views.InterlocutorClienteDetailView.as_view(), name='interlocutor_detalle'),
    path('interlocutor/detalle-tabla/<pk>/', views.InterlocutorClienteDetailTabla, name='interlocutor_detalle_tabla'),
    path('interlocutor/eliminar/<pk>/', views.InterlocutorClienteDeleteView.as_view(), name='interlocutor_eliminar'),

    path('interlocutor/lista/', views.InterlocutorClienteListaView.as_view(), name='interlocutor_lista'),
    path('cliente-interlocutor/actualizar/<pk>/', views.ClienteInterlocutorUpdateView.as_view(), name='cliente_interlocutor_actualizar'),
    path('cliente-interlocutor/agregar/<int:interlocutor_cliente_id>/', views.ClienteInterlocutorCreateView.as_view(), name='cliente_interlocutor_agregar'),
    path('cliente-interlocutor/eliminar/<int:interlocutor_cliente_id>/<pk>/', views.ClienteInterlocutorDeleteView.as_view(), name='cliente_interlocutor_eliminar'),
]

urlCorreo = [
    path('correo/registrar/<int:cliente_id>/', views.CorreoClienteCreateView.as_view(), name='correo_registrar'),
    path('correo/actualizar/<pk>/', views.CorreoClienteUpdateView.as_view(), name='correo_actualizar'),
    path('correo/baja/<pk>/', views.CorreoClienteDarBajaView.as_view(), name='correo_baja'),
]

urlRepresentante_Legal = [
    path('representante-legal/asignar/<int:cliente_id>/', views.RepresentanteLegalClienteCreateView.as_view(), name='representante_legal_asignar'),
    path('representante-legal/baja/<pk>/', views.RepresentanteLegalClienteDarBajaView.as_view(), name='representante_legal_baja'),
]

urlpatterns = [
    path('telefono-interlocutor/registrar/<int:interlocutor_id>/', views.TelefonoInterlocutorCreateView.as_view(), name='telefono_interlocutor_registrar'),
    path('telefono-interlocutor/actualizar/<pk>/', views.TelefonoInterlocutorUpdateView.as_view(), name='telefono_interlocutor_actualizar'),
    path('telefono-interlocutor/baja/<pk>/', views.TelefonoInterlocutorDarBajaView.as_view(), name='telefono_interlocutor_baja'),

    path('correo-interlocutor/registrar/<int:interlocutor_id>/', views.CorreoInterlocutorCreateView.as_view(), name='correo_interlocutor_registrar'),
    path('correo-interlocutor/actualizar/<pk>/', views.CorreoInterlocutorUpdateView.as_view(), name='correo_interlocutor_actualizar'),
    path('correo-interlocutor/baja/<pk>/', views.CorreoInterlocutorDarBajaView.as_view(), name='correo_interlocutor_baja'),
    
    path('anexo/registrar/<int:cliente_id>/', views.ClienteAnexoCreateView.as_view(), name='anexo_registrar'),
    path('anexo/baja/<pk>/', views.ClienteAnexoDarBajaView.as_view(), name='anexo_baja'),
    
] + urlCliente + urlInterlocutor + urlCorreo + urlRepresentante_Legal