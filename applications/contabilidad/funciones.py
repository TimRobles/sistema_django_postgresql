from decimal import Decimal
from django.db import models
from applications.caja_chica.models import ReciboCajaChica, Requerimiento
from applications.importaciones import *
from applications.contabilidad.models import ChequeFisico, ChequeVueltoExtra, EsSalud, ReciboBoletaPago, ReciboServicio
from applications.datos_globales.models import RemuneracionMinimaVital


def calcular_datos_boleta(obj):
    datos_planilla = obj.datos_planilla
    fecha_boleta = date(obj.year, obj.month, 1)
    if datos_planilla.fondo_pensiones:
        comision_fondo_pensiones = datos_planilla.fondo_pensiones.ComisionFondoPensiones_fondo_pensiones.filter(fecha_vigencia__lte=fecha_boleta).latest('fecha_vigencia')
        aporte_obligatorio = comision_fondo_pensiones.aporte_obligatorio
        comision_flujo_mixta = comision_fondo_pensiones.comision_flujo_mixta
        comision_flujo = comision_fondo_pensiones.comision_flujo
        prima_seguro = comision_fondo_pensiones.prima_seguro
    else:
        aporte_obligatorio = Decimal('0.00')
        comision_flujo_mixta = Decimal('0.00')
        comision_flujo = Decimal('0.00')
        prima_seguro = Decimal('0.00')
    rmv = RemuneracionMinimaVital.objects.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio')
    essalud = EsSalud.objects.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio')
    obj.haber_mensual = (datos_planilla.sueldo_bruto * obj.dias_trabajados / Decimal('30') + Decimal('0.001')).quantize(Decimal('.01'))
    obj.gratificacion = Decimal('0.00')
    if datos_planilla.sociedad.TamañoEmpresa_sociedad.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio').tipo_empresa==1 and obj.tipo == 2: #MICRO EMPRESA Y GRATIFICACIÓN
        obj.haber_mensual = Decimal('0.00')
    elif datos_planilla.sociedad.TamañoEmpresa_sociedad.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio').tipo_empresa==2 and obj.tipo == 2: #PEQUEÑA EMPRESA Y GRATIFICACIÓN
        obj.haber_mensual = Decimal('0.00')
        obj.gratificacion = (datos_planilla.sueldo_bruto/2 + Decimal('0.001')).quantize(Decimal('.01'))
    elif datos_planilla.sociedad.TamañoEmpresa_sociedad.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio').tipo_empresa==3 and obj.tipo == 2: #MEDIANA EMPRESA Y GRATIFICACIÓN
        obj.haber_mensual = Decimal('0.00')
        obj.gratificacion = (datos_planilla.sueldo_bruto + Decimal('0.001')).quantize(Decimal('.01'))
    obj.lic_con_goce_haber = Decimal('0.00')
    obj.dominical = Decimal('0.00')
    obj.movilidad = datos_planilla.movilidad
    obj.asig_familiar = Decimal('0.00')
    if datos_planilla.asignacion_familiar:
        obj.asig_familiar = (Decimal(0.1) * rmv.monto + Decimal('0.001')).quantize(Decimal('.01'))
    obj.vacaciones = Decimal('0.00')
    obj.compra_vacaciones = Decimal('0.00')
    obj.ley29351 = Decimal('0.00')
    obj.cts = Decimal('0.00')
    obj.bonif_1mayo = Decimal('0.00')
    if obj.month == 5 and fecha_boleta.weekday()==6 and obj.tipo == 1:
        obj.bonif_1mayo = (obj.haber_mensual / Decimal('30.0') + Decimal('0.001')).quantize(Decimal('.01'))
    
    obj.essalud = ((obj.haber_mensual + obj.compra_vacaciones + obj.asig_familiar + obj.bonif_1mayo) * essalud.porcentaje + Decimal('0.001')).quantize(Decimal('0.01'))
    if essalud.ley30334 and obj.tipo == 2: #GRATIFICACIÓN
        obj.ley29351 = (obj.gratificacion * essalud.porcentaje + Decimal('0.001')).quantize(Decimal('0.01'))
        obj.essalud = Decimal('0.00')

    obj.aporte_obligatorio = ((obj.haber_mensual + obj.compra_vacaciones + obj.asig_familiar + obj.bonif_1mayo) * aporte_obligatorio + Decimal('0.001')).quantize(Decimal('0.01'))
    if datos_planilla.tipo_comision == 1:
        obj.comision = ((obj.haber_mensual + obj.compra_vacaciones + obj.asig_familiar + obj.bonif_1mayo) * comision_flujo_mixta + Decimal('0.001')).quantize(Decimal('0.01'))
    else:
        obj.comision = ((obj.haber_mensual + obj.compra_vacaciones + obj.asig_familiar + obj.bonif_1mayo) * comision_flujo + Decimal('0.001')).quantize(Decimal('0.01'))
    obj.prima_seguro = ((obj.haber_mensual + obj.compra_vacaciones + obj.asig_familiar + obj.bonif_1mayo) * prima_seguro + Decimal('0.001')).quantize(Decimal('0.01'))
    
    if not obj.impuesto_quinta:
        obj.impuesto_quinta = Decimal('0.00')
    obj.neto_recibido = obj.haber_mensual + obj.compra_vacaciones + obj.lic_con_goce_haber + obj.dominical + obj.movilidad + obj.asig_familiar + obj.vacaciones + obj.gratificacion + obj.ley29351 + obj.cts + obj.bonif_1mayo - (obj.aporte_obligatorio + obj.comision + obj.prima_seguro + obj.impuesto_quinta)


def movimientos_cheque(cheque):
    movimientos = []
    
    for recibo_bp in ReciboBoletaPago.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id):
        tipo = 'BOLETA DE PAGO'
        foto = False
        fecha = recibo_bp.fecha_pagar
        concepto = recibo_bp.boleta_pago
        monto = recibo_bp.monto
        mora = Decimal('0.00')
        redondeo = recibo_bp.redondeo
        documentos = False
        voucher = recibo_bp.voucher
        fecha_pago = recibo_bp.fecha_pago
        monto_pagado = recibo_bp.monto_pagado
        estado = recibo_bp.get_estado_display()

        fila = []
        fila.append(tipo)
        fila.append(foto)
        fila.append(concepto)
        fila.append(fecha)
        fila.append(monto)
        fila.append(mora)
        fila.append(redondeo)
        fila.append(documentos)
        fila.append(voucher)
        fila.append(fecha_pago)
        fila.append(monto_pagado)
        fila.append(estado)
        movimientos.append(fila)

    for recibo_s in ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id):
        tipo = 'SERVICIO'
        foto = recibo_s.foto
        fecha = recibo_s.fecha_vencimiento
        concepto = recibo_s.servicio
        monto = recibo_s.monto
        mora = Decimal('0.00')
        redondeo = recibo_s.redondeo
        documentos = False
        voucher = recibo_s.voucher
        fecha_pago = recibo_s.fecha_pago
        monto_pagado = recibo_s.monto_pagado
        estado = recibo_s.get_estado_display()

        fila = []
        fila.append(tipo)
        fila.append(foto)
        fila.append(concepto)
        fila.append(fecha)
        fila.append(monto)
        fila.append(mora)
        fila.append(redondeo)
        fila.append(documentos)
        fila.append(voucher)
        fila.append(fecha_pago)
        fila.append(monto_pagado)
        fila.append(estado)
        movimientos.append(fila)

    for recibo_cc in ReciboCajaChica.objects.filter(cheque = cheque):
        tipo = 'CAJA CHICA'
        foto = False
        fecha = recibo_cc.fecha
        concepto = recibo_cc.concepto
        monto = recibo_cc.monto
        mora = Decimal('0.00')
        redondeo = Decimal('0.00')
        redondeo = recibo_cc.redondeo
        documentos = False
        voucher = False
        fecha_pago = recibo_cc.fecha_pago
        monto_pagado = recibo_cc.monto_pagado
        estado = recibo_cc.get_estado_display()

        fila = []
        fila.append(tipo)
        fila.append(foto)
        fila.append(concepto)
        fila.append(fecha)
        fila.append(monto)
        fila.append(mora)
        fila.append(redondeo)
        fila.append(documentos)
        fila.append(voucher)
        fila.append(fecha_pago)
        fila.append(monto_pagado)
        fila.append(estado)
        movimientos.append(fila)

    for requerimiento in Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id):
        tipo = 'REQUERIMIENTO'
        foto = False
        fecha = requerimiento.fecha
        concepto = requerimiento.concepto_final
        monto = requerimiento.monto
        mora = Decimal('0.00')
        redondeo = requerimiento.redondeo
        documentos = requerimiento.RequerimientoDocumento_requerimiento.all()
        if len(documentos) == 0:
            documentos = False
        voucher = False
        fecha_entrega = requerimiento.fecha_entrega
        monto_usado = requerimiento.monto_usado
        estado = requerimiento.get_estado_display()

        fila = []
        fila.append(tipo)
        fila.append(foto)
        fila.append(concepto)
        fila.append(fecha)
        fila.append(monto)
        fila.append(mora)
        fila.append(redondeo)
        fila.append(documentos)
        fila.append(voucher)
        fila.append(fecha_entrega)
        fila.append(monto_usado)
        fila.append(estado)
        movimientos.append(fila)

    try:
        movimientos.sort(key = lambda i: i[0]) #Fecha
    except:
        fila = []
        fila.append('')
        fila.append('ERROR. CONTACTAR A SOPORTE')
        fila.append('')
        fila.append('')
        fila.append(Decimal('0.00'))
        fila.append(Decimal('0.00'))
        fila.append(Decimal('0.00'))
        movimientos.append(fila)

    return movimientos
    

def movimientos_telecredito(telecredito):
    movimientos = []
    
    for recibo_bp in ReciboBoletaPago.objects.filter(content_type = ContentType.objects.get_for_model(telecredito), id_registro = telecredito.id):
        tipo = 'BOLETA DE PAGO'
        foto = False
        fecha = recibo_bp.fecha_pagar
        concepto = recibo_bp.boleta_pago
        monto = recibo_bp.monto
        voucher = recibo_bp.voucher
        fecha_pago = recibo_bp.fecha_pago
        monto_pagado = recibo_bp.monto_pagado
        estado = recibo_bp.get_estado_display()

        fila = []
        fila.append(tipo)
        fila.append(foto)
        fila.append(concepto)
        fila.append(fecha)
        fila.append(monto)
        fila.append(voucher)
        fila.append(fecha_pago)
        fila.append(monto_pagado)
        fila.append(estado)
        movimientos.append(fila)

    try:
        movimientos.sort(key = lambda i: i[0]) #Fecha
    except:
        fila = []
        fila.append('')
        fila.append('ERROR. CONTACTAR A SOPORTE')
        fila.append('')
        fila.append('')
        fila.append(Decimal('0.00'))
        fila.append(Decimal('0.00'))
        fila.append(Decimal('0.00'))
        movimientos.append(fila)

    return movimientos