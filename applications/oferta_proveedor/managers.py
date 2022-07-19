from django.db import models

class OfertaProveedorDetalleManager(models.Manager):
    def ver_detalle(self, oferta_proveedor):
        consulta = self.filter(oferta_proveedor = oferta_proveedor)
        for dato in consulta:
            dato.material = dato.proveedor_material.content_type.get_object_for_this_type(id=dato.proveedor_material.id_registro)
        return consulta
