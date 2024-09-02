# Description: Funciones para verificar

# Verificar que todas las confirmaciones de los productos se hayan despachado correctamente
from applications.funciones import send_slack_verificar
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from django.contrib.contenttypes.models import ContentType

def verificar_confirmacion_total():
    materiales = Material.objects.all()
    for material in materiales:
        verificar_confirmacion(material.id)

def verificar_confirmacion(id_producto):
    try:
        producto = Material.objects.get(id=id_producto)
        print(f"{producto}")
    except:
        return "Error"
    tipo_stock_confirmado = TipoStock.objects.get(codigo=17)
    movimientos_confirmacion = MovimientosAlmacen.objects.filter(
        id_registro_producto=id_producto,
        content_type_producto=ContentType.objects.get_for_model(Material),
        tipo_stock=tipo_stock_confirmado,
        signo_factor_multiplicador=1,
        )
    
    movimientos_relacion = {}

    for movimiento_confirmacion in movimientos_confirmacion:
        movimientos_relacion[movimiento_confirmacion.id] = {}
        movimientos_relacion[movimiento_confirmacion.id]['confirmacion'] = [movimiento_confirmacion.id, movimiento_confirmacion.cantidad, movimiento_confirmacion.fecha_documento]
        movimientos_relacion[movimiento_confirmacion.id]['suma'] = movimiento_confirmacion.cantidad * movimiento_confirmacion.signo_factor_multiplicador
        for movimiento_despacho in movimiento_confirmacion.MovimientosAlmacen_movimiento_anterior.all():
            if movimiento_despacho.tipo_stock.codigo == 3:
                movimientos_relacion[movimiento_confirmacion.id]['despacho'] = [movimiento_despacho.id, movimiento_despacho.cantidad, movimiento_despacho.fecha_documento]
                movimientos_relacion[movimiento_confirmacion.id]['suma'] += movimiento_despacho.cantidad * movimiento_despacho.signo_factor_multiplicador

    primero = True
    for movimiento, valor in movimientos_relacion.items():
        if movimientos_relacion[movimiento]['suma'] != 0:
            if primero: 
                send_slack_verificar(f"{producto}")
                primero = False
            print(f"{movimiento} {valor}")
            send_slack_verificar(f"{movimiento} {valor}")
    return False

# verificar_confirmacion(42)
