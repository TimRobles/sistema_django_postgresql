from django.db import models

class SerieManager(models.Manager):
    def buscar_series(self, movimientos):
        consulta = self.filter(
            serie_movimiento_almacen__in = movimientos,
        )
        return consulta


class NotaSalidaManager(models.Manager):
    def confirmacion_venta(self, id_nota_salida):
        nota_salida = self.get(id=id_nota_salida)
        consulta = nota_salida.NotaSalidaDocumento_nota_salida.all()
        for documento in consulta:
            if documento.confirmacion_venta:
                return documento.confirmacion_venta
        return None

    def solicitud_prestamo_materiales(self, id_nota_salida):
        print("solicitud_prestamo_materiales")
        nota_salida = self.get(id=id_nota_salida)
        print(nota_salida)
        consulta = nota_salida.NotaSalidaDocumento_nota_salida.all()
        print(consulta)
        for documento in consulta:
            if documento.solicitud_prestamo_materiales:
                print(documento.solicitud_prestamo_materiales)
                return documento.solicitud_prestamo_materiales
        return None

    def devolucion_muestra(self, id_nota_salida):
        nota_salida = self.get(id=id_nota_salida)
        consulta = nota_salida.NotaSalidaDocumento_nota_salida.all()
        for documento in consulta:
            if documento.devolucion_muestra:
                return documento.devolucion_muestra
        return None