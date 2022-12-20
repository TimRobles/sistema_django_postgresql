from django.urls import path
from . import views

app_name='sociedad_app'

urlSociedad = [
    path('sociedad/', views.SociedadListView.as_view(), name='sociedad_inicio'),
    path('sociedad-tabla/', views.SociedadTabla, name='sociedad_tabla'),
    path('sociedad/actualizar/<pk>/', views.SociedadUpdateView.as_view(), name='sociedad_actualizar'),
    path('sociedad/baja/<pk>/', views.SociedadDarBajaView.as_view(), name='sociedad_baja'),
    path('sociedad/alta/<pk>/', views.SociedadDarAltaView.as_view(), name='sociedad_alta'),
    path('sociedad/detalle/<pk>/', views.SociedadDetailView.as_view(), name='sociedad_detalle'),
    path('sociedad/detalle-tabla/<pk>/', views.SociedadDetailTabla, name='sociedad_detalle_tabla'),
    path('sociedad/sede/', views.SedeNoneView, name='sociedad_sede_none'),
    path('sociedad/sede/<int:id_sociedad>/', views.SedeView, name='sociedad_sede'),
]

urlpatterns = [
    path('documento/registrar/<int:sociedad_id>/', views.DocumentoCreateView.as_view(), name='documento_registrar'),
    path('documento/eliminar/<pk>/', views.DocumentoDeleteView.as_view(), name='documento_eliminar'),    
    
    path('representante/registrar/<int:sociedad_id>/', views.RepresentanteCreateView.as_view(), name='representante_registrar'),
    path('representante/baja/<pk>/', views.RepresentanteLegalDarBajaView.as_view(), name='representante_baja'),
] + urlSociedad