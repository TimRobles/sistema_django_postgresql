from decimal import Decimal
from applications.cotizacion.models import CotizacionObservacion
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoStock
from django.db import models

def disponible(content_type, id_registro, id_sociedad, id_almacen=None):
    disponible = TipoStock.objects.get(codigo=3)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        tipo_stock = disponible,
                    )
        if id_almacen:
            movimientos = movimientos.filter(almacen__id=id_almacen)
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def vendible(content_type, id_registro, id_sociedad, id_almacen=None):
    return disponible(content_type, id_registro, id_sociedad, id_almacen) - reservado(content_type, id_registro, id_sociedad) - confirmado(content_type, id_registro, id_sociedad)

def reservado(content_type, id_registro, id_sociedad): #No tiene almacén
    reservado = TipoStock.objects.get(codigo=16)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        tipo_stock = reservado,
                    )
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def confirmado(content_type, id_registro, id_sociedad): #No tiene almacén
    confirmado = TipoStock.objects.get(codigo=17)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        tipo_stock = confirmado,
                    )
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def confirmado_anticipo(content_type, id_registro, id_sociedad): #No tiene almacén
    confirmado = TipoStock.objects.get(codigo=21)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        tipo_stock = confirmado,
                    )
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def calidad(content_type, id_registro, id_sociedad, id_almacen=None):
    bloqueo_sin_serie = TipoStock.objects.get(id=4)
    bloqueo_sin_qa = TipoStock.objects.get(id=5)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        models.Q(tipo_stock=bloqueo_sin_serie) | models.Q(tipo_stock=bloqueo_sin_qa)
                    )
        if id_almacen:
            movimientos = movimientos.filter(almacen__id=id_almacen)
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def transito(content_type, id_registro, id_sociedad): #No tiene almacén
    confirmado = TipoStock.objects.get(codigo=1)
    recibido = TipoStock.objects.get(codigo=2)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        tipo_stock__in=[confirmado, recibido],
                    )
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def stock(content_type, id_registro, id_sociedad, id_almacen=None):
    return vendible(content_type, id_registro, id_sociedad, id_almacen) + calidad(content_type, id_registro, id_sociedad, id_almacen)

def en_camino(content_type, id_registro, id_sociedad):
    return transito(content_type, id_registro, id_sociedad) - confirmado_anticipo(content_type, id_registro, id_sociedad)

def observacion(cotizacion, sociedad):
    busqueda = CotizacionObservacion.objects.get(
        cotizacion_venta = cotizacion,
        sociedad = sociedad,
    )
    return busqueda.observacion
