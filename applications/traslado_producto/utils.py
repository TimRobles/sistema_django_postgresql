from decimal import Decimal


def validar_recepcion_traslado(envio_traslado_producto):
    lista_envio = {}
    for detalle in envio_traslado_producto.detalle:
        if detalle.producto not in lista_envio:
            lista_envio[detalle.producto] = [Decimal(0), Decimal(0)]
        lista_envio[detalle.producto][0] += detalle.cantidad_envio
    for detalle in envio_traslado_producto.detalle_recepcion:
        lista_envio[detalle.producto][1] += detalle.cantidad_recepcion

    for k, v in lista_envio.items():
        if v[0] != v[1]:
            return False
    return True
