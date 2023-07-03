from datetime import date
from decimal import Decimal
import requests
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoStock
from applications import orden_compra
from applications.variables import ESTADOS
from django.db import models
from django.conf import settings
from django.db.models import Q
from applications.datos_globales.models import Unidad,ProductoSunat
from applications.proveedores.models import Proveedor
from django.contrib.contenttypes.models import ContentType
from applications.variables import URL_MULTIPLAY
from applications.material.models import Idioma
from applications.sociedad.models import Sociedad
from applications.sede.models import Sede
from applications.almacenes.models import Almacen

class ClaseMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    imagen = models.ImageField('Imagen', upload_to='img/merchandising/clase/', default='img/merchandising/clase/default_image.png', height_field=None, width_field=None, max_length=None)
    descripcion = models.TextField('Descripción')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ClaseMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ClaseMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'Clase Merchandising'
        verbose_name_plural = 'Clases Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class ComponenteMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComponenteMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComponenteMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'Componente Merchandising'
        verbose_name_plural = 'Componentes Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class AtributoMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='AtributoMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='AtributoMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'Atributo Merchandising'
        verbose_name_plural = 'Atributos Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class FamiliaMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    atributos = models.ManyToManyField(AtributoMerchandising, blank=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FamiliaMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FamiliaMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'Familia Merchandising'
        verbose_name_plural = 'Familias Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class SubFamiliaMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    familia = models.ForeignKey(FamiliaMerchandising, on_delete=models.PROTECT)
    componentes = models.ManyToManyField(ComponenteMerchandising, blank=True)
    unidad = models.ManyToManyField(Unidad)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamiliaMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamiliaMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'SubFamilia Merchandising'
        verbose_name_plural = 'SubFamilias Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class ModeloMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=41)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ModeloMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ModeloMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'Modelo Merchandising'
        verbose_name_plural = 'Modelos Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class MarcaMerchandising(models.Model):
    nombre = models.CharField('Nombre', max_length=42)
    modelos = models.ManyToManyField(ModeloMerchandising)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MarcaMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MarcaMerchandising_updated_by', editable=False)

    class Meta:

        verbose_name = 'Marca Merchandising'
        verbose_name_plural = 'Marcas Merchandising'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Merchandising(models.Model):
    descripcion_venta = models.CharField('Descripción Venta', max_length=150)
    descripcion_corta = models.CharField('Descripción Corta', max_length=55)
    unidad_base = models.ForeignKey(Unidad, on_delete=models.PROTECT, related_name='Merchandising_unidad_base')
    peso_unidad_base = models.DecimalField('Peso Unidad Base', max_digits=6, decimal_places=2)
    marca = models.ForeignKey(MarcaMerchandising, on_delete=models.PROTECT, related_name='Merchandising_marca', blank=True, null=True)
    modelo = models.ForeignKey(ModeloMerchandising, on_delete=models.PROTECT, related_name='Merchandising_modelo', blank=True, null=True)
    subfamilia = models.ForeignKey(SubFamiliaMerchandising, on_delete=models.PROTECT, related_name='Merchandising_subfamilia')
    clase = models.ForeignKey(ClaseMerchandising, on_delete=models.PROTECT, related_name='Merchandising_clase', blank=True, null=True)
    producto_sunat = models.ForeignKey(ProductoSunat, on_delete=models.PROTECT, related_name='Merchandising_producto_sunat', blank=True,null=True)
    control_serie = models.BooleanField('Control Serie', default=False)
    control_lote = models.BooleanField('Control Lote', default=False)
    control_calidad = models.BooleanField('Control Calidad', default=False)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)
    mostrar = models.BooleanField('Mostrar',default=False)
    traduccion = models.CharField('Traducción', max_length=255, blank=True, null=True)
    partida =  models.CharField('Partida', max_length=30, blank=True, null=True)
    uso_funcion =  models.CharField('Uso función', max_length=500, blank=True, null=True)
    compuesto_por =  models.CharField('Compuesto por', max_length=255, blank=True, null=True)
    es_componente = models.BooleanField('Es componente', default=False)
    atributo = models.ManyToManyField(AtributoMerchandising, verbose_name='Atributo', related_name='Merchandising_atributo')
    componente = models.ManyToManyField(ComponenteMerchandising, verbose_name='Componente', related_name='Merchandising_componente', through='merchandising.RelacionMerchandisingComponente')
    id_producto_temporal = models.IntegerField(blank=True, null=True)
    id_multiplay = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Merchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Merchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Merchandising'
        verbose_name_plural = 'Merchandising'
        ordering = [
            'estado_alta_baja',
            'descripcion_venta',
        ]
    
    @property
    def codigo_producto_sunat(self):
        if self.producto_sunat:
            return self.producto_sunat.codigo
        else:
            return ''

    @property
    def descripcion_documento(self):
        if self.marca and self.modelo:
            return "%s MARCA: %s MODELO: %s" % (self.descripcion_venta, self.marca.nombre, self.modelo.nombre)
        elif self.marca:
            return "%s MARCA: %s" % (self.descripcion_venta, self.marca.nombre)
        elif self.modelo:
            return "%s MARCA: %s" % (self.descripcion_venta, self.modelo.nombre)
        else:
            return "%s" % (self.descripcion_venta)

    @property
    def ultimo_precio(self):
        try:
            ordenes_detalle = orden_compra.models.OrdenCompraDetalle.objects.filter(
                        content_type = ContentType.objects.get_for_model(self),
                        id_registro = self.id,
                    )
            ultima_fecha = date(1900,1,1)
            ultimo_precio = Decimal('0.00')
            for orden_detalle in ordenes_detalle:
                if orden_detalle.orden_compra.fecha_orden >= ultima_fecha:
                    ultima_fecha = orden_detalle.orden_compra.fecha_orden
                    ultimo_precio = orden_detalle.precio_final_con_igv
            return ultimo_precio
        except:
            return ""

    @property
    def minimo_precio(self):
        try:
            ordenes_detalle = orden_compra.models.OrdenCompraDetalle.objects.filter(
                        content_type = ContentType.objects.get_for_model(self),
                        id_registro = self.id,
                    )
            minimo_precio = Decimal('1000000000000000.00')
            if ordenes_detalle:
                for orden_detalle in ordenes_detalle:
                    if orden_detalle.precio_final_con_igv <= minimo_precio:
                        minimo_precio = orden_detalle.precio_final_con_igv
            else:
                minimo_precio = Decimal('0.00')
            return minimo_precio
        except:
            return ""

    @property
    def disponible(self):
        disponible = TipoStock.objects.get(codigo=3)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            tipo_stock = disponible,
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def vendible(self):
        return self.disponible - self.reservado - self.confirmado - self.prestamo

    @property
    def reservado(self):
        reservado = TipoStock.objects.get(codigo=16)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            tipo_stock = reservado,
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def transito(self):
        transito = TipoStock.objects.get(codigo=1)
        recibido = TipoStock.objects.get(codigo=2)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            tipo_stock__in = [transito, recibido],
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def confirmado(self):
        confirmado = TipoStock.objects.get(codigo=17)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            tipo_stock = confirmado,
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def prestamo(self):
        prestamo = TipoStock.objects.get(codigo=22)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            tipo_stock = prestamo,
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def confirmado_anticipo(self):
        confirmado = TipoStock.objects.get(codigo=21)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            tipo_stock = confirmado,
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def calidad(self):
        bloqueo_sin_serie = TipoStock.objects.get(id=4)
        bloqueo_sin_qa = TipoStock.objects.get(id=5)
        total = Decimal('0.00')
        try:
            movimientos = MovimientosAlmacen.objects.filter(
                            content_type_producto = ContentType.objects.get_for_model(self),
                            id_registro_producto = self.id,
                        ).filter(
                            Q(tipo_stock=bloqueo_sin_serie) | Q(tipo_stock=bloqueo_sin_qa)
                        )
            for movimiento in movimientos:
                total += movimiento.cantidad * movimiento.signo_factor_multiplicador
        except:
            pass

        return total

    @property
    def stock(self):
        return self.vendible + self.calidad

    @property
    def en_camino(self):
        return self.transito - self.confirmado_anticipo

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def precio_oferta(self):
        try:
            print("*****************************")
            url = f'{URL_MULTIPLAY}producto/producto_api/{self.id_multiplay}/'
            print(url)
            r = requests.get(url)
            print(r)
            data = r.text
            print(data)
            print("*****************************")
            return Decimal(data)
        except:
            return None
            

    def __str__(self):
        return self.descripcion_venta

class RelacionMerchandisingComponente(models.Model):
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)
    componentemerchandising = models.ForeignKey(ComponenteMerchandising,verbose_name='Componente merchandising', on_delete=models.CASCADE)
    cantidad = models.IntegerField('Cantidad')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RelacionMerchandisingComponente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RelacionMerchandisingComponente_updated_by', editable=False)


    class Meta:
        verbose_name = 'Relacion Merchandising Componente'
        verbose_name_plural = 'Relacion Merchandising Componentes'

    def __str__(self):
        return self.merchandising.__str__() +" - "+ self.componentemerchandising.__str__()

class EspecificacionMerchandising(models.Model):
    orden = models.IntegerField('Orden')
    atributomerchandising = models.ForeignKey(AtributoMerchandising,verbose_name='Atributo Merchandising', on_delete=models.CASCADE)
    valor = models.CharField('Valor', max_length=100)
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EspecificacionMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EspecificacionMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Especificacion Merchandising'
        verbose_name_plural = 'Especificaciones Merchandising'
        ordering = ['orden',]

    def __str__(self):
        return str(self.orden) + " - " +self.atributomerchandising.__str__() + " - " + str(self.valor)

class DatasheetMerchandising(models.Model):
    descripcion = models.CharField('Descripción', max_length=200)
    archivo = models.FileField('Archivo',upload_to = 'file/merchandising/archivo_datasheet/', max_length=100, blank=True, null=True)
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatasheetMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatasheetMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datasheet Merchandising'
        verbose_name_plural = 'Datasheets Merchandising'

    def __str__(self):
        return self.descripcion.__str__() + " - " + self.merchandising.__str__()

class ImagenMerchandising(models.Model):
    descripcion = models.CharField('Descripción imagen merchandising', max_length=200)
    imagen = models.ImageField('Imagen merchandising', upload_to='img/merchandising/imagen/', height_field=None, width_field=None, max_length=None)
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImagenMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImagenMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Imagen Merchandising'
        verbose_name_plural = 'Imagenes Merchandising'
        ordering = ['estado_alta_baja']

    def __str__(self):
        return self.descripcion.__str__() + " - " + self.merchandising.__str__()

class VideoMerchandising(models.Model):
    descripcion = models.CharField('Descripción video merchandising', max_length=200)
    url = models.URLField('URL video merchandising')
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='VideoMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='VideoMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Video Merchandising'
        verbose_name_plural = 'Videos Merchandising'
        ordering = ['estado_alta_baja']


    def __str__(self):
        return self.descripcion.__str__()+ " - " + self.merchandising.__str__()

class ProveedorMerchandising(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True) #Merchandising
    id_registro = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=100)
    brand = models.CharField('Brand', max_length=100)
    description = models.CharField('Description', max_length=255)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, null=True)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ProveedorMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ProveedorMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Proveedor Merchandising'
        verbose_name_plural = 'Proveedores Merchandising'
        ordering = ['estado_alta_baja',]

    @property
    def producto(self):
        try:
            return self.content_type.get_object_for_this_type(id = self.id_registro)
        except:
            return None

    def __str__(self):
        if self.producto:
            return str(self.producto)
        else:
            return "%s - %s - %s" % (self.name, self.brand, self.description)

class EquivalenciaUnidadMerchandising(models.Model):
    cantidad_base = models.DecimalField('Cantidad Base', max_digits=6, decimal_places=2)
    nueva_unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT, related_name='EquivalenciaUnidadMerchandising_nueva_unidad')
    cantidad_nueva_unidad = models.DecimalField('Cantidad Nueva', max_digits=6, decimal_places=2)
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EquivalenciaUnidadMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EquivalenciaUnidadMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Equivalencia Unidad Merchandising'
        verbose_name_plural = 'Equivalencia Unidades Merchandising'
        ordering = ['estado_alta_baja',]


    def __str__(self):
        return str(self.cantidad_base) + " : " + str(self.cantidad_nueva_unidad) + " " + str(self.nueva_unidad)

class IdiomaMerchandising(models.Model):
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    traduccion = models.CharField('Traducción', max_length=50)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='IdiomaMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='IdiomaMerchandising_updated_by', editable=False)

    class Meta:
        verbose_name = 'Idioma Merchandising'
        verbose_name_plural = 'Idiomas Merchandising'

    def __str__(self):
        return str(self.idioma)
    
######################################################---INVENTARIO MERCHANDISING---######################################################

class InventarioMerchandising(models.Model):

    ESTADOS_INVENTARIO = [
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        ]
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE,blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    fecha_inventario = models.DateField('Fecha de Inventario', auto_now=False, auto_now_add=True, blank=True, null=True)
    hora_inventario = models.TimeField('Hora de Inventario',  auto_now=False, auto_now_add=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMerchandising_responsable', verbose_name='Responsable')
    estado = models.IntegerField('Estado', choices=ESTADOS_INVENTARIO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMerchandising_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Inventario Merchandising'
        verbose_name_plural = 'Inventarios Merchandising'

    def __str__(self):
        return str(self.id)


class InventarioMerchandisingDetalle(models.Model):

    item = models.IntegerField(blank=True, null=True)
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE,blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    inventario_merchandising = models.ForeignKey(InventarioMerchandising, on_delete=models.CASCADE, related_name='InventarioMerchandisingDetalle_inventario_merchandising')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMerchandisingDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMerchandisingDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Inventario Merchandising Detalle'
        verbose_name_plural = 'Inventarios Merchandising Detalle'
        ordering = [
            'inventario_merchandising',
            'item',
            ]

    @property
    def AjusteInventarioMerchandisingDetalle_inventario_merchandising_detalle(self):
        ajuste_inventario_merchandising_detalle = AjusteInventarioMerchandisingDetalle.objects.filter(
            merchandising = self.merchandising,
        )
        return ajuste_inventario_merchandising_detalle

    def __str__(self):
        return str(self.merchandising)


class AjusteInventarioMerchandising(models.Model):

    ESTADOS_AJUSTE_INVENTARIO = [
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        (3, 'ANULADO'),
        ]
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    fecha_ajuste_inventario = models.DateField('Fecha de Inventario', auto_now=False, auto_now_add=True, blank=True, null=True)
    hora_ajuste_inventario = models.TimeField('Hora de Inventario',  auto_now=False, auto_now_add=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMerchandising_responsable', verbose_name='Responsable')
    observacion = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_AJUSTE_INVENTARIO, default=1)
    inventario_merchandising = models.ForeignKey(InventarioMerchandising, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMerchandising_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMerchandising_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Ajuste Inventario Merchandising'
        verbose_name_plural = 'Ajuste Inventarios Merchandising'

    @property
    def fecha(self):
        return self.fecha_ajuste_inventario

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        return str(self.id)


class AjusteInventarioMerchandisingDetalle(models.Model):

    item = models.IntegerField(blank=True, null=True)
    merchandising = models.ForeignKey(Merchandising, on_delete=models.CASCADE,blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    cantidad_stock = models.DecimalField('Cantidad Stock', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    cantidad_contada = models.DecimalField('Cantidad Contada', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    ajuste_inventario_merchandising = models.ForeignKey(AjusteInventarioMerchandising, on_delete=models.CASCADE, related_name='AjusteInventarioMerchandisingDetalle_ajuste_inventario_merchandising')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMerchandisingDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMerchandisingDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Ajuste Inventario Merchandising Detalle'
        verbose_name_plural = 'Ajuste Inventarios Merchandising Detalle'
        ordering = [
            'ajuste_inventario_merchandising',
            'item',
            ]

    def __str__(self):
        return str(self.merchandising)