from django.urls import path
from . import views

app_name='activos_app'

urlActivoBase = [
    path('activo_base/', views.ActivoBaseListView.as_view(), name='activo_base_inicio'),
    path('activo_base-tabla/', views.ActivoBaseTabla, name='activo_base_tabla'),
    path('activo_base/registrar/', views.ActivoBaseCreateView.as_view(), name='activo_base_registrar'),
    path('activo_base/actualizar/<pk>', views.ActivoBaseUpdateView.as_view(), name='activo_base_actualizar'),
    path('activo_base/dar_baja/<pk>', views.ActivoBaseDarBajaView.as_view(), name='activo_base_dar_baja'),
    path('activo_base/dar_alta/<pk>', views.ActivoBaseDarAltaView.as_view(), name='activo_base_dar_alta'),
]

urlpatterns = [
] + urlActivoBase