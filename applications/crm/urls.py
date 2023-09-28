from django.urls import path
from . import views

app_name='crm_app'

urlCliente = [
    path('cliente-crm/', views.ClienteCRMListView.as_view(), name='cliente_crm_inicio'),
    path('cliente-crm-tabla/', views.ClienteCRMTabla, name='cliente_crm_tabla'),
    path('cliente-crm/nacional/registrar/', views.ClienteCRMNacionalCreateView.as_view(), name='cliente_crm_nacional_registrar'),
    path('cliente-crm/extranjero/registrar/', views.ClienteCRMExtranjeroCreateView.as_view(), name='cliente_crm_extranjero_registrar'),
    path('cliente-crm/nacional/actualizar/<pk>/', views.ClienteCRMNacionalUpdateView.as_view(), name='cliente_crm_nacional_actualizar'),
    path('cliente-crm/extranjero/actualizar/<pk>/', views.ClienteCRMExtranjeroUpdateView.as_view(), name='cliente_crm_extranjero_actualizar'),

    path('cliente-crm/detalle/reuniones/<pk>/', views.ReunionesView.as_view(), name='detalle_reuniones'),
    path('cliente-crm/detalle-tabla/reuniones/<pk>/', views.ReunionesTabla, name='detalle_tabla_reuniones'),
    path('cliente-crm/detalle/reuniones/registrar/<int:cliente_crm_id>/', views.ReunionesCreateView.as_view(), name='detalle_registrar_reuniones'),
    path('cliente-crm/detalle/reuniones/actualizar/<pk>/', views.ReunionesUpdateView.as_view(), name='detalle_actualizar_reuniones'),
    path('cliente-crm/detalle/reuniones/eliminar/<pk>/', views.ReunionesDeleteView.as_view(), name='detalle_eliminar_reuniones'),

    path('cliente-crm/detalle/visitas/<pk>/', views.VisitasView.as_view(), name='detalle_visitas'),
    path('cliente-crm/detalle-tabla/visitas/<pk>/', views.VisitasTabla, name='detalle_tabla_visitas'),
    path('cliente-crm/detalle/visitas/registrar/<int:cliente_crm_id>/', views.VisitasCreateView.as_view(), name='detalle_registrar_visitas'),
    path('cliente-crm/detalle/visitas/actualizar/<pk>/', views.VisitasUpdateView.as_view(), name='detalle_actualizar_visitas'),
    path('cliente-crm/detalle/visitas/eliminar/<pk>/', views.VisitasDeleteView.as_view(), name='detalle_eliminar_visitas'),

    path('cliente-crm/detalle/llamadas/<pk>/', views.LlamadasView.as_view(), name='detalle_llamadas'),
    path('cliente-crm/detalle-tabla/llamadas/<pk>/', views.LlamadasTabla, name='detalle_tabla_llamadas'),
    path('cliente-crm/detalle/llamadas/registrar/<int:cliente_crm_id>/', views.LlamadasCreateView.as_view(), name='detalle_registrar_llamadas'),
    path('cliente-crm/detalle/llamadas/actualizar/<pk>/', views.LlamadasUpdateView.as_view(), name='detalle_actualizar_llamadas'),
    path('cliente-crm/detalle/llamadas/eliminar/<pk>/', views.LlamadasDeleteView.as_view(), name='detalle_eliminar_llamadas'),

    path('cliente-crm/detalle/correos/<pk>/', views.CorreosView.as_view(), name='detalle_correos'),
    path('cliente-crm/detalle-tabla/correos/<pk>/', views.CorreosTabla, name='detalle_tabla_correos'),
    path('cliente-crm/detalle/correos/registrar/<int:cliente_crm_id>/', views.CorreosCreateView.as_view(), name='detalle_registrar_correos'),
    path('cliente-crm/detalle/correos/actualizar/<pk>/', views.CorreosUpdateView.as_view(), name='detalle_actualizar_correos'),
    path('cliente-crm/detalle/correos/eliminar/<pk>/', views.CorreosDeleteView.as_view(), name='detalle_eliminar_correos'),

    path('cliente-crm/detalle/eventos/<pk>/', views.EventosView.as_view(), name='detalle_eventos'),
    path('cliente-crm/detalle-tabla/eventos/<pk>/', views.EventosTabla, name='detalle_tabla_eventos'),
    path('cliente-crm/detalle/eventos/registrar/<int:cliente_crm_id>/', views.EventosCreateView.as_view(), name='detalle_registrar_eventos'),
    path('cliente-crm/detalle/eventos/actualizar/<pk>/', views.EventosUpdateView.as_view(), name='detalle_actualizar_eventos'),
    path('cliente-crm/detalle/eventos/eliminar/<pk>/', views.EventosDeleteView.as_view(), name='detalle_eliminar_eventos'),

    path('cliente-crm/detalle/soporte-tecnico/<pk>/', views.SoporteTecnicoView.as_view(), name='detalle_soporte_tecnico'),
    path('cliente-crm/detalle-tabla/soporte-tecnico/<pk>/', views.SoporteTecnicoTabla, name='detalle_tabla_soporte_tecnico'),
    path('cliente-crm/detalle/soporte-tecnico/registrar/<int:cliente_crm_id>/', views.SoporteTecnicoCreateView.as_view(), name='detalle_registrar_soporte_tecnico'),
    path('cliente-crm/detalle/soporte-tecnico/actualizar/<pk>/', views.SoporteTecnicoUpdateView.as_view(), name='detalle_actualizar_soporte_tecnico'),
    path('cliente-crm/detalle/soporte-tecnico/eliminar/<pk>/', views.SoporteTecnicoDeleteView.as_view(), name='detalle_eliminar_soporte_tecnico'),

    path('cliente-crm/detalle/caracteristicas_tecnicas/<pk>/', views.CaracteristicasTecnicasView.as_view(), name='detalle_caracteristicas_tecnicas'),
    path('cliente-crm/detalle-tabla/caracteristicas_tecnicas/<pk>/', views.CaracteristicasTecnicasTabla, name='detalle_tabla_caracteristicas_tecnicas'),
    path('cliente-crm/detalle/caracteristicas_tecnicas/registrar/<int:cliente_crm_id>/', views.CaracteristicasTecnicasCreateView.as_view(), name='detalle_registrar_caracteristicas_tecnicas'),
    path('cliente-crm/detalle/caracteristicas_tecnicas/actualizar/<pk>/', views.CaracteristicasTecnicasUpdateView.as_view(), name='detalle_actualizar_caracteristicas_tecnicas'),
    path('cliente-crm/detalle/caracteristicas_tecnicas/eliminar/<pk>/', views.CaracteristicasTecnicasDeleteView.as_view(), name='detalle_eliminar_caracteristicas_tecnicas'),

    path('cliente-crm/detalle/nuevos-productos-solicitados/<pk>/', views.NuevosProductosSolicitadosView.as_view(), name='detalle_nuevos_productos_solicitados'),
    path('cliente-crm/detalle-tabla/nuevos-productos-solicitados/<pk>/', views.NuevosProductosSolicitadosTabla, name='detalle_tabla_nuevos_productos_solicitados'),
    path('cliente-crm/detalle/nuevos-productos-solicitados/registrar/<int:cliente_crm_id>/', views.NuevosProductosSolicitadosCreateView.as_view(), name='detalle_registrar_nuevos_productos_solicitados'),
    path('cliente-crm/detalle/nuevos-productos-solicitados/actualizar/<pk>/', views.NuevosProductosSolicitadosUpdateView.as_view(), name='detalle_actualizar_nuevos_productos_solicitados'),
    path('cliente-crm/detalle/nuevos-productos-solicitados/eliminar/<pk>/', views.NuevosProductosSolicitadosDeleteView.as_view(), name='detalle_eliminar_nuevos_productos_solicitados'),

    path('cliente-crm/detalle/cotizaciones/<pk>/', views.ClienteCRMCotizacionesView.as_view(), name='cliente_crm_detalle_cotizaciones'),
    path('cliente-crm/detalle/facturas/<pk>/', views.ClienteCRMFacturasView.as_view(), name='cliente_crm_detalle_facturas'),
    # path('cliente-crm/detalle/ver/<pk>/', views.ClienteCRMDetalleVerView.as_view(), name='cliente_crm_detalle_ver'),
    ]

urlEvento = [
    path('evento-crm/', views.EventoCRMListView.as_view(), name='evento_crm_inicio'),
    path('evento-crm-tabla/', views.EventoCRMTabla, name='evento_crm_tabla'),
    path('evento-crm/registrar/', views.EventoCRMCreateView.as_view(), name='evento_crm_registrar'),
    path('evento-crm/actualizar/<pk>/', views.EventoCRMUpdateView.as_view(), name='evento_crm_actualizar'),
    path('evento-crm/eliminar/<pk>', views.EventoCRMEliminarDeleteView.as_view(), name='evento_crm_eliminar'),
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
    # path('<slug>/', views.RespuestaVerView.as_view(), name='encuesta_ver'),
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
