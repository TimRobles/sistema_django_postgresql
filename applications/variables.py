SUNAT_TRANSACTION = (
    (1, 'VENTA INTERNA'),
    (2, 'EXPORTACIÓN'),
    (4, 'VENTA INTERNA - ANTICIPOS'),
    (29, 'VENTAS NO DOMICILIADOS QUE NO CALIFICAN COMO EXPORTACIÓN.'),
    (30, 'OPERACIÓN SUJETA A DETRACCIÓN.'),
    (33, 'DETRACCIÓN - SERVICIOS DE TRANSPORTE CARGA'),
    (34, 'OPERACIÓN SUJETA A PERCEPCIÓN'),
    (32, 'DETRACCIÓN - SERVICIOS DE TRANSPORTE DE PASAJEROS.'),
    (31, 'DETRACCIÓN - RECURSOS HIDROBIOLÓGICOS'),
    (35, 'VENTA NACIONAL A TURISTAS - TAX FREE'),
)
TIPO_DOCUMENTO_SUNAT_NACIONAL = (
    ('6', 'RUC - REGISTRO ÚNICO DE CONTRIBUYENTE'),
    ('1', 'DNI - DOC. NACIONAL DE IDENTIDAD'),
    ('-', 'VARIOS - VENTAS MENORES A S/.700.00 Y OTROS'),
    ('4', 'CARNET DE EXTRANJERÍA'),
    ('7', 'PASAPORTE'),
    )

TIPO_DOCUMENTO_SUNAT_EXTRANJERO = (
    ('A', 'CÉDULA DIPLOMÁTICA DE IDENTIDAD'),
    ('B', 'DOC.IDENT.PAIS.RESIDENCIA-NO.D'),
    ('0', 'NO DOMICILIADO, SIN RUC (EXPORTACIÓN)'),
    ('G', 'Salvoconducto'),
    )

TIPO_DOCUMENTO_SUNAT = TIPO_DOCUMENTO_SUNAT_NACIONAL + TIPO_DOCUMENTO_SUNAT_EXTRANJERO

DICCIONARIO_TIPO_DOCUMENTO_SUNAT = {
    '6' : 'RUC',
    '1' : 'DNI',
    '-' : 'VENTAS MENORES',
    '4' : 'C. EXTRANJERÍA',
    '7' : 'PASAPORTE',
    'A' : 'CÉDULA DIPLOMÁTICA DE IDENTIDAD',
    'B' : 'DOC.IDENT.PAIS.RESIDENCIA-NO.D',
    '0' : 'SIN RUC (EXPORTACIÓN)',
    'G' : 'Salvoconducto',
    }

TIPO_REPRESENTANTE_LEGAL_SUNAT = (
    ('001', 'Administrador'),
    ('002', 'Administrador Judicial'),
    ('003', 'Albacea'),
    ('004', 'Alcalde'),
    ('005', 'Apoderado'),
    ('007', 'Contador'),
    ('008', 'Coordinador'),
    ('009', 'Curador'),
    ('010', 'Decano'),
    ('011', 'Director'),
    ('012', 'Director (centro de estudios)'),
    ('013', 'Director Ejecutivo'),
    ('014', 'Director General'),
    ('015', 'Director Municipal'),
    ('016', 'Embajador'),
    ('017', 'Factor'),
    ('019', 'Gerente'),
    ('020', 'Gerente Ejecutivo'),
    ('021', 'Gerente General'),
    ('022', 'Gestor de Empresas'),
    ('023', 'Heredero'),
    ('024', 'Intendente'),
    ('025', 'Jefe'),
    ('026', 'Liquidador'),
    ('027', 'Mandatario'),
    ('028', 'Ministro'),
    ('029', 'Presidente'),
    ('030', 'Presidente Consejo de Vigilancia'),
    ('031', 'Presidente Consejo Administración'),
    ('032', 'Presidente Directorio'),
    ('033', 'Presidente Ejecutivo'),
    ('034', 'Procurador'),
    ('035', 'Promotor'),
    ('036', 'Regidor'),
    ('037', 'Representante no domiciliado'),
    ('038', 'Representante religioso'),
    ('039', 'Representante de universidades'),
    ('040', 'Secretario'),
    ('041', 'Síndico'),
    ('042', 'Sub director'),
    ('043', 'Sub gerente'),
    ('044', 'Superintendente'),
    ('045', 'Teniente alcalde'),
    ('046', 'Tesorero'),
    ('047', 'Tutor'),
    ('048', 'Vicepresidente'),
    ('049', 'Vice decano'),
    ('050', 'Vocal'),
    ('051', 'Titular gerente'),
    ('052', 'Socio Administrador'),
    ('998', 'Otros persona jurídica'),
    ('999', 'Otros persona natural'),
    )

CONDICION_SUNAT = (
    (1, 'Habido'),
    (2, 'No hallado'),
    (3, 'No habido'),
    )

ESTADO_SUNAT = (
    (1, 'Activo'),
    (2, 'Suspension temporal'),
    (3, 'Baja provisional'),
    (4, 'Baja definitiva'),
    (5, 'Baja provisional de oficio'),
    (6, 'Baja definitiva de oficio'),
    (7, 'Baja interna'),
    )

TIPO_IGV_CHOICES = (
    (1, 'Gravado - Operación Onerosa'),
    (2, 'Gravado - Retiro por premio'),
    (3, 'Gravado - Retiro por donación'),
    (4, 'Gravado - Retiro'),
    (5, 'Gravado - Retiro por publicidad'),
    (6, 'Gravado - Bonificaciones'),
    (7, 'Gravado - Retiro por entrega a trabajadores'),
    (8, 'Exonerado - Operación Onerosa'),
    (9, 'Inafecto - Operación Onerosa'),
    (10, 'Inafecto - Retiro por Bonificación'),
    (11, 'Inafecto - Retiro'),
    (12, 'Inafecto - Retiro por Muestras Médicas'),
    (13, 'Inafecto - Retiro por Convenio Colectivo'),
    (14, 'Inafecto - Retiro por premio'),
    (15, 'Inafecto - Retiro por publicidad'),
    (16, 'Exportación'),
    (17, 'Exonerado - Transferencia Gratuita'),
    )

TIPO_ISC_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
)

TIPO_DOCUMENTO_CHOICES = (
    ('1', 'DNI - DOC. NACIONAL DE IDENTIDAD'),
    ('4', 'CARNET DE EXTRANJERÍA'),
    ('7', 'PASAPORTE'),
    ('A', 'CÉDULA DIPLOMÁTICA DE IDENTIDAD'),
    ('B', 'DOC.IDENT.PAIS.RESIDENCIA-NO.D'),
    ('-', 'SIN DOCUMENTO'),
    )

TIPO_COMPROBANTE = (
    (1, 'FACTURA'),
    (2, 'BOLETA'),
    (3, 'NOTA DE CRÉDITO'),
    (4, 'NOTA DE DÉBITO'),
    (7, 'GUÍA REMISIÓN REMITENTE'),
    )

MOTIVO_TRASLADO = (
    ("01", "VENTA"),
    ("14", "VENTA SUJETA A CONFIRMACION DEL COMPRADOR"),
    ("02", "COMPRA"),
    ("04", "TRASLADO ENTRE ESTABLECIMIENTOS DE LA MISMA EMPRESA"),
    ("18", "TRASLADO EMISOR ITINERANTE CP"),
    ("08", "IMPORTACION"),
    ("09", "EXPORTACION"),
    ("19", "TRASLADO A ZONA PRIMARIA"),
    ("13", "OTROS"),
    )

TIPO_VENTA= (
    (1, 'CONTADO'),
    (2, 'CREDITO'),
    )

ESTADOS = (
    (1, 'ALTA'),
    (2, 'BAJA'),
    )

ESTADOS_RECIBO = (
    (1, 'PENDIENTE'),
    (2, 'CANCELADO'),
    (3, 'ANULADO'),
    )

ESTADOS_TELECREDITO = (
    (1, 'ABIERTO'),
    (2, 'SOLICITADO'),
    (3, 'REGISTRADO'),
    (4, 'CERRADO'),
    )

ESTADOS_DOCUMENTO = (
    (1, 'BORRADOR'),
    (2, 'ACTIVO'),
    (3, 'ANULADO'),
    (4, 'ACEPTADO POR SUNAT'),
    (5, 'RECHAZADO POR SUNAT'),
    (6, 'CON ERRORES'),
    (7, 'FINTA'),
    )

ESTADO_NOTA_INGRESO = (
    (1, 'BORRADOR'),
    (2, 'FINALIZADO'),
    (3, 'ANULADO'),
    )

ESTADO_NOTA_DEVOLUCION = (
    (1, 'BORRADOR'),
    (2, 'FINALIZADO'),
    (3, 'ANULADO'),
    )

ESTADO_COMPROBANTE = (
    (1, 'PENDIENTE'),
    (2, 'ANULADO'),
    (3, 'FINALIZADO'),
    )

ESTADO_DOCUMENTO = (
    (1, 'PENDIENTE'),
    (2, 'CONFIRMADO'),
    (3, 'FINALIZADO'),
    )

ESTADO_COMPROBANTE_PI = (
    (0, 'BORRADOR'),
    (1, 'PENDIENTE'),
    (2, 'RECIBIDO'),
    (3, 'ANULADO'),
    )

ESTADO_COMPROBANTE_CI = (
    (1, 'BORRADOR'),
    (2, 'FINALIZADO'),
    )

ESTADO_SOLICITUD = (
    (1, 'BORRADOR'),
    (2, 'ESPERA DE APROBACIÓN'),
    (3, 'APROBADO'),
    (4, 'RECHAZADO'),
)

INTERNACIONAL_NACIONAL = (
    (1,'INTERNACIONAL'),
    (2,'NACIONAL'),
    )

INCOTERMS = (
        (1, 'EXW'),
        (2, 'FOB'),
        (3, 'FCA'),
        (4, 'CIF'),
        (5, 'DDP'),
)

ESTADOS_ORDEN_COMPRA = (
    (0, 'NUEVA VERSIÓN'),
    (1, 'POR VERIFICAR'),
    (2, 'ENVIADO'),
    (3, 'CONFIRMADO'),
    (4, 'ANULADO'),
    (5, 'INICIAL'),
    )

ESTADOS_COTIZACION_VENTA = (
    (1, 'BORRADOR'),
    (2, 'PENDIENTE'),
    (3, 'RESERVADO'),
    (4, 'CONFIRMADO'), #Regresa a Reservado
    (5, 'CONFIRMADO'), #Regresa a Pendiente
    (6, 'CONFIRMADO ANTICIPADO'),
    (7, 'FINALIZADO'),
    (8, 'VENCIDO'),
    (9, 'ANULADO'),
    (10, 'BORRADOR PRÉSTAMO'),
    (11, 'PRÉSTAMO'),
    (12, 'CONFIRMADO'), #Regresa a Préstamo
    )

ESTADOS_CONFIRMACION = (
    (1, 'PENDIENTE'),
    (2, 'CON COMPROBANTE DE VENTA'),
    (3, 'ANULADO'),
    (4, 'DESPACHO COMPLETO'),
    (5, 'DESPACHO COMPLETO SIN COMPROBANTE'),
    )

TIPO_PERCEPCION = (
    (1, 'PERCEPCIÓN VENTA INTERNA - TASA 2%'),
    (2, 'PERCEPCIÓN ADQUISICIÓN DE COMBUSTIBLE-TASA 1%'),
    (3, 'PERCEPCIÓN REALIZADA AL AGENTE DE PERCEPCIÓN CON TASA ESPECIAL - TASA 0.5%')
)

TIPO_RETENCION = (
    (1, 'TASA 3%'),
    (2, 'TASA 6%'),
)

TIPO_NOTA_CREDITO_SIN_NADA = (
    (3, 'CORRECCIÓN POR ERROR EN LA DESCRIPCIÓN'),
)

TIPO_NOTA_CREDITO_SIN_DEVOLUCION = (
    (1, 'ANULACIÓN DE LA OPERACIÓN'),
    (2, 'ANULACIÓN POR ERROR EN EL RUC'),
    (4, 'DESCUENTO GLOBAL'),
    (5, 'DESCUENTO POR ÍTEM'),
    (8, 'BONIFICACIÓN'),
    (9, 'DISMINUCIÓN EN EL VALOR'),
    (10, 'OTROS CONCEPTOS'),
    (11, 'AJUSTES AFECTOS AL IVAP'),
    (12, 'AJUSTES DE OPERACIONES DE EXPORTACIÓN'),
    (13, 'AJUSTES - MONTOS Y/O FECHAS DE PAGO'),
)

TIPO_NOTA_CREDITO_CON_DEVOLUCION = (
    (6, 'DEVOLUCIÓN TOTAL'),
    (7, 'DEVOLUCIÓN POR ÍTEM'),
)

TIPO_NOTA_CREDITO = TIPO_NOTA_CREDITO_CON_DEVOLUCION + TIPO_NOTA_CREDITO_SIN_DEVOLUCION + TIPO_NOTA_CREDITO_SIN_NADA


TIPO_NOTA_DEBITO = (
    (1, 'INTERESES POR MORA'),
    (2, 'AUMENTO DE VALOR'),
    (3, 'PENALIDADES'),
    (4, 'AJUSTES AFECTOS AL IVAP'),
    (5, 'AJUSTES DE OPERACIONES DE EXPORTACIÓN'),
)


ESTADOS_TRASLADO_PRODUCTO = (
    (1, 'EN PROCESO'),
    (2, 'TRASLADO ENVIADO'),
    (3, 'TRASLADO RECEPCIONADO'),
    (4, 'ANULADO'),
    )

ESTADOS_TRASLADO_PRODUCTO_DETALLE = (
    (1, 'EN PROCESO'),
    (2, 'ENVIADO'),
    (3, 'RECEPCIONADO PARCIALMENTE'),
    (4, 'RECEPCIONADO'),
    )


ESTADOS_INGRESO_RECLAMO_GARANTIA = (
    (1, 'EN PROCESO'),
    (2, 'PENDIENTE'),
    (3, 'CONTROL'),
    (4, 'ANULADO'),
    (5, 'POR ENTREGAR'),
    (6, 'CONCLUIDO'),
    )

ESTADOS_CONTROL_RECLAMO_GARANTIA = (
    (1, 'EN PROCESO'),
    (2, 'CONCLUIDO'),
    (3, 'SALIDA GARANTIA'),
    )

ESTADOS_SALIDA_RECLAMO_GARANTIA = (
    (1, 'EN PROCESO'),
    (2, 'CONCLUIDO'),
    )

TIPOS_COMISION = (
    (1, 'MIXTA'),
    (2, 'SOBRE FLUJO'),
    )

TIPO_PAGO_BOLETA = (
    (1, 'FIN DE MES'),
    (2, 'GRATIFICACION'),
    (3, 'LIQUIDACIÓN'),
    )

TIPO_PAGO_RECIBO = (
    (1, 'QUINCENA'),
    (2, 'FIN DE MES'),
    (3, 'GRATIFICACION'),
    (4, 'VACACIONES'),
    (5, 'LIQUIDACION'),
    )

YEARS = (
    (2022, '2022'),
    (2023, '2023'),
)

MESES = (
    (1, 'ENERO'),
    (2, 'FEBRERO'),
    (3, 'MARZO'),
    (4, 'ABRIL'),
    (5, 'MAYO'),
    (6, 'JUNIO'),
    (7, 'JULIO'),
    (8, 'AGOSTO'),
    (9, 'SETIEMBRE'),
    (10, 'OCTUBRE'),
    (11, 'NOVIEMBRE'),
    (12, 'DICIEMBRE'),
    )

TIPO_PRESTAMO = (
    (1, 'PRESTAMO'),
    (2, 'DEVOLUCION'),
    )

ESTADO_PRESTAMO_CAJA_CHICA = (
    (1, 'PENDIENTE'),
    (2, 'CANCELADO'),
    )

ESTADO_CAJA_CHICA = (
        (1, 'ABIERTO'),
        (2, 'CERRADO'),
        (3, 'USADO'),
    )

ESTADO_RECIBO_CAJA_CHICA = (
        (1, 'BORRADOR'),
        (2, 'PENDIENTE'),
        (3, 'CANCELADO'),
    )

MEDIO = (
    (1, 'FACEBOOK'),
    (2, 'INSTAGRAM'),
    (5, 'TIKTOK'),
    (6, 'YOUTUBE'),
    (7, 'WHATSAPP'),
    (3, 'LLAMADA'),
    (4, 'EVENTOS'),
    (8, 'PÁGINA WEB'),
    (9, 'POR RECOMENDACIÓN'),
    (10, 'PENDIENTE'),
)

ESTADOS_CLIENTE = (
    (1, 'NUEVO'),
    (2, 'POTENCIAL'),
    (3, 'INTERESADO'),
    (4, 'FINAL'),
    (5, 'ESTRELLA'),
    (6, 'DEUDOR'),
    (7, 'DEUDOR ESTRELLA'),
)

TIPO_ACTIVIDAD = (
    (1, 'REUNIÓN'),
    (2, 'VISITA'),
    (3, 'LLAMADA'),
    (4, 'CORREO'),
    (5, 'EVENTO'),
    (6, 'SOPORTE TÉCNICO'),
    (7, 'CARACTERÍSTICAS TÉCNICAS'),
    (8, 'NUEVOS PRODUCTOS SOLICITADOS'),
)

ESTADOS_EVENTO_CRM = (
    (1, 'ACTIVO'),
    (2, 'EN PROCESO'),
    (3, 'FINALIZADO'),
    )

PRIORIDAD_TAREA = (
    (1, 'ALTA'),
    (2, 'MEDIA'),
    (3, 'BAJA'),
    )
    
ESTADO_TAREA = (
    (1, 'ASIGNADO'),
    (2, 'EN PROCESO'),
    (3, 'FINALIZADO'),
    (4, 'REAPERTURADO'),
    )
    
MOTIVO_INASISTENCIA = (
    (1, 'ASISTIO'),
    (2, 'FALTA'),
    (3, 'PERMISO'),
    (4, 'VACACIONES'),
    )

ESTADO_SOLICITUD_INASISTENCIA = (
    (1, 'SOLICITADO'),
    (2, 'APROBADO'),
    (3, 'RECHAZADO'),
    )

TIPO_ENCUESTA_CRM = (
    (1, 'VENTA'),
    (2, 'EVENTO'),
    (3, 'SATISFACCION'),
    )

TIPO_PREGUNTA_CRM = (
    (1, 'UNICA OPCION'),
    (2, 'MULTIPLE'),
    (3, 'ABIERTA'),
    )

MENSAJE_DAR_ALTA = 'Operación exitosa: El registro fue dado de alta.'
MENSAJE_ACTUALIZACION = 'Operación exitosa: El registro fue actualizado.'
MENSAJE_DAR_BAJA = 'Operación exitosa: El registro fue dado de baja.'
MENSAJE_COMPROBANTE_COMPRA = 'Operación exitosa: El comprobante fue registrado.'
MENSAJE_REGISTRAR_SALIDA = 'Operación exitosa: La Hora de Salida fue registrada.'

MENSAJE_ELIMINAR_ITEM = 'Operación exitosa: El registro fue eliminado.'
MENSAJE_RECHAZAR_OFERTA_PROVEEDOR = 'Operación exitosa: La Oferta fue Rechazada.'
MENSAJE_GENERAR_REQUERIMIENTO_PROVEEDOR = 'Operación exitosa: Requerimiento Proveedor generado.'
MENSAJE_GENERAR_ORDEN_COMPRA = 'Operación exitosa: Orden de Compra generada.'
MENSAJE_GENERAR_COMPROBANTE_COMPRA_PI = 'Operación exitosa: Generar Comprobante de Compra PI.'
MENSAJE_GUARDAR_COMPROBANTE_COMPRA_PI = 'Operación exitosa: Comprobante de Compra PI Guardado.'
MENSAJE_ANULAR_COMPROBANTE_COMPRA_PI = 'Operación exitosa: Comprobante de Compra PI Anulado.'
MENSAJE_ERROR_ANULAR_COMPROBANTE_COMPRA_PI= 'No se puede anular el Comprobante de Compra PI, verifique los procesos siguientes.'
MENSAJE_GENERAR_COMPROBANTE_COMPRA_MERCHANDISING = 'Operación exitosa: Generar Comprobante de Compra Merchandising.'

MENSAJE_FINALIZAR_INVENTARIO_ACTIVO = 'Operación exitosa: El Inventario fue Finalizado.'

MENSAJE_GUARDAR_COTIZACION = 'Operación exitosa: La cotización fue guardada con éxito.'
MENSAJE_ANULAR_COTIZACION = 'Operación exitosa: La cotización fue anulada con éxito.'
MENSAJE_CLONAR_COTIZACION = 'Operación exitosa: La cotización fue clonada con éxito.'
MENSAJE_RESERVAR_COTIZACION = 'Operación exitosa: La cotización fue reservada con éxito.'
MENSAJE_ANULAR_RESERVAR_COTIZACION = 'Operación exitosa: La reserva fue anulada con éxito.'
MENSAJE_CONFIRMAR_COTIZACION = 'Operación exitosa: La cotización fue confirmada con éxito.'
MENSAJE_ANULAR_CONFIRMAR_COTIZACION = 'Operación exitosa: La confirmación fue anulada con éxito.'
MENSAJE_GENERAR_FACTURA= 'Operación exitosa: La factura fue generada con éxito.'
MENSAJE_GENERAR_BOLETA= 'Operación exitosa: La boleta fue generada con éxito.'
MENSAJE_GENERAR_GUIA= 'Operación exitosa: La guía fue generada con éxito.'
MENSAJE_INGRESO_RECLAMO_GARANTIA= 'Operación exitosa: El ingreso reclamo garantía fue generado con éxito.'
MENSAJE_CONTROL_RECLAMO_GARANTIA= 'Operación exitosa: La nota de control fue guardada con éxito.'
MENSAJE_SALIDA_RECLAMO_GARANTIA= 'Operación exitosa: La salida del reclamo por garantía fue generada con éxito.'

MENSAJE_FINALIZAR_SOLICITUD_PRESTAMO_MATERIALES = 'Operación exitosa: La Solicitud de Prestamo fue finalizada.'
MENSAJE_CONFIRMAR_SOLICITUD_PRESTAMO_MATERIALES = 'Operación exitosa: La Solicitud de Prestamo fue confirmada.'
MENSAJE_ANULAR_SOLICITUD_PRESTAMO_MATERIALES = 'Operación exitosa: La Solicitud de Prestamo fue anulada.'
MENSAJE_GENERAR_NOTA_SALIDA = 'Operación exitosa: La Nota de Salida fue generada.'
MENSAJE_CONCLUIR_NOTA_SALIDA = 'Operación exitosa: La Nota de Salida fue concluida.'
MENSAJE_ANULAR_CONTEO = 'Operación exitosa: El conteo fue anulado.'
MENSAJE_ANULAR_NOTA_SALIDA = 'Operación exitosa: La Nota de Salida fue anulada.'
MENSAJE_GENERAR_DESPACHO = 'Operación exitosa: El despacho fue generada.'
MENSAJE_CONCLUIR_DESPACHO = 'Operación exitosa: El despacho fue concluido.'
MENSAJE_ANULAR__DESPACHO = 'Operación exitosa: El despacho fue anulado.'
MENSAJE_FINALIZAR_SIN_GUIA_DESPACHO = 'Operación exitosa: El despacho fue finalizado sin guia.'
MENSAJE_GENERAR_NOTA_DEVOLUCION = 'Operación exitosa: La Nota de Devolución fue generada.'

MENSAJE_ELIMINAR_DEUDA = 'Operación exitosa: Deuda eliminada.'
MENSAJE_ERROR_ELIMINAR_DEUDA = 'No se pudo eliminar la deuda, contactar con el administrador.'

MENSAJE_GUARDAR_ENVIO = 'Operación exitosa: El envio fue guardado con éxito.'
MENSAJE_GUARDAR_RECEPCION = 'Operación exitosa: La recepción fue guardado con éxito.'

MENSAJE_ANULAR_ORDEN_COMPRA = 'Operación exitosa: La Orden de Compra fue anulada.'
MENSAJE_ANULAR_NOTA_CONTROL_CALIDAD_STOCK = 'Operación exitosa: La Nota Control Calidad Stock fue anulada.'
MENSAJE_CONCLUIR_NOTA_CONTROL_CALIDAD_STOCK = 'Operación exitosa: La Nota Control Calidad Stock fue concluida.'

MENSAJE_CONCLUIR_TRASPASO_STOCK = 'Operación exitosa: El Traspaso Stock fue concluido.'

MENSAJE_GENERAR_DOCUMENTO_AJUSTE_INVENTARIO = 'Operación exitosa: Inventario Materiales fue concluido. Documento de Ajuste de Inventario generado'
MENSAJE_AJUSTE_INVENTARIO_MATERIALES = 'Operación exitosa: Ajuste Inventario Materiales fue concluido.'
MENSAJE_GENERAR_DOCUMENTO_AJUSTE_INVENTARIO_MERCHANDISING = 'Operación exitosa: Inventario Merchandising fue concluido. Documento de Ajuste de Inventario generado'
MENSAJE_AJUSTE_INVENTARIO_MERCHANDISING = 'Operación exitosa: Ajuste Inventario Merchandising fue concluido.'
MENSAJE_CONCLUIR_TRANSFORMACION_PRODUCTOS = 'Operación exitosa: La Transformacion de productos fue concluido.'
MENSAJE_SOLICITAR_REQUERIMIENTO = 'Operación exitosa: El Requerimiento fue Solicitado.'
MENSAJE_EDITAR_REQUERIMIENTO = 'Operación exitosa: El Requerimiento paso a estado Borrador.'
MENSAJE_RETROCEDER_REQUERIMIENTO = 'Operación exitosa: El Requerimiento paso a estado Solicitado.'
MENSAJE_FINALIZAR_RENDICION_REQUERIMIENTO = 'Operación exitosa: La rendición del Requerimiento finalizó.'
MENSAJE_APROBAR_RENDICION_REQUERIMIENTO = 'Operación exitosa: La rendición del Requerimiento fue aprobada.'
MENSAJE_EDITAR_RENDICION_REQUERIMIENTO = 'Operación exitosa: La rendición del Requerimiento paso a estado Requerimiento Aprobado.'
MENSAJE_RETROCEDER_RENDICION_REQUERIMIENTO = 'Operación exitosa: La rendición del Requerimiento paso a estado Revisar Rendición.'
MENSAJE_REMOVER_RECIBO_BOLETA_PAGO = 'Operación exitosa: El Recibo de Boleta de Pago fue removido.'
MENSAJE_REMOVER_RECIBO_SERVICIO = 'Operación exitosa: El Recibo de Servicio fue removido.'
MENSAJE_REMOVER_REQUERIMIENTO = 'Operación exitosa: El Requerimiento fue removido.'
MENSAJE_CONCLUIR_CHEQUE_FISICO = 'Operación exitosa: El Cheque Fisico fue concluido con éxito.'

MENSAJE_SOLICITAR_CHEQUE= 'Operación exitosa: El Cheque fue Solicitado.'
MENSAJE_EDITAR_CHEQUE = 'Operación exitosa: El Cheque paso a estado Abierto.'
MENSAJE_POR_CERRAR_CHEQUE = 'Operación exitosa: El Cheque paso a estado Por Cerrar.'

MENSAJE_CONFIRMAR_DOCUMENTO_RECLAMO = 'Operación exitosa: El Documento de Reclamo fue Confirmado.'
MENSAJE_GUARDAR_EVENTO_DETALLE = 'Operación exitosa: El detalle evento fue guardado con éxito.'

MENSAJE_CONCLUIR_CAMBIO_SOCIEDAD_STOCK = 'Operación exitosa: El Cambio de Sociedad Stock fue concluido.'

COLOR_DEFAULT = '#04fb1d'
PIE_DE_PAGINA_DEFAULT = '''GRUPO MULTIPLAY
Celular: 974899069 / Teléfono: 2536767
Dirección: CAL. RICARDO ANGULO 1226 URB. CORPAC, SAN ISIDRO-LIMA-LIMA / E-mail: info@multiplay.com.pe / Web: www.multiplay.com.pe'''

EMAIL_REMITENTE = 'no-responder@multiplay.com.pe'

DICCIONARIO_TOTALES={
    # 'descuento_global':'Descuento Global',
    # 'descuento_global_con_igv':'Descuento Global',
    # 'total_descuento':'Descuento',
    # 'total_descuento_con_igv':'Descuento',
    'descuento_cotizacion':'Descuento Extra',
    'total_anticipo':'Anticipo',
    'total_gravada':'Gravada',
    'total_inafecta':'Inafecta',
    'total_exonerada':'Exonerada',
    'total_igv':'I.G.V.',
    'total_gratuita':'Gratuita',
    # 'total_otros_cargos':'Otros Cargos',
    'otros_cargos_cotizacion':'Otros Cargos',
    'total_icbper':'ICBPER',
    'total':'Total',
}

SERIE_CONSULTA = (
        (1, 'PENDIENTE'),
        (2, 'SUBIDO'),
    )

ESTADOS_NOTA_CALIDAD_STOCK = (
    (1, 'EN PROCESO'),
    (2, 'POR REGISTRAR SERIES'),
    (3, 'CONCLUIDA'),
    (4, 'ANULADA'),
)

ESTADO_COMPROBANTE_MERCHANDISING = (
    (0, 'BORRADOR'),
    (1, 'PENDIENTE'),
    (2, 'RECIBIDO'),
    (3, 'ANULADO'),
    )


URL_MULTIPLAY = 'https://www.multiplay.com.pe/'

CHOICE_VACIO = ((None, '-----------------'),)
