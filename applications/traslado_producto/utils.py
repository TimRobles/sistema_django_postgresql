from decimal import Decimal


def validar_recepcion_traslado(envio_traslado_producto):
    lista_envio = {}
    for detalle in envio_traslado_producto.detalle:
        lista_envio[detalle.producto] = [detalle.cantidad_envio, Decimal(0)]
    for detalle in envio_traslado_producto.detalle_recepcion:
        lista_envio[detalle.producto][1] += detalle.cantidad_recepcion

    for k, v in lista_envio.items():
        if v[0] != v[1]:
            return False
    return True
    