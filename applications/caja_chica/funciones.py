from datetime import date
from decimal import Decimal
from django.db import models

from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
import applications


def movimientos_caja_chica(caja_chica):
    movimientos = []

    #Saldo inicial
    fecha = date(caja_chica.year, caja_chica.month, 1)
    concepto = 'SALDO INICIAL'
    estado = 'ACTIVO'
    ingreso = caja_chica.saldo_inicial
    egreso = Decimal('0.00')
    saldo = Decimal('0.00')
    url = '#'
    fila = []
    fila.append(fecha)
    fila.append(concepto)
    fila.append(estado)
    fila.append(ingreso)
    fila.append(egreso)
    fila.append(saldo)
    fila.append(url)
    movimientos.append(fila)

    #Requerimientos
    for requerimiento in applications.caja_chica.models.Requerimiento.objects.filter(content_type=ContentType.objects.get_for_model(caja_chica), id_registro=caja_chica.id,):

        fecha = requerimiento.fecha
        concepto = requerimiento.concepto
        estado = requerimiento.get_estado_display()
        ingreso = Decimal('0.00')
        egreso = requerimiento.monto
        saldo = Decimal('0.00')
        if requerimiento.estado > 2 and requerimiento.estado != 4:
            concepto = requerimiento.concepto_final
            egreso = requerimiento.monto_final
            fecha = requerimiento.fecha_entrega
        if requerimiento.estado == 7:
            egreso = requerimiento.monto_usado
            fecha = requerimiento.fecha_entrega
        moneda = requerimiento.moneda
        tipo_cambio = requerimiento.tipo_cambio
        if moneda != caja_chica.moneda:
            if moneda.id == 2: #Dólares
                egreso = (egreso * tipo_cambio).quantize(Decimal('0.01'))
        url = reverse_lazy('caja_chica_app:requerimiento_detalle', kwargs={'pk':requerimiento.id})
        documentos = []
        for documento in requerimiento.RequerimientoDocumento_requerimiento.all():
            documentos.append(documento)
        fila = []
        fila.append(fecha)
        fila.append(concepto)
        fila.append(estado)
        fila.append(ingreso)
        fila.append(egreso)
        fila.append(saldo)
        fila.append(url)
        fila.append(documentos)
        movimientos.append(fila)

    #Recibos Caja Chica
    for recibos_caja in applications.caja_chica.models.ReciboCajaChica.objects.filter(caja_chica=caja_chica.id, estado=3):

        fecha = recibos_caja.fecha_pago
        concepto = recibos_caja.concepto
        estado = recibos_caja.get_estado_display()
        ingreso = recibos_caja.monto
        egreso = Decimal('0.00')
        saldo = Decimal('0.00')
        if recibos_caja.estado == 3:
            ingreso = recibos_caja.monto_pagado
        # moneda = recibos_caja.moneda
        url = '#'
        documentos = []

        fila = []
        fila.append(fecha)
        fila.append(concepto)
        fila.append(estado)
        fila.append(ingreso)
        fila.append(egreso)
        fila.append(saldo)
        fila.append(url)
        fila.append(documentos)
        movimientos.append(fila)

    #Caja Chica Salida
    for caja_chica_salida in applications.caja_chica.models.CajaChicaSalida.objects.filter(caja_chica=caja_chica.id):

        fecha = caja_chica_salida.fecha
        concepto = caja_chica_salida.concepto
        estado = 'USADO'
        ingreso = Decimal('0.00')
        egreso = caja_chica_salida.monto
        saldo = Decimal('0.00')
        url = '#'
        documentos = []
        
        fila = []
        fila.append(fecha)
        fila.append(concepto)
        fila.append(estado)
        fila.append(ingreso)
        fila.append(egreso)
        fila.append(saldo)
        fila.append(url)
        fila.append(documentos)
        movimientos.append(fila)

    movimientos.sort(key = lambda i: i[3], reverse=True) #Egreso
    try:
        movimientos.sort(key = lambda i: i[0]) #Fecha
    except:
        fila = []
        fila.append('')
        fila.append('ERROR. CONTACTAR A SOPORTE')
        fila.append('')
        fila.append(Decimal('0.00'))
        fila.append(Decimal('0.00'))
        fila.append(Decimal('0.00'))
        fila.append('#')
        movimientos.append(fila)

    return movimientos


def cheque_monto_usado_post_save(*args, **kwargs):
    obj = kwargs['instance']
    cheque = obj.cheque
    if cheque:
        cheque_monto_usado(cheque)

def cheque_monto_usado(cheque):
    recibos_boleta_pago = applications.contabilidad.models.ReciboBoletaPago.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
    recibos_servicio = applications.contabilidad.models.ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
    recibos_caja_chica = applications.caja_chica.models.ReciboCajaChica.objects.filter(cheque = cheque)
    requerimientos = applications.caja_chica.models.Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
    vuelto_extra = applications.contabilidad.models.ChequeVueltoExtra.objects.filter(cheque = cheque)

    total_boleta_pago_pagado = Decimal('0.00')
    total_servicio_pagado = Decimal('0.00')
    total_caja_chica_pagado = Decimal('0.00')
    total_requerimiento_usado = Decimal('0.00')
    total_vuelto_extra = Decimal('0.00')

    if recibos_boleta_pago:
        total_boleta_pago_pagado = recibos_boleta_pago.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
    if recibos_servicio:
        total_servicio_pagado = recibos_servicio.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
    if recibos_caja_chica:
        total_caja_chica_pagado = recibos_caja_chica.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
    if requerimientos:
        total_requerimiento_usado = requerimientos.aggregate(models.Sum('monto_usado'))['monto_usado__sum']
    if vuelto_extra:
        total_vuelto_extra = vuelto_extra.aggregate(models.Sum('vuelto_extra'))['vuelto_extra__sum']
    
    cheque.monto_usado = total_boleta_pago_pagado + total_servicio_pagado + total_caja_chica_pagado + total_requerimiento_usado + total_vuelto_extra
    cheque.save()