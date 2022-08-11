from django.db import models

class MovimientoAlmacenManager(models.Manager):
    def ver_movimientos(self, content_type, id_registro):
        consulta = self.filter(
            content_type_producto = content_type,
            id_registro_producto = id_registro,
        )
        total = 0
        for dato in consulta:
            total += dato.cantidad * dato.signo_factor_multiplicador
        return consulta, total

    def ver_stock(self, content_type, id_registro, tipo_stock):
        lista_almacenes = []
        filas = {}
        lista_estados = list(tipo_stock)
        stocks = {}
        
        consulta = self.filter(
            content_type_producto = content_type,
            id_registro_producto = id_registro,
        )
        for dato in consulta:
            estado = dato.tipo_movimiento.tipo_stock
            index = lista_estados.index(estado) + 1
            if not (dato.sociedad, dato.almacen) in lista_almacenes:
                lista_almacenes.append((dato.sociedad, dato.almacen))
                totales = ['Totales',] + [0,]*len(lista_estados) + [0,]
                filas[(dato.sociedad, dato.almacen)] = [[dato.almacen,] + [0,]*len(lista_estados) + [0,], totales]
            filas[(dato.sociedad, dato.almacen)][0][index] = filas[(dato.sociedad, dato.almacen)][0][index] + dato.cantidad * dato.signo_factor_multiplicador
            filas[(dato.sociedad, dato.almacen)][0][-1] = filas[(dato.sociedad, dato.almacen)][0][-1] + dato.cantidad * dato.signo_factor_multiplicador

            filas[(dato.sociedad, dato.almacen)][1][index] = filas[(dato.sociedad, dato.almacen)][1][index] + dato.cantidad * dato.signo_factor_multiplicador
            filas[(dato.sociedad, dato.almacen)][1][-1] = filas[(dato.sociedad, dato.almacen)][1][-1] + dato.cantidad * dato.signo_factor_multiplicador

        for tupla, fila in filas.items():
            if not tupla[0] in stocks:
                stocks[tupla[0]] = [[], fila[1]]
            stocks[tupla[0]][0].append(fila[0])

        return stocks, tipo_stock
