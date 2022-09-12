from decimal import Decimal
from applications.cotizacion.models import CotizacionObservacion
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoStock

def disponible(content_type, id_registro, id_sociedad):
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
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def vendible(content_type, id_registro, id_sociedad):
    return disponible(content_type, id_registro, id_sociedad) - reservado(content_type, id_registro, id_sociedad) - confirmado(content_type, id_registro, id_sociedad)

def reservado(content_type, id_registro, id_sociedad):
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

def confirmado(content_type, id_registro, id_sociedad):
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

def calidad(content_type, id_registro, id_sociedad):
    bloqueo_sin_serie = TipoStock.objects.get(id=4)
    bloqueo_sin_qa = TipoStock.objects.get(id=5)
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                    ).filter(
                        Q(tipo_stock=bloqueo_sin_serie) | Q(tipo_stock=bloqueo_sin_qa)
                    )
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def stock(content_type, id_registro, id_sociedad):
    return vendible(content_type, id_registro, id_sociedad) + calidad(content_type, id_registro, id_sociedad)

def observacion(cotizacion, sociedad):
    busqueda = CotizacionObservacion.objects.get(
        cotizacion_venta = cotizacion,
        sociedad = sociedad,
    )
    return busqueda.observacion
