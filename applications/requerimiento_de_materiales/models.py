from django.conf import settings
from django.db import models
from applications.importaciones import registro_guardar_user
from applications.proveedores.models import Proveedor, InterlocutorProveedor,ProveedorInterlocutor
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import pre_save, post_save

class ListaRequerimientoMaterial(models.Model):
    titulo = models.CharField('Titulo', max_length=150,null=True, blank=True)

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
    item = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return str(self.id)


class RequerimientoMaterialProveedor(models.Model):
    ESTADOS_REQUERIMIENTO = (
        (1, 'BORRADOR'),
        (2, 'PENDIENTE'),
        (3, 'ENVIADO'),
    )

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    titulo = models.CharField('Titulo', max_length=150,null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='ProveedorMaterial',null=True, blank=True)
    interlocutor_proveedor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT, related_name='InterlocutorProveedorMaterial',null=True, blank=True)
    lista_requerimiento = models.ForeignKey(ListaRequerimientoMaterial, on_delete=models.CASCADE)
    requerimiento_material_anterior = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)
    version = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_REQUERIMIENTO, default=1)

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
    item = models.IntegerField(null=True, blank=True)
    id_requerimiento_material_detalle =  models.ForeignKey(ListaRequerimientoMaterialDetalle, on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, null=True, blank=True)
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
        return str(self.cantidad)




class RequerimientoMaterial(models.Model):
    ESTADOS_REQUERIMIENTO = (
        (1, 'BORRADOR'),
        (2, 'PENDIENTE'),
        (3, 'ENVIADO'),
    )

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    titulo = models.CharField('Titulo', max_length=150,null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='Proveedor',null=True, blank=True)
    interlocutor_proveedor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT, related_name='InterlocutorProveedor',null=True, blank=True)
    requerimiento_material_anterior = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    version = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_REQUERIMIENTO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Requerimiento de Material'
        verbose_name_plural = 'Requerimiento de Materiales'
        ordering = [
            '-fecha',
        ]
    def __str__(self):
        return str(self.titulo)

class RequerimientoMaterialDetalle(models.Model):
    item = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, null=True, blank=True)
    requerimiento_material = models.ForeignKey(RequerimientoMaterial, on_delete=models.CASCADE, related_name='RequerimientoMaterialDetalle_requerimiento_material')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Requerimiento de Material Detalle'
        verbose_name_plural = 'Requerimiento de Materiales Detalle'
        ordering = [
            'item',
        ]

    def __str__(self):
        return str(self.cantidad)


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

pre_save.connect(requerimiento_material_proveedor_pre_save, sender=RequerimientoMaterialProveedor)
post_save.connect(requerimiento_material_proveedor_post_save, sender=RequerimientoMaterialProveedor)
