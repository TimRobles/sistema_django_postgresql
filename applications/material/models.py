from applications.variables import ESTADOS
from django.db import models
from django.conf import settings

from applications.datos_globales.models import Unidad,ProductoSunat
from applications.proveedores.models import Proveedor

class Clase(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    imagen = models.ImageField('Imagen', upload_to='img/material/clase/', default='img/material/clase/default_image.png', height_field=None, width_field=None, max_length=None)
    descripcion = models.TextField('Descripción')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Clase_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Clase_updated_by', editable=False)

    class Meta:

        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Componente(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Componente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Componente_updated_by', editable=False)

    class Meta:

        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Atributo(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Atributo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Atributo_updated_by', editable=False)

    class Meta:

        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Familia(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    atributos = models.ManyToManyField(Atributo, blank=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Familia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Familia_updated_by', editable=False)

    class Meta:

        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class SubFamilia(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    familia = models.ForeignKey(Familia, on_delete=models.PROTECT)
    componentes = models.ManyToManyField(Componente, blank=True)
    unidad = models.ManyToManyField(Unidad)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamilia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamilia_updated_by', editable=False)

    class Meta:

        verbose_name = 'SubFamilia'
        verbose_name_plural = 'SubFamilias'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Modelo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Modelo_updated_by', editable=False)

    class Meta:

        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    modelos = models.ManyToManyField(Modelo)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Marca_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Marca_updated_by', editable=False)

    class Meta:

        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Material(models.Model):
    descripcion_venta = models.CharField('Descripción Venta', max_length=500)
    descripcion_corta = models.CharField('Descripción Corta', max_length=150)
    unidad_base = models.ForeignKey(Unidad, on_delete=models.PROTECT, related_name='Material_unidad_base')
    peso_unidad_base = models.DecimalField('Peso Unidad Base', max_digits=6, decimal_places=2)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='Material_marca', blank=True, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='Material_modelo', blank=True, null=True)
    subfamilia = models.ForeignKey(SubFamilia, on_delete=models.PROTECT, related_name='Material_subfamilia')
    clase = models.ForeignKey(Clase, on_delete=models.PROTECT, related_name='Material_clase',blank=True,null=True)
    producto_sunat = models.ForeignKey(ProductoSunat, on_delete=models.PROTECT, related_name='Material_producto_sunat', blank=True,null=True)
    control_serie = models.BooleanField('Control Serie',default=False)
    control_lote = models.BooleanField('Control Lote',default=False)
    control_calidad = models.BooleanField('Control Calidad',default=False)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)
    mostrar = models.BooleanField('Mostrar',default=False)
    traduccion = models.CharField('Traducción', max_length=255, blank=True)
    partida =  models.CharField('Partida', max_length=30,blank=True)
    uso_funcion =  models.CharField('Uso función', max_length=500,blank=True)
    compuesto_por =  models.CharField('Compuesto por', max_length=255,blank=True)
    es_componente = models.BooleanField('Es componente',default=False)
    atributo = models.ManyToManyField(Atributo,verbose_name='Atributo',related_name='Material_atributo',blank=True)
    componente = models.ManyToManyField(Componente,verbose_name='Componente',related_name='Material_componente', blank=True, through='material.RelacionMaterialComponente')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Material_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Material_updated_by', editable=False)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = [
        'estado_alta_baja',
        'descripcion_venta',
        ]

    def __str__(self):
        return self.descripcion_venta +" - "+ self.descripcion_corta

class RelacionMaterialComponente(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    componentematerial = models.ForeignKey(Componente,verbose_name='Componente material', on_delete=models.CASCADE)
    cantidad = models.IntegerField('Cantidad')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RelacionMaterialComponente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RelacionMaterialComponente_updated_by', editable=False)


    class Meta:
        verbose_name = 'Relacion Material Componente'
        verbose_name_plural = 'Relacion Material Componentes'

    def __str__(self):
        return self.material.__str__() +" - "+ self.componentematerial.__str__()

class Especificacion(models.Model):
    orden = models.IntegerField('Orden')
    atributomaterial = models.ForeignKey(Atributo,verbose_name='Atributo material', on_delete=models.CASCADE)
    valor = models.CharField('Valor', max_length=100)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Especificacion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Especificacion_updated_by', editable=False)

    class Meta:
        verbose_name = 'Especificacion'
        verbose_name_plural = 'Especificaciones'
        ordering = ['orden',]

    def __str__(self):
        return str(self.orden) + " - " +self.atributomaterial.__str__() + " - " + str(self.valor)

class Datasheet(models.Model):
    descripcion = models.CharField('Descripción', max_length=200)
    archivo = models.FileField('Archivo',upload_to = 'file/materiales/archivo_datasheet/', max_length=100, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Datasheet_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Datasheet_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datasheet'
        verbose_name_plural = 'Datasheets'

    def __str__(self):
        return self.descripcion.__str__() + " - " + self.material.__str__()

class ImagenMaterial(models.Model):
    descripcion = models.CharField('Descripción imagen material', max_length=200)
    imagen = models.ImageField('Imagen material', upload_to='img/material/imagen/', height_field=None, width_field=None, max_length=None)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImagenMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImagenMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Imagen Material'
        verbose_name_plural = 'Imagen Materiales'
        ordering = ['estado_alta_baja']

    def __str__(self):
        return self.descripcion.__str__() + " - " + self.material.__str__()

class VideoMaterial(models.Model):
    descripcion = models.CharField('Descripción video material', max_length=200)
    url = models.URLField('URL video material')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='VideoMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='VideoMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Video Material'
        verbose_name_plural = 'Video Materiales'
        ordering = ['estado_alta_baja']


    def __str__(self):
        return self.descripcion.__str__()+ " - " + self.material.__str__()

class ProveedorMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=100)
    brand = models.CharField('Brand', max_length=100)
    description = models.CharField('Description', max_length=255)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ProveedorMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ProveedorMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Proveedor Material'
        verbose_name_plural = 'Proveedor Materiales'
        ordering = ['estado_alta_baja',]


    def __str__(self):
        return str(self.proveedor) + " - " + self.material.__str__()

class EquivalenciaUnidad(models.Model):
    cantidad_base = models.DecimalField('Cantidad Base', max_digits=6, decimal_places=2)
    nueva_unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT, related_name='EquivalenciaUnidad_nueva_unidad')
    cantidad_nueva_unidad = models.DecimalField('Cantidad Nueva', max_digits=6, decimal_places=2)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EquivalenciaUnidad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EquivalenciaUnidad_updated_by', editable=False)

    class Meta:
        verbose_name = 'Equivalencia Unidad'
        verbose_name_plural = 'Equivalencia Unidades'
        ordering = ['estado_alta_baja',]


    def __str__(self):
        return str(self.cantidad_base) + " : " + str(self.cantidad_nueva_unidad) + " " + str(self.nueva_unidad)
