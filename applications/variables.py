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
        ('007', 'Contador'),
        ('013', 'Director Ejecutivo'),
        ('014', 'Director General'),
        ('019', 'Gerente'),
        ('020', 'Gerente Ejecutivo'),
        ('021', 'Gerente General'),
        ('022', 'Gestor de Empresas'),
        ('025', 'Jefe'),
        ('029', 'Presidente'),
        ('032', 'Presidente Directorio'),
        ('033', 'Presidente Ejecutivo'),
        ('037', 'Representante no domiciliado'),
        ('040', 'Secretario'),
        ('043', 'Sub gerente'),
        ('048', 'Vicepresidente'),
        ('051', 'Titular gerente'),
        ('052', 'Socio Administrador'),
        ('998', 'Otros persona juridica'),
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

TIPO_DOCUMENTO_CHOICES = (
        ('1', 'DNI - DOC. NACIONAL DE IDENTIDAD'),
        ('4', 'CARNET DE EXTRANJERÍA'),
        ('7', 'PASAPORTE'),
        ('A', 'CÉDULA DIPLOMÁTICA DE IDENTIDAD')
        )

ESTADOS = (
        (1, 'Alta'),
        (2, 'Baja'),
        )

MENSAJE_DAR_ALTA = 'Operación exitosa: El registro fue dado de alta.'
MENSAJE_DAR_BAJA = 'Operación exitosa: El registro fue dado de baja.'
MENSAJE_REGISTRAR_SALIDA = 'Operación exitosa: La Hora de Salida fue registrada.'

MENSAJE_ELIMINAR_ITEM = 'Operación exitosa: El registro fue eliminado.'

COLOR_DEFAULT = '#8B32A8'
PIE_DE_PAGINA_DEFAULT = 'GRUPO MULTIPLAY'

EMAIL_REMITENTE = 'no-responder@multiplay.com.pe'