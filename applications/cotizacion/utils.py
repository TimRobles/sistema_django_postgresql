from applications.funciones import obtener_totales

def actualizar_cotizacion(cotizacion_venta):
    print('actualizar_cotizacion')
    try:
        respuesta = obtener_totales(cotizacion_venta)
        if cotizacion_venta.total != respuesta['total']:
            cotizacion_venta.total = respuesta['total']
            cotizacion_venta.save()
    except Exception as e:
        print('Error actualizar_cotizacion: ', e)
        return False

