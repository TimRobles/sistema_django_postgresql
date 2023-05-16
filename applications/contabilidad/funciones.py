from decimal import Decimal
from django.db import models
from applications.importaciones import *
from applications.contabilidad.models import EsSalud
from applications.datos_globales.models import RemuneracionMinimaVital


def calcular_datos_boleta(obj):
    datos_planilla = obj.datos_planilla
    if datos_planilla.fondo_pensiones:
        comision_fondo_pensiones = datos_planilla.fondo_pensiones.ComisionFondoPensiones_fondo_pensiones.latest('fecha_vigencia')
        aporte_obligatorio = comision_fondo_pensiones.aporte_obligatorio
        comision_flujo_mixta = comision_fondo_pensiones.comision_flujo_mixta
        comision_flujo = comision_fondo_pensiones.comision_flujo
        prima_seguro = comision_fondo_pensiones.prima_seguro
    else:
        aporte_obligatorio = Decimal('0.00')
        comision_flujo_mixta = Decimal('0.00')
        comision_flujo = Decimal('0.00')
        prima_seguro = Decimal('0.00')
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
    obj.cts = Decimal('0.00')
    obj.bonif_1mayo = Decimal('0.00')
    obj.essalud = (datos_planilla.sueldo_bruto * essalud.porcentaje).quantize(Decimal('0.01'))
    if essalud.ley30334 and obj.tipo == 2: #GRATIFICACIÓN
        obj.ley29351 = (datos_planilla.sueldo_bruto * essalud.porcentaje).quantize(Decimal('0.01'))
        obj.essalud = Decimal('0.00')

    obj.aporte_obligatorio = (datos_planilla.sueldo_bruto * aporte_obligatorio).quantize(Decimal('0.01'))
    if datos_planilla.tipo_comision == 1:
        obj.comision = (datos_planilla.sueldo_bruto * comision_flujo_mixta).quantize(Decimal('0.01'))
    else:
        obj.comision = (datos_planilla.sueldo_bruto * comision_flujo).quantize(Decimal('0.01'))
    obj.prima_seguro = (datos_planilla.sueldo_bruto * prima_seguro).quantize(Decimal('0.01'))
    
    if not obj.impuesto_quinta:
        obj.impuesto_quinta = Decimal('0.00')
    obj.neto_recibido = obj.haber_mensual + obj.lic_con_goce_haber + obj.dominical + obj.movilidad + obj.asig_familiar + obj.vacaciones + obj.gratificacion + obj.ley29351 + obj.cts + obj.bonif_1mayo - (obj.aporte_obligatorio + obj.comision + obj.prima_seguro + obj.impuesto_quinta)