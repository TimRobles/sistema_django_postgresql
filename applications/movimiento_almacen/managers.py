from decimal import Decimal
from django.db import models

def retornar_fecha(movimiento):
    fecha = movimiento.content_type_documento_proceso.model_class().objects.get(id=movimiento.id_registro_documento_proceso).fecha
    return fecha

class MovimientoAlmacenManager(models.Manager):
    def ver_movimientos(self, content_type, id_registro):
        movimientos_fuera = [9, 12, 14, 15, 16, 17, 19]
        consulta = self.filter(
            content_type_producto = content_type,
            id_registro_producto = id_registro,
        )
        total = 0
        lista = []
        for dato in consulta:
            lista.append(dato)
            if not dato.tipo_stock.codigo in movimientos_fuera:
                total += dato.cantidad * dato.signo_factor_multiplicador

        lista.sort(key=retornar_fecha)
        
        return lista, total

    def ver_stock(self, content_type, id_registro, tipo_stock):
        movimientos_fuera = [9, 12, 14, 15, 16, 17, 19]
        lista_estados = list(tipo_stock)
        stocks = {}
        totales = {}
        
        consulta = self.filter(
            content_type_producto = content_type,
            id_registro_producto = id_registro,
        )

        for dato in consulta:
            estado = dato.tipo_stock
            index = lista_estados.index(estado) + 1
            cantidad = dato.cantidad * dato.signo_factor_multiplicador

            if not dato.sociedad in stocks:
                totales = ['Totales',] + [Decimal('0.00'),]*len(lista_estados) + [Decimal('0.00'),]
                stocks[dato.sociedad]= [{}, totales]
            
            if not dato.almacen in stocks[dato.sociedad][0]:
                almacenes = [dato.almacen,] + [Decimal('0.00'),]*len(lista_estados) + [Decimal('0.00'),]
                stocks[dato.sociedad][0][dato.almacen] = almacenes

            stocks[dato.sociedad][0][dato.almacen][index] = stocks[dato.sociedad][0][dato.almacen][index] + cantidad
            if not dato.tipo_stock.codigo in movimientos_fuera:
                stocks[dato.sociedad][0][dato.almacen][-1] = stocks[dato.sociedad][0][dato.almacen][-1] + cantidad

            stocks[dato.sociedad][1][index] = stocks[dato.sociedad][1][index] + cantidad
            if not dato.tipo_stock.codigo in movimientos_fuera:
                stocks[dato.sociedad][1][-1] = stocks[dato.sociedad][1][-1] + cantidad

        return stocks, tipo_stock
