from decimal import Decimal

from applications import cobranza


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