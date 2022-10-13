from django.urls import path
from . import views

app_name='proveedores_app'

urlProveedor = [
    path('proveedor/', views.ProveedorListView.as_view(), name='proveedor_inicio'),
    path('proveedor-tabla/', views.ProveedorTabla, name='proveedor_tabla'),
    path('proveedor/registrar/', views.ProveedorCreateView.as_view(), name='proveedor_registrar'),
    path('proveedor/actualizar/<pk>/', views.ProveedorUpdateView.as_view(), name='proveedor_actualizar'),
    path('proveedor/baja/<pk>/', views.ProveedorDarBajaView.as_view(), name='proveedor_baja'),
    path('proveedor/alta/<pk>/', views.ProveedorDarAltaView.as_view(), name='proveedor_alta'),
    path('proveedor/detalle/<pk>/', views.ProveedorDetailView.as_view(), name='proveedor_detalle'),
    path('proveedor/detalle-tabla/<pk>/', views.ProveedorDetailTabla, name='proveedor_detalle_tabla'),
]

urlInterlocutor = [
    path('interlocutor/registrar/<int:proveedor_id>/', views.InterlocutorProveedorCreateView.as_view(), name='interlocutor_registrar'),
    path('interlocutor/actualizar/<pk>/', views.InterlocutorProveedorUpdateView.as_view(), name='interlocutor_actualizar'),
    path('interlocutor/baja/<pk>/', views.InterlocutorProveedorDarBajaView.as_view(), name='interlocutor_baja'),
    path('interlocutor/alta/<pk>/', views.InterlocutorProveedorDarAltaView.as_view(), name='interlocutor_alta'),
    path('interlocutor/detalle/<pk>/', views.InterlocutorProveedorDetailView.as_view(), name='interlocutor_detalle'),
    path('interlocutor/detalle-tabla/<pk>/', views.InterlocutorProveedorDetailTabla, name='interlocutor_detalle_tabla'),
]

urlpatterns = [
    path('telefono/registrar/<int:interlocutor_id>/', views.TelefonoInterlocutorCreateView.as_view(), name='telefono_registrar'),
    path('telefono/actualizar/<pk>/', views.TelefonoInterlocutorUpdateView.as_view(), name='telefono_actualizar'),
    path('telefono/baja/<pk>/', views.TelefonoInterlocutorDarBajaView.as_view(), name='telefono_baja'),

    path('correo/registrar/<int:interlocutor_id>/', views.CorreoInterlocutorCreateView.as_view(), name='correo_registrar'),
    path('correo/actualizar/<pk>/', views.CorreoInterlocutorUpdateView.as_view(), name='correo_actualizar'),
    path('correo/baja/<pk>/', views.CorreoInterlocutorDarBajaView.as_view(), name='correo_baja'),
    path('correo/alta/<pk>/', views.CorreoInterlocutorDarAltaView.as_view(), name='correo_alta'),
    
] + urlProveedor + urlInterlocutor