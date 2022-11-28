from django.conf import settings
from django.db import models
from applications.importaciones import registro_guardar_user
from applications.proveedores.models import Proveedor, InterlocutorProveedor,ProveedorInterlocutor
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

class ListaRequerimientoMaterial(models.Model):
    titulo = models.CharField('Titulo', max_length=150,blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ListaRequerimientoMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ListaRequerimientoMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Lista de Requerimiento Material'
        verbose_name_plural = 'Listas de Requerimiento Material'
        ordering = [
            '-created_at',
        ]

    def __str__(self):
        return str(self.titulo)

class ListaRequerimientoMaterialDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    lista_requerimiento_material = models.ForeignKey(ListaRequerimientoMaterial, on_delete=models.CASCADE, related_name='ListaRequerimientoMaterialDetalle_requerimiento_material')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ListaRequerimientoMaterialDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ListaRequerimientoMaterialDetalle_updated_by', editable=False)


    class Meta:
        verbose_name = 'Lista de Requerimiento Material Detalle'
        verbose_name_plural = 'Listas de Requerimiento Material Detalle'
        ordering = [
            'item',
        ]
    
    @property
    def descripcion_venta(self):
        try:
            return self.content_type.get_object_for_this_type(id=self.id_registro).descripcion_venta
        except:
            return "Sin Material"

    def __str__(self):
        return "%s. %s" % (self.item, self.descripcion_venta)


class RequerimientoMaterialProveedor(models.Model):
    ESTADOS_REQUERIMIENTO = (
        (1, 'BORRADOR'),
        (2, 'PENDIENTE DE ENVÍO'),
        (3, 'ENVIADO'),
        (4, 'ANULADO'),
    )

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    titulo = models.CharField('Titulo', max_length=150,blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='ProveedorMaterial',blank=True, null=True)
    interlocutor_proveedor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT, related_name='InterlocutorProveedorMaterial',blank=True, null=True)
    lista_requerimiento = models.ForeignKey(ListaRequerimientoMaterial, on_delete=models.PROTECT)
    requerimiento_material_anterior = models.ForeignKey('self', on_delete=models.PROTECT,blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_REQUERIMIENTO, default=1)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialProveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialProveedor_updated_by', editable=False)

    class Meta:
        verbose_name = 'Requerimiento Material Proveedor'
        verbose_name_plural = 'Requerimientos Material Proveedor'
        ordering = [
            '-fecha',
        ]

    def __str__(self):
        return str(self.titulo)

class RequerimientoMaterialProveedorDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    id_requerimiento_material_detalle =  models.ForeignKey(ListaRequerimientoMaterialDetalle, on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, blank=True, null=True)
    requerimiento_material = models.ForeignKey(RequerimientoMaterialProveedor, on_delete=models.CASCADE, related_name='RequerimientoMaterialProveedorDetalle_requerimiento_material')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialProveedorDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialProveedorDetalle_updated_by', editable=False)


    class Meta:
        verbose_name = 'Requerimiento Material Proveedor Detalle'
        verbose_name_plural = 'Requerimientos Material Proveedor Detalle'
        ordering = [
            'item',
        ]

    def __str__(self):
        return "%s. %s" % (self.item, self.id_requerimiento_material_detalle.descripcion_venta)


def requerimiento_material_proveedor_post_save(*args, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance']
        listadetalle = ListaRequerimientoMaterialDetalle.objects.filter(lista_requerimiento_material=obj.lista_requerimiento)
        for detalle in listadetalle:
            obj_detalle = RequerimientoMaterialProveedorDetalle.objects.create(
                item=detalle.item,
                id_requerimiento_material_detalle=detalle,
                cantidad=detalle.cantidad,
                requerimiento_material=obj,
            )
            registro_guardar_user(obj_detalle, obj.created_by)
            obj_detalle.save()

def requerimiento_material_proveedor_pre_save(*args, **kwargs):
    print("Pre save de requerimiento material proveedor")
    print(kwargs)

def lista_requerimiento_material_detalle_pre_delete(sender, instance, *args, **kwargs):
    print("************PRE*****************")

def lista_requerimiento_material_detalle_post_delete(sender, instance, *args, **kwargs):
    materiales = ListaRequerimientoMaterialDetalle.objects.filter(lista_requerimiento_material=instance.lista_requerimiento_material)
    contador = 1
    for material in materiales:
        material.item = contador
        material.save()
        contador += 1

pre_save.connect(requerimiento_material_proveedor_pre_save, sender=RequerimientoMaterialProveedor)
post_save.connect(requerimiento_material_proveedor_post_save, sender=RequerimientoMaterialProveedor)

pre_delete.connect(lista_requerimiento_material_detalle_pre_delete, sender=ListaRequerimientoMaterialDetalle)
post_delete.connect(lista_requerimiento_material_detalle_post_delete, sender=ListaRequerimientoMaterialDetalle)
