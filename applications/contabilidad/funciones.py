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
    recibos_boleta_pago = ReciboBoletaPago.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
    recibos_servicio = ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
    recibos_caja_chica = ReciboCajaChica.objects.filter(cheque = cheque)
    requerimientos = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
    cheques_fisicos = ChequeFisico.objects.filter(cheque = cheque)
    vuelto_extra = ChequeVueltoExtra.objects.filter(cheque = cheque)
    total_boleta_pago = recibos_boleta_pago.aggregate(models.Sum('monto'))['monto__sum']
    total_boleta_pago_pagado = recibos_boleta_pago.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
    total_servicio = recibos_servicio.aggregate(models.Sum('monto'))['monto__sum']
    total_servicio_pagado = recibos_servicio.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
    total_caja_chica = recibos_caja_chica.aggregate(models.Sum('monto'))['monto__sum']
    total_caja_chica_pagado = recibos_caja_chica.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
    total_requerimiento = requerimientos.aggregate(models.Sum('monto'))['monto__sum']
    total_requerimiento_usado = requerimientos.aggregate(models.Sum('monto_usado'))['monto_usado__sum']
    total_cheque_fisico = cheques_fisicos.aggregate(models.Sum('monto'))['monto__sum']
    total_cheque_fisico_comision = cheques_fisicos.aggregate(models.Sum('comision'))['comision__sum']
    total_cheque_fisico_recibido = cheques_fisicos.aggregate(models.Sum('monto_recibido'))['monto_recibido__sum']
    total_monto_requerido = total_boleta_pago + total_servicio + total_caja_chica + total_requerimiento