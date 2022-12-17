from decimal import Decimal
from django.db import models

def retornar_signo(movimiento):
    signo_factor_multiplicador = movimiento.id
    return signo_factor_multiplicador

def retornar_fecha(movimiento):
    fecha = movimiento.content_type_documento_proceso.model_class().objects.get(id=movimiento.id_registro_documento_proceso).fecha
    return fecha

class MovimientoAlmacenManager(models.Manager):
    def ver_movimientos(self, content_type, id_registro):
        movimientos_fuera = [9, 12, 14, 15, 16, 17, 19, 22]
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

        lista.sort(key=retornar_signo)
        lista.sort(key=retornar_fecha)
        
        return lista, total

    def ver_stock(self, content_type, id_registro, tipo_stock):
        movimientos_fuera = [9, 12, 14, 15, 16, 17, 19, 22]
        lista_estados = list(tipo_stock)
        stocks = {}
        totales = {}
        
        consulta = self.filter(
            content_type_producto = content_type,
            id_registro_producto = id_registro,
        ).order_by('sociedad')

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

        columnas = {}
        for sociedad, stocks_sociedad in stocks.items():
            stocks_almacen = stocks_sociedad[0]
            totales = stocks_sociedad[1]
            for columna in range(len(totales)-2, 0, -1):
                if not totales[columna]:
                    if not columna in columnas: columnas[columna]=0
                    columnas[columna] = columnas[columna] + 1

        columnas = dict(sorted(columnas.items(), reverse=True))

        for sociedad, stocks_sociedad in stocks.items():
            stocks_almacen = stocks_sociedad[0]
            totales = stocks_sociedad[1]
            for columna, v in columnas.items():
                if v == len(stocks.items()):
                    totales.pop(columna)
                    estado = lista_estados[columna-1]
                    for almacen, stock in stocks_almacen.items():
                        stock.pop(columna)
                    if list(stocks.items())[-1][0] == sociedad:
                        tipo_stock = tipo_stock.exclude(id=lista_estados[columna-1].id)
                        lista_estados.pop(columna-1)


        return stocks, tipo_stock