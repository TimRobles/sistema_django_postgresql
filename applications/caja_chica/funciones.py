from datetime import date
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from applications.caja_chica.models import Requerimiento


def movimientos_caja_chica(caja_chica):
    movimientos = []
    
    #Saldo inicial
    fecha = date(caja_chica.year, caja_chica.month, 1)
    concepto = 'SALDO INICIAL'
    estado = 'ACTIVO'
    ingreso = caja_chica.saldo_inicial
    egreso = Decimal('0.00')
    saldo = Decimal('0.00')
    fila = []
    fila.append(fecha)
    fila.append(concepto)
    fila.append(estado)
    fila.append(ingreso)
    fila.append(egreso)
    fila.append(saldo)
    movimientos.append(fila)

    #Requerimientos
    for requerimiento in Requerimiento.objects.filter(content_type=ContentType.objects.get_for_model(caja_chica), id_registro=caja_chica.id,):

        fecha = requerimiento.fecha
        concepto = requerimiento.concepto
        estado = requerimiento.get_estado_display()
        ingreso = Decimal('0.00')
        egreso = requerimiento.monto
        saldo = Decimal('0.00')
        if requerimiento.estado > 2 and requerimiento.estado != 4:
            concepto = requerimiento.concepto_final
            egreso = requerimiento.monto_final
        if requerimiento.estado == 7:
            egreso = requerimiento.monto_usado
        moneda = requerimiento.moneda
        tipo_cambio = requerimiento.tipo_cambio
        if moneda != caja_chica.moneda:
            if moneda.id == 2: #Dólares
                egreso = (egreso * tipo_cambio).quantize(Decimal('0.01'))
        fila = []
        fila.append(fecha)
        fila.append(concepto)
        fila.append(estado)
        fila.append(ingreso)
        fila.append(egreso)
        fila.append(saldo)
        movimientos.append(fila)

    movimientos.sort(key = lambda i: i[3], reverse=True)
    movimientos.sort(key = lambda i: i[0])

    # #Recibos Caja Chica
    # for recibos_caja in ReciboCajaChica.objects.filter(caja_chica=caja_chica.id):

    #     fecha = recibos_caja.fecha
    #     concepto = recibos_caja.concepto
    #     estado = recibos_caja.get_estado_display()
    #     ingreso = recibos_caja.monto
    #     egreso = Decimal('0.00')
    #     saldo = Decimal('0.00')
    #     if recibos_caja.estado > 2 and recibos_caja.estado != 4:
    #         concepto = recibos_caja.concepto_final
    #         egreso = recibos_caja.monto_final
    #     if recibos_caja.estado == 7:
    #         egreso = recibos_caja.monto_usado
    #     moneda = recibos_caja.moneda

    #     fila = []
    #     fila.append(fecha)
    #     fila.append(concepto)
    #     fila.append(estado)
    #     fila.append(ingreso)
    #     fila.append(egreso)
    #     fila.append(saldo)
    #     movimientos.append(fila)

    # movimientos.sort(key = lambda i: i[3], reverse=True)
    # movimientos.sort(key = lambda i: i[0])
    #____________________________________________________

    return movimientos