from django.db import models

from ..material.models import ProveedorMaterial

class OrdenCompraDetalleManager(models.Manager):
    def ver_detalle(self, orden_compra):
        consulta = self.filter(orden_compra = orden_compra)
        proveedor = orden_compra.proveedor
        for dato in consulta:
            dato.material = dato.content_type.get_object_for_this_type(id = dato.id_registro)
            dato.proveedor_material = ProveedorMaterial.objects.get(
                content_type = dato.content_type,
                id_registro = dato.id_registro,
                proveedor = proveedor,
                estado_alta_baja = 1,
            )
        return consulta
