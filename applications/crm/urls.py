from django.urls import path
from . import views

app_name='crm_app'

urlpatterns = [
    path('cliente-crm/', views.ClienteCRMListView.as_view(), name='cliente_crm_inicio'),
    path('cliente-crm-tabla/', views.ClienteCRMTabla, name='cliente_crm_tabla'),
    path('cliente-crm/registrar/', views.ClienteCRMCreateView.as_view(), name='cliente_crm_registrar'),
    path('cliente-crm/actualizar/<pk>/', views.ClienteCRMUpdateView.as_view(), name='cliente_crm_actualizar'),
    path('cliente-crm/detalle/<pk>/', views.ClienteCRMDetailView.as_view(), name='cliente_crm_detalle'),
    path('cliente-crm/detalle-tabla/<pk>/', views.ClienteCRMDetailTabla, name='cliente_crm_detalle_tabla'),
    path('cliente-crm/detalle/registrar/<int:cliente_crm_id>/', views.ClienteCRMDetalleCreateView.as_view(), name='cliente_crm_detalle_registrar'),
]