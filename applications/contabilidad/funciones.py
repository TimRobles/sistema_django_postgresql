from decimal import Decimal
from django.db import models
from applications.importaciones import *
from applications.contabilidad.models import EsSalud, ReciboBoletaPago, ReciboServicio

from applications.datos_globales.models import RemuneracionMinimaVital
from applications.caja_chica.models import Requerimiento


def calcular_datos_boleta(obj):
    datos_planilla = obj.datos_planilla
    comision_fondo_pensiones = datos_planilla.fondo_pensiones.ComisionFondoPensiones_fondo_pensiones.latest('fecha_vigencia')
    rmv = RemuneracionMinimaVital.objects.latest('fecha_inicio')
    essalud = EsSalud.objects.latest('fecha_inicio')
    obj.haber_mensual = datos_planilla.sueldo_bruto
    obj.lic_con_goce_haber = Decimal('0.00')
    obj.dominical = Decimal('0.00')
    obj.movilidad = datos_planilla.movilidad
    obj.asig_familiar = Decimal('0.00')
    if datos_planilla.asignacion_familiar:
        obj.asig_familiar = (Decimal(0.1) * rmv.monto).quantize(Decimal('.01'))
    obj.vacaciones = Decimal('0.00')
    obj.gratificacion = Decimal('0.00')
    obj.ley29351 = Decimal('0.00')
    obj.bonif_1mayo = Decimal('0.00')
    obj.essalud = (datos_planilla.sueldo_bruto * essalud.porcentaje).quantize(Decimal('0.01'))
    if essalud.ley30334 and obj.tipo == 2: #GRATIFICACIÓN
        obj.ley29351 = (datos_planilla.sueldo_bruto * essalud.porcentaje).quantize(Decimal('0.01'))
        obj.essalud = Decimal('0.00')

    obj.aporte_obligatorio = (datos_planilla.sueldo_bruto * comision_fondo_pensiones.aporte_obligatorio).quantize(Decimal('0.01'))
    if datos_planilla.tipo_comision == 1:
        obj.comision_porcentaje = (datos_planilla.sueldo_bruto * comision_fondo_pensiones.comision_flujo_mixta).quantize(Decimal('0.01'))
    else:
        obj.comision_porcentaje = (datos_planilla.sueldo_bruto * comision_fondo_pensiones.comision_flujo).quantize(Decimal('0.01'))
    obj.prima_seguro = (datos_planilla.sueldo_bruto * comision_fondo_pensiones.prima_seguro).quantize(Decimal('0.01'))
    
    obj.impuesto_quinta = Decimal('0.00')
    obj.neto_recibido = obj.haber_mensual + obj.lic_con_goce_haber + obj.dominical + obj.movilidad + obj.asig_familiar + obj.vacaciones + obj.gratificacion + obj.ley29351 + obj.bonif_1mayo - (obj.aporte_obligatorio + obj.comision_porcentaje + obj.prima_seguro)


def calculo_montos(obj):
    totales_parciales = {}
    cheque = obj
    recibo_boleta = ReciboBoletaPago.objects.filter(
                    content_type = ContentType.objects.get_for_model(cheque),
                    id_registro = cheque.id,
                    )
    totales_parciales['total_boleta'] = recibo_boleta.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']

    recibo_servicio = ReciboServicio.objects.filter(
                    content_type = ContentType.objects.get_for_model(cheque),
                    id_registro = cheque.id,
                    )
    totales_parciales['total_servicio'] = recibo_servicio.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']

    requerimiento = Requerimiento.objects.filter(
                    content_type = ContentType.objects.get_for_model(cheque),
                    id_registro = cheque.id,
                    )
    totales_parciales['total_requerimiento'] = requerimiento.aggregate(models.Sum('monto_usado'))['monto_usado__sum']

    return totales_parciales