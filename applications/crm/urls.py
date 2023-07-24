from django.urls import path
from . import views

app_name='crm_app'

urlCliente = [
    path('cliente-crm/', views.ClienteCRMListView.as_view(), name='cliente_crm_inicio'),
    path('cliente-crm-tabla/', views.ClienteCRMTabla, name='cliente_crm_tabla'),
    path('cliente-crm/registrar/', views.ClienteCRMCreateView.as_view(), name='cliente_crm_registrar'),
    path('cliente-crm/actualizar/<pk>/', views.ClienteCRMUpdateView.as_view(), name='cliente_crm_actualizar'),
    path('cliente-crm/detalle/<pk>/', views.ClienteCRMDetailView.as_view(), name='cliente_crm_detalle'),
    path('cliente-crm/detalle-tabla/<pk>/', views.ClienteCRMDetailTabla, name='cliente_crm_detalle_tabla'),
    path('cliente-crm/detalle/registrar/<int:cliente_crm_id>/', views.ClienteCRMDetalleCreateView.as_view(), name='cliente_crm_detalle_registrar'),
    path('cliente-crm/detalle/actualizar/<pk>/', views.ClienteCRMDetalleUpdateView.as_view(), name='cliente_crm_detalle_actualizar'),
    path('cliente-crm/detalle/eliminar/<pk>/', views.ClienteCRMDetalleDeleteView.as_view(), name='cliente_crm_detalle_eliminar'),
    path('cliente-crm/detalle/ver/<pk>/', views.ClienteCRMDetalleVerView.as_view(), name='cliente_crm_detalle_ver'),
    ]

urlEvento = [
    path('evento-crm/', views.EventoCRMListView.as_view(), name='evento_crm_inicio'),
    path('evento-crm-tabla/', views.EventoCRMTabla, name='evento_crm_tabla'),
    path('evento-crm/registrar/', views.EventoCRMCreateView.as_view(), name='evento_crm_registrar'),
    path('evento-crm/actualizar/<pk>/', views.EventoCRMUpdateView.as_view(), name='evento_crm_actualizar'),
    path('evento-crm/detalle/<pk>/', views.EventoCRMDetailView.as_view(), name='evento_crm_detalle'),
    path('evento-crm/detalle-tabla/<pk>/', views.EventoCRMDetailTabla, name='evento_crm_detalle_tabla'),
    path('evento-crm/detalle/descripcion/<pk>/', views.EventoCRMDetalleDescripcionView.as_view(), name='evento_crm_detalle_descripcion'),
    path('evento-crm/update/<pk>/', views.EventoCRMActualizarView.as_view(), name='evento_crm_update'),
    path('evento-crm/detalle/registrar/<int:evento_crm_id>/', views.EventoCRMDetalleInformacionAdicionalCreateView.as_view(), name='evento_crm_detalle_informacion_adicional_registrar'),
    path('evento-crm/detalle/actualizar/<pk>/', views.EventoCRMDetalleInformacionAdicionalUpdateView.as_view(), name='evento_crm_detalle_informacion_adicional_actualizar'),
    path('evento-crm/detalle/eliminar/<pk>/', views.EventoCRMDetalleInformacionAdicionalDeleteView.as_view(), name='evento_crm_detalle_informacion_adicional_eliminar'),
    path('evento-crm/detalle/agregar-merchandising/<int:evento_crm_id>/', views.EventoCRMDetalleMerchandisingCreateView.as_view(), name='evento_crm_detalle_agregar_merchandising'),
    path('evento-crm/detalle/actualizar-merchandising/<pk>/', views.EventoCRMDetalleMerchandisingUpdateView.as_view(), name='evento_crm_detalle_actualizar_merchandising'),
    path('evento-crm/detalle/eliminar-merchandising/<pk>/', views.EventoCRMDetalleMerchandisingDeleteView.as_view(), name='evento_crm_detalle_eliminar_merchandising'),
    path('evento-crm/guardar/<pk>/', views.EventoCRMGuardarView.as_view(), name='evento_crm_guardar'),
    path('evento-crm/generar-guia/<pk>/', views.EventoCRMGenerarGuiaView.as_view(), name='evento_crm_generar_guia'),
    path('evento-crm/finalizar/<pk>/', views.EventoCRMFinalizarView.as_view(), name='evento_crm_finalizar'),
    ]

urlEncuesta = [
    path('encuesta-crm/', views.EncuestaCRMListView.as_view(), name='encuesta_crm_inicio'),
    path('encuesta-crm-tabla/', views.EncuestaCRMTabla, name='encuesta_crm_tabla'),    
    path('encuesta-crm/registrar/', views.EncuestaCRMCreateView.as_view(), name='encuesta_crm_registrar'),
    path('encuesta-crm/actualizar/<slug>/', views.EncuestaCRMUpdateView.as_view(), name='encuesta_crm_actualizar'),
    path('encuesta-crm/eliminar/<slug>/', views.EncuestaCRMDeleteView.as_view(), name='encuesta_crm_eliminar'),
    path('encuesta-crm/detalle/<slug>/', views.EncuestaCRMDetailView.as_view(), name='encuesta_crm_detalle'),
    path('encuesta-crm/detalle-tabla/<slug>/', views.EncuestaCRMDetailTabla, name='encuesta_crm_detalle_tabla'),
    path('encuesta-crm/agregar-pregunta/<slug>/', views.EncuestaPreguntaCRMUpdateView.as_view(), name='encuesta_crm_pregunta'), #Añadir pregunta
    path('encuesta-crm/ver/<slug>/', views.RespuestaVerView.as_view(), name='encuesta_ver'),
    path('encuesta-respuesta/', views.EncuestaRespuesta.as_view(), name='encuesta_respuesta'),
    ]

urlEncuestaPregunta = [
    path('encuesta-crm/pregunta/', views.PreguntaCRMListView.as_view(), name='pregunta_crm_inicio'),
    path('encuesta-crm/pregunta-tabla/', views.PreguntaCRMTabla, name='pregunta_crm_tabla'),
    path('encuesta-crm/pregunta/registrar/', views.PreguntaCRMCreateView.as_view(), name='pregunta_crm_registrar'),
    path('encuesta-crm/pregunta/actualizar/<pk>/', views.PreguntaCRMUpdateView.as_view(), name='pregunta_crm_actualizar'),
    path('encuesta-crm/pregunta/eliminar/<pk>/', views.PreguntaCRMDeleteView.as_view(), name='pregunta_crm_eliminar'),
    path('encuesta-crm/pregunta/detalle/<pk>/', views.PreguntaCRMDetailView.as_view(), name='pregunta_crm_detalle'),
    path('encuesta-crm/pregunta/detalle-tabla/<pk>/', views.PreguntaCRMDetailTabla, name='pregunta_crm_detalle_tabla'),
    ]

urlEncuestaAlternativa = [
    path('encuesta-crm/alternativa/registrar/<int:pregunta_id>/', views.AlternativaCRMCreateView.as_view(), name='alternativa_registrar'),
    path('encuesta-crm/alternativa/actualizar/<pk>/', views.AlternativaCRMUpdateView.as_view(), name='alternativa_actualizar'),
    path('encuesta-crm/alternativa/eliminar/<pk>/', views.AlternativaCRMDeleteView.as_view(), name='alternativa_eliminar'),
    ]

urlEncuestaRespuesta = [
    path('encuesta-crm/respuesta/', views.RespuestaCRMListView.as_view(), name='respuesta_crm_inicio'),
    path('encuesta-crm/respuesta-tabla/', views.RespuestaCRMTabla, name='respuesta_crm_tabla'),
    path('encuesta-crm/respuesta/registrar/', views.RespuestaCRMCreateView.as_view(), name='respuesta_crm_registrar'),
    path('encuesta-crm/respuesta/actualizar/<slug>/', views.RespuestaCRMUpdateView.as_view(), name='respuesta_crm_actualizar'),
    path('encuesta-crm/respuesta/eliminar/<slug>/', views.RespuestaCRMDeleteView.as_view(), name='respuesta_crm_eliminar'),
    path('encuesta-crm/respuesta/detalle/<slug>/', views.RespuestaCRMDetailView.as_view(), name='respuesta_crm_detalle'),
    path('encuesta-crm/respuesta/detalle-tabla/<slug>/', views.RespuestaCRMDetailTabla, name='respuesta_crm_detalle_tabla'),
    ]

urlpatterns = urlCliente + urlEvento + urlEncuesta + urlEncuestaPregunta + urlEncuestaAlternativa + urlEncuestaRespuesta
