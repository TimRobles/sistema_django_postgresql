TIPO_DOCUMENTO_CHOICES = (
        ('6', 'RUC - REGISTRO ÚNICO DE CONTRIBUYENTE'),
        ('1', 'DNI - DOC. NACIONAL DE IDENTIDAD'),
        ('-', 'VARIOS - VENTAS MENORES A S/.700.00 Y OTROS'),
        ('4', 'CARNET DE EXTRANJERÍA'),
        ('7', 'PASAPORTE'),
        ('A', 'CÉDULA DIPLOMÁTICA DE IDENTIDAD'),
        ('0', 'NO DOMICILIADO, SIN RUC (EXPORTACIÓN)'),
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

ESTADOS = (
        (1, 'Alta'),
        (2, 'Baja'),
        )

MENSAJE_DAR_BAJA = 'Operación exitosa: El registro fue dado de baja.'
