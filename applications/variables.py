TIPO_DOCUMENTO_SUNAT = (
    ('6', 'RUC - REGISTRO ÚNICO DE CONTRIBUYENTE'),
    ('1', 'DNI - DOC. NACIONAL DE IDENTIDAD'),
    ('-', 'VARIOS - VENTAS MENORES A S/.700.00 Y OTROS'),
    ('4', 'CARNET DE EXTRANJERÍA'),
    ('7', 'PASAPORTE'),
    ('A', 'CÉDULA DIPLOMÁTICA DE IDENTIDAD'),
    ('0', 'NO DOMICILIADO, SIN RUC (EXPORTACIÓN)'),
    )

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
    (2, 'Suspensión temporal'),
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

TIPO_DOCUMENTO_CHOICES = (
    ('1', 'DNI - DOC. NACIONAL DE IDENTIDAD'),
    ('4', 'CARNET DE EXTRANJERÍA'),
    ('7', 'PASAPORTE'),
    ('A', 'CÉDULA DIPLOMÁTICA DE IDENTIDAD')
    )

TIPO_COMPROBANTE = (
    (1, 'FACTURA'),
    (2, 'BOLETA'),
    )
TIPO_VENTA= (
    (1, 'CONTADO'),
    (2, 'CREDITO'),
    )

ESTADOS = (
    (1, 'Alta'),
    (2, 'Baja'),
    )

ESTADO_NOTA_INGRESO = (
    (1, 'BORRADOR'),
    (2, 'FINALIZADO'),
    (3, 'ANULADO'),
    )

ESTADO_COMPROBANTE = (
    (1, 'PENDIENTE'),
    (2, 'ANULADO'),
    )

ESTADO_COMPROBANTE_PI = (
    (0, 'PARCIAL'),
    (1, 'PENDIENTE'),
    (2, 'RECIBIDO'),
    (3, 'ANULADO'),
    )

ESTADO_COMPROBANTE_CI = (
    (1, 'BORRADOR'),
    (2, 'FINALIZADO'),
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
    (3, 'ANULADO'),
    )

ESTADOS_COTIZACION_VENTA = (
    (1, 'BORRADOR'),
    (2, 'PENDIENTE'),
    (3, 'RESERVADO'),
    (4, 'CONFIRMADO'),
    (5, 'VENCIDO'),
    (6, 'SIN CONFIRMAR'),
    (7, 'DE BAJA'),
    )



MENSAJE_DAR_ALTA = 'Operación exitosa: El registro fue dado de alta.'
MENSAJE_ACTUALIZACION = 'Operación exitosa: El registro fue actualizado.'
MENSAJE_DAR_BAJA = 'Operación exitosa: El registro fue dado de baja.'
MENSAJE_COMPROBANTE_COMPRA = 'Operación exitosa: El comprobante fue registrado.'
MENSAJE_REGISTRAR_SALIDA = 'Operación exitosa: La Hora de Salida fue registrada.'

MENSAJE_ELIMINAR_ITEM = 'Operación exitosa: El registro fue eliminado.'
MENSAJE_RECHAZAR_OFERTA_PROVEEDOR = 'Operación exitosa: La Oferta fue Rechazada.'
MENSAJE_GENERAR_REQUERIMIENTO_PROVEEDOR = 'Operación exitosa: Generar Requerimiento Proveedor.'
MENSAJE_GENERAR_ORDEN_COMPRA = 'Operación exitosa: Generar Orden de Compra.'
MENSAJE_GENERAR_COMPROBANTE_COMPRA_PI = 'Operación exitosa: Generar Comprobante de Compra PI.'
MENSAJE_FINALIZAR_INVENTARIO_ACTIVO = 'Operación exitosa: El Inventario fue Finalizado.'


COLOR_DEFAULT = '#8B32A8'
PIE_DE_PAGINA_DEFAULT = 'GRUPO MULTIPLAY'

EMAIL_REMITENTE = 'no-responder@multiplay.com.pe'


MENSAJE_ANULAR_ORDEN_COMPRA = 'Operación exitosa: La Orden de Compra fue anulada.'