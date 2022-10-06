from datetime import date, timedelta
from decimal import Decimal

from applications import cobranza
from django.contrib.contenttypes.models import ContentType

from applications.funciones import tipo_de_cambio

def convertir_moneda(tipo_cambio, moneda_destino, moneda_inicial):
    if moneda_inicial == moneda_destino:
        return Decimal('1')
    if moneda_inicial.secundario and moneda_destino.principal:
        return tipo_cambio
    if moneda_inicial.principal and moneda_destino.secundario:
        return 1/tipo_cambio
        
    return Decimal('0')


def movimientos_bancarios(cuenta_bancaria):
    movimientos = []
    ingresos = cobranza.models.Ingreso.objects.filter(cuenta_bancaria__id=cuenta_bancaria)
    egresos = cobranza.models.Egreso.objects.filter(cuenta_bancaria__id=cuenta_bancaria)
    for ingreso in ingresos:
        ingreso.ingreso = ingreso.monto
        movimientos.append(ingreso)
    for egreso in egresos:
        egreso.egreso = egreso.monto
        movimientos.append(egreso)
    return movimientos


def generarDeuda(documento, request):
    if len(documento.confirmacion.ConfirmacionVentaCuota_confirmacion_venta.all())>0:
        cuota_final = documento.confirmacion.ConfirmacionVentaCuota_confirmacion_venta.order_by('-dias_calculo')[0]
        if cuota_final.fecha_pago:
            fecha_vencimiento = cuota_final.fecha_pago
        else:
            fecha_vencimiento = date.today() + timedelta(cuota_final.dias_pago)
    else:
        fecha_vencimiento = date.today()
    obj = cobranza.models.Deuda.objects.create(
        content_type = ContentType.objects.get_for_model(documento),
        id_registro = documento.id,
        monto = documento.confirmacion.total,
        moneda = documento.confirmacion.moneda,
        tipo_cambio = tipo_de_cambio(),
        fecha_deuda = date.today(),
        fecha_vencimiento = fecha_vencimiento,
        sociedad = documento.confirmacion.sociedad,
        cliente = documento.confirmacion.cliente,
        created_by = request.user,
        updated_by = request.user,
        )
    
    for cuota in documento.confirmacion.ConfirmacionVentaCuota_confirmacion_venta.all():
        if cuota.fecha_pago:
            fecha = cuota.fecha_pago
        else:
            fecha = date.today() + timedelta(cuota.dias_pago)
        cobranza.models.Cuota.objects.create(
            deuda = obj,
            fecha = fecha,
            monto = cuota.monto,
            created_by = request.user,
            updated_by = request.user,
        )

    return fecha_vencimiento


def eliminarDeuda(documento):
    try:
        obj = cobranza.models.Deuda.objects.get(
            content_type = ContentType.objects.get_for_model(documento),
            id_registro = documento.id,
            )
        obj.delete()

        return True
    except:
        return False