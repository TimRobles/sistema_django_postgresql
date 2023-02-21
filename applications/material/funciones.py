from decimal import Decimal
from applications.cotizacion.models import CotizacionObservacion
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoStock
from django.db import models

from applications.nota_ingreso.models import NotaIngresoDetalle
from applications.sede.models import Sede

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

def disponible_sede(content_type, id_registro, id_sociedad, id_sede):
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
        sede = Sede.objects.get(id=id_sede)
        almacenes = []
        for almacen in sede.Almacen_sede.filter(estado_alta_baja=1):
            almacenes.append(almacen.id)
        movimientos = movimientos.filter(almacen__id__in=almacenes)
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def ver_tipo_stock(content_type, id_registro, id_sociedad, id_almacen, id_tipo_stock):
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                        tipo_stock__id = id_tipo_stock,
                        almacen__id = id_almacen,
                    )
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def sede_tipo_stock(content_type, id_registro, id_sociedad, id_sede, id_tipo_stock):
    total = Decimal('0.00')
    try:
        movimientos = MovimientosAlmacen.objects.filter(
                        content_type_producto = content_type,
                        id_registro_producto = id_registro,
                        sociedad__id = id_sociedad,
                        tipo_stock__id = id_tipo_stock,
                    )
        sede = Sede.objects.get(id=id_sede)
        almacenes = []
        for almacen in sede.Almacen_sede.filter(estado_alta_baja=1):
            almacenes.append(almacen.id)
        movimientos = movimientos.filter(almacen__id__in=almacenes)
        for movimiento in movimientos:
            total += movimiento.cantidad * movimiento.signo_factor_multiplicador
    except:
        pass

    return total

def vendible(content_type, id_registro, id_sociedad, id_almacen=None):
    return disponible(content_type, id_registro, id_sociedad, id_almacen) - reservado(content_type, id_registro, id_sociedad) - confirmado(content_type, id_registro, id_sociedad) - prestado(content_type, id_registro, id_sociedad)

def vendible_sede(content_type, id_registro, id_sociedad, id_sede):
    return disponible_sede(content_type, id_registro, id_sociedad, id_sede) - reservado(content_type, id_registro, id_sociedad) - confirmado(content_type, id_registro, id_sociedad) - prestado(content_type, id_registro, id_sociedad)

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

def prestado(content_type, id_registro, id_sociedad): #No tiene almacén
    confirmado = TipoStock.objects.get(codigo=22)
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

def calidad_sede(content_type, id_registro, id_sociedad, id_sede):
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
        sede = Sede.objects.get(id=id_sede)
        almacenes = []
        for almacen in sede.Almacen_sede.filter(estado_alta_baja=1):
            almacenes.append(almacen.id)
        movimientos = movimientos.filter(almacen__id__in=almacenes)
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

def stock_vendible(content_type, id_registro, id_sociedad, id_almacen=None):
    return vendible(content_type, id_registro, id_sociedad, id_almacen)

def stock_sede(content_type, id_registro, id_sociedad, id_sede):
    return vendible_sede(content_type, id_registro, id_sociedad, id_sede) + calidad_sede(content_type, id_registro, id_sociedad, id_sede)

def stock_sede_tipo_stock(content_type, id_registro, id_sociedad, id_sede, id_tipo_stock):
    return sede_tipo_stock(content_type, id_registro, id_sociedad, id_sede, id_tipo_stock)

def stock_disponible(content_type, id_registro, id_sociedad, id_almacen=None):
    return disponible(content_type, id_registro, id_sociedad, id_almacen)

def stock_sede_disponible(content_type, id_registro, id_sociedad, id_sede):
    return disponible_sede(content_type, id_registro, id_sociedad, id_sede)

def stock_tipo_stock(content_type, id_registro, id_sociedad, id_almacen, id_tipo_stock):
    return ver_tipo_stock(content_type, id_registro, id_sociedad, id_almacen, id_tipo_stock)

def en_camino(content_type, id_registro, id_sociedad):
    return transito(content_type, id_registro, id_sociedad) - confirmado_anticipo(content_type, id_registro, id_sociedad)

def observacion(cotizacion, sociedad):
    busqueda = CotizacionObservacion.objects.get(
        cotizacion_venta = cotizacion,
        sociedad = sociedad,
    )
    return busqueda.observacion

def NotaIngresoDetalle_comprobante_compra_detalle(obj):
    busqueda = NotaIngresoDetalle.objects.filter(
        content_type = obj.content_type,
        id_registro = obj.id_registro,
        nota_ingreso__estado=2
    ).aggregate(models.Sum('cantidad_conteo'))['cantidad_conteo__sum']
    return busqueda
