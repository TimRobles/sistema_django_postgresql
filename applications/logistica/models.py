from decimal import Decimal
from django.db import models
from django.conf import settings
from django_resized import ResizedImageField
from django.contrib.contenttypes.models import ContentType
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.funciones import numeroXn
from applications.logistica import funciones
from applications.logistica.managers import NotaSalidaManager
from applications.muestra.models import DevolucionMuestra
from applications.sociedad.models import Sociedad
from applications.cotizacion.models import ConfirmacionVenta, ConfirmacionVentaDetalle
from applications.variables import ESTADOS
from applications.almacenes.models import Almacen
from applications.calidad.models import Serie
from applications.sede.models import Sede
from applications.material.models import Material
from applications.movimiento_almacen.models import TipoStock
from applications.usuario.models import DatosUsuario

class SolicitudPrestamoMateriales(models.Model):
    ESTADOS_PRESTAMO_MATERIALES = (
        (1, 'EN PROCESO'),
        (2, 'FINALIZADO SIN CONFIRMAR'),
        (3, 'CONFIRMADO'),
        (4, 'ANULADO'),
        (5, 'CONCLUIDO'),
    )
    numero_prestamo = models.IntegerField('Número Prestamo', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    interlocutor_cliente = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT,blank=True, null=True, related_name='SolicitudPrestamoMateriales_interlocutor_cliente')
    fecha_prestamo = models.DateField('Fecha Prestamo', auto_now=False, auto_now_add=False)
    comentario = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_PRESTAMO_MATERIALES, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMateriales_updated_by', editable=False)

    class Meta:

        verbose_name = 'Solicitud Prestamo Materiales'
        verbose_name_plural = 'Solicitudes Prestamo Materiales'
        ordering = ['numero_prestamo',]

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def cotizacion_venta(self):
        return self

    @property
    def fecha(self):
        return self.fecha_prestamo

    @property
    def NotaSalida_solicitud_prestamo_materiales(self):
        lista_nota_salida = []
        notas_salida_documento = NotaSalidaDocumento.objects.filter(
            content_type = self.content_type,
            id_registro = self.id,
        )
        for nota_salida_documento in notas_salida_documento:
            lista_nota_salida.append(nota_salida_documento.nota_salida.id)
        notas_salida = NotaSalida.objects.filter(id__in=lista_nota_salida)
        return notas_salida

    def __str__(self):
        return "%s - %s" % (numeroXn(self.numero_prestamo, 6), self.cliente)

class SolicitudPrestamoMaterialesDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad_prestamo = models.DecimalField('Cantidad Prestamo', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    observacion = models.TextField(blank=True, null=True)
    solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, blank=True, null=True, on_delete=models.CASCADE, related_name='SolicitudPrestamoMaterialesDetalle_solicitud_prestamo_materiales')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMaterialesDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SolicitudPrestamoMaterialesDetalle_updated_by', editable=False)

    class Meta:

        verbose_name = 'Solicitud Prestamo Materiales Detalle'
        verbose_name_plural = 'Solicitudes Prestamo Materiales Detalle'
        ordering = [
            'solicitud_prestamo_materiales',
            'item',
            ]

    @property
    def NotaSalidaDetalle_solicitud_prestamo_materiales_detalle(self):
        notas_salida_detalle = NotaSalidaDetalle.objects.filter(
            content_type_detalle = ContentType.objects.get_for_model(self),
            id_registro_detalle = self.id,
        )
        return notas_salida_detalle

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def cantidad_salida(self):
        total = Decimal('0.00')
        try:
            for detalle in self.NotaSalidaDetalle_solicitud_prestamo_materiales_detalle.exclude(nota_salida__estado=3):
                if detalle.producto == self.producto:
                    total += detalle.cantidad_salida
        except:
            pass
        return total

    @property
    def pendiente(self):
        return self.cantidad_prestamo - self.cantidad_salida

    @property
    def unidad(self):
        return self.producto.unidad_base

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)


class DocumentoPrestamoMateriales(models.Model):
    comentario = models.TextField(blank=True, null=True)
    documento = models.FileField('Documento', blank=True, null=True)
    solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, blank=True, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoPrestamoMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoPrestamoMateriales_updated_by', editable=False)

    class Meta:

        verbose_name = 'Documento Prestamo Materiales'
        verbose_name_plural = 'Documentos Prestamo Materiales'

    def __str__(self):
        return str(self.documento)


class DevolucionPrestamoMateriales(models.Model):
    ESTADOS_PRESTAMO_MATERIALES = (
        (1, 'BORRADOR'),
        (2, 'CONFIRMADO'),
        (3, 'ANULADO'),
    )
    numero_devolucion = models.IntegerField('Número Devolución', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    interlocutor_cliente = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT,blank=True, null=True, related_name='DevolucionPrestamoMateriales_interlocutor_cliente')
    fecha_devolucion = models.DateField('Fecha Devolución', auto_now=False, auto_now_add=False)
    comentario = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    solicitud_prestamo = models.ForeignKey(SolicitudPrestamoMateriales, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_PRESTAMO_MATERIALES, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionPrestamoMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionPrestamoMateriales_updated_by', editable=False)

    class Meta:

        verbose_name = 'Devolucion Prestamo Materiales'
        verbose_name_plural = 'Devoluciones Prestamo Materiales'
        ordering = ['numero_devolucion',]

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def cotizacion_venta(self):
        return self

    @property
    def fecha(self):
        return self.fecha_devolucion

    def __str__(self):
        return "%s - %s" % (numeroXn(self.numero_devolucion, 6), self.cliente)

class DevolucionPrestamoMaterialesDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad_devolucion = models.DecimalField('Cantidad Devuelta', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    observacion = models.TextField(blank=True, null=True)
    devolucion_materiales = models.ForeignKey(DevolucionPrestamoMateriales, blank=True, null=True, on_delete=models.CASCADE, related_name='DevolucionPrestamoMaterialesDetalle_devolucion_materiales')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionPrestamoMaterialesDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionPrestamoMaterialesDetalle_updated_by', editable=False)

    class Meta:

        verbose_name = 'Devolucion Prestamo Materiales Detalle'
        verbose_name_plural = 'Devoluciones Prestamo Materiales Detalle'
        ordering = [
            'devolucion_materiales',
            'item',
            ]

    @property
    def NotaSalidaDetalle_devolucion_materiales_detalle(self):
        notas_salida_detalle = NotaSalidaDetalle.objects.filter(
            content_type_detalle = ContentType.objects.get_for_model(self),
            id_registro_detalle = self.id,
        )
        return notas_salida_detalle

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def cantidad_salida(self):
        total = Decimal('0.00')
        try:
            for detalle in self.NotaSalidaDetalle_devolucion_materiales_detalle.exclude(nota_salida__estado=3):
                if detalle.producto == self.producto:
                    total += detalle.cantidad_salida
        except:
            pass
        return total

    @property
    def pendiente(self):
        return self.cantidad_devolucion - self.cantidad_salida

    @property
    def unidad(self):
        return self.producto.unidad_base

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)

# from applications.logistica.models import NotaSalida, NotaSalidaDocumento
# from django.contrib.contenttypes.models import ContentType
# for nota in NotaSalida.objects.all():
#     if nota.confirmacion_venta:
#         NotaSalidaDocumento.objects.get_or_create(
#             content_type=nota.confirmacion_venta.content_type,
#             id_registro=nota.confirmacion_venta.id,
#             nota_salida=nota,
#             created_by=nota.created_by,
#             updated_by=nota.updated_by,
#         )
#     if nota.solicitud_prestamo_materiales:
#         NotaSalidaDocumento.objects.get_or_create(
#             content_type=nota.solicitud_prestamo_materiales.content_type,
#             id_registro=nota.solicitud_prestamo_materiales.id,
#             nota_salida=nota,
#             created_by=nota.created_by,
#             updated_by=nota.updated_by,
#         )

class NotaSalida(models.Model):
    ESTADOS_NOTA_SALIDA = (
        (1, 'EN PROCESO'),
        (2, 'ATENDIDO'),
        (3, 'ANULADO'),
    )

    # confirmacion_venta = models.ForeignKey(ConfirmacionVenta, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalida_confirmacion_venta')
    # solicitud_prestamo_materiales = models.ForeignKey(SolicitudPrestamoMateriales, on_delete=models.CASCADE, blank=True, null=True, related_name='NotaSalida_solicitud_prestamo_materiales')
    numero_salida = models.IntegerField('Número Salida', blank=True, null=True)
    observacion_adicional = models.TextField('Observación Adicional', blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_NOTA_SALIDA, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalida_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalida_updated_by', editable=False)

    objects = NotaSalidaManager()

    class Meta:
        verbose_name = 'Nota de Salida'
        verbose_name_plural = 'Notas de Salida'
        ordering = ['-numero_salida',]

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def pendiente(self):
        total = Decimal('0.00')
        try:
            for detalle in self.detalles:
                total += detalle.pendiente
        except:
            pass
        return total

    @property
    def fecha(self):
        return self.created_at.date()

    @property
    def confirmacion_venta(self):
        consulta = self.NotaSalidaDocumento_nota_salida.all()
        for documento in consulta:
            if documento.content_type == ContentType.objects.get_for_model(ConfirmacionVenta):
                return documento.documento
        return None

    @property
    def solicitud_prestamo_materiales(self):
        consulta = self.NotaSalidaDocumento_nota_salida.all()
        for documento in consulta:
            if documento.content_type == ContentType.objects.get_for_model(SolicitudPrestamoMateriales):
                return documento.documento
        return None

    # @property
    # def devolucion_muestra(self):
    #     return self.objects.devolucion_muestra()

    @property
    def sociedad(self):
        if self.confirmacion_venta:
            return self.confirmacion_venta.sociedad
        elif self.solicitud_prestamo_materiales:
            return self.solicitud_prestamo_materiales.sociedad
        else:
            return None

    # def get_cliente(self, str):
    #     if not str:
    #         return self.cliente
    #     return None

    @property
    def cliente(self):
        if self.confirmacion_venta:
            return self.confirmacion_venta.cliente
        elif self.solicitud_prestamo_materiales:
            return self.solicitud_prestamo_materiales.cliente
        else:
            return None

    @property
    def interlocutor_cliente(self):
        if self.confirmacion_venta:
            return self.confirmacion_venta.cliente_interlocutor
        elif self.solicitud_prestamo_materiales:
            return self.solicitud_prestamo_materiales.interlocutor_cliente
        else:
            return None

    @property
    def detalles(self):
        return self.NotaSalidaDetalle_nota_salida.all()

    @property
    def documentos(self):
        return self.documentos_despacho + self.documentos_venta

    @property
    def documentos_venta(self):
        documentos = []
        try:
            for factura in self.confirmacion_venta.FacturaVenta_confirmacion.filter(estado=4):
                documentos.append(factura.descripcion)
        except:
            pass
        try:
            for boleta in self.confirmacion_venta.BoletaVenta_confirmacion.filter(models.Q(estado=4) | models.Q(estado=5)):
                documentos.append(boleta.descripcion)
        except:
            pass
        return documentos

    @property
    def documentos_venta_objeto(self):
        documentos = []
        try:
            for factura in self.confirmacion_venta.FacturaVenta_confirmacion.filter(estado=4):
                documentos.append(factura)
        except:
            pass
        try:
            for boleta in self.confirmacion_venta.BoletaVenta_confirmacion.filter(models.Q(estado=4) | models.Q(estado=5)):
                documentos.append(boleta)
        except:
            pass
        return documentos

    @property
    def documentos_despacho(self):
        guias = []
        try:
            despachos = self.Despacho_nota_salida.all()
            for despacho in despachos:
                for guia in despacho.Guia_despacho.filter(estado=4):
                    guias.append(guia.descripcion)
        except:
            pass
        return guias

    def __str__(self):
        return "%s" % (numeroXn(self.numero_salida, 6))


# from applications.logistica.models import NotaSalidaDetalle, SolicitudPrestamoMaterialesDetalle
# from applications.cotizacion.models import ConfirmacionVentaDetalle
# from django.contrib.contenttypes.models import ContentType
# for detalle in NotaSalidaDetalle.objects.all():
#     if detalle.confirmacion_venta_detalle:
#         detalle.content_type_detalle=ContentType.objects.get_for_model(ConfirmacionVentaDetalle)
#         detalle.id_registro_detalle=detalle.confirmacion_venta_detalle.id
#     elif detalle.solicitud_prestamo_materiales_detalle:
#         detalle.content_type_detalle=ContentType.objects.get_for_model(SolicitudPrestamoMaterialesDetalle)
#         detalle.id_registro_detalle=detalle.solicitud_prestamo_materiales_detalle.id
#     detalle.save()


class NotaSalidaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    # confirmacion_venta_detalle = models.ForeignKey(ConfirmacionVentaDetalle, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDetalle_confirmacion_venta_detalle')
    # solicitud_prestamo_materiales_detalle = models.ForeignKey(SolicitudPrestamoMaterialesDetalle, on_delete=models.CASCADE, blank=True, null=True, related_name='NotaSalidaDetalle_solicitud_prestamo_materiales_detalle')
    content_type_detalle = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE) #ConfirmacionDetalle / SolicitudPrestamoDetalle / DevolucionMuestraDetalle / DevolucionGarantiaDetalle
    id_registro_detalle = models.IntegerField(blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    cantidad_salida = models.DecimalField('Cantidad Salida', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    nota_salida = models.ForeignKey(NotaSalida, on_delete=models.CASCADE, related_name='NotaSalidaDetalle_nota_salida')
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Salida Detalle'
        verbose_name_plural = 'Notas de Salida Detalle'
        ordering = [
            'nota_salida',
            'item',
            ]

    @property
    def detalle(self):
        return self.content_type_detalle.get_object_for_this_type(id=self.id_registro_detalle)

    @property
    def confirmacion_venta_detalle(self):
        if self.content_type_detalle == ContentType.objects.get_for_model(ConfirmacionVentaDetalle):
            return self.detalle
        return None

    @property
    def solicitud_prestamo_materiales_detalle(self):
        if self.content_type_detalle == ContentType.objects.get_for_model(SolicitudPrestamoMaterialesDetalle):
            return self.detalle
        return None

    @property
    def producto(self):
        try:
            return self.confirmacion_venta_detalle.producto
        except:
            return self.solicitud_prestamo_materiales_detalle.producto

    @property
    def despachado(self):
        total = Decimal('0.00')
        try:
            for despacho in self.nota_salida.Despacho_nota_salida.exclude(estado=3):
                for detalle in despacho.DespachoDetalle_despacho.all():
                    if detalle.producto == self.producto:
                        total += detalle.cantidad_despachada
        except:
            pass
        return total

    @property
    def pendiente(self):
        return self.cantidad_salida - self.despachado

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.producto)

    @property
    def id_registro(self):
        return self.producto.id

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieNotaSalidaDetalle_nota_salida_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return "%s" % (self.item)


class NotaSalidaDocumento(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE) #Confirmacion / SolicitudPrestamo / DevolucionMuestra / DevolucionGarantia
    id_registro = models.IntegerField(blank=True, null=True)
    nota_salida = models.ForeignKey(NotaSalida, on_delete=models.CASCADE, related_name='NotaSalidaDocumento_nota_salida')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDocumento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaSalidaDocumento_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota Salida Documento'
        verbose_name_plural = 'Nota Salida Documentos'

    @property
    def confirmacion_venta(self):
        if self.content_type == ContentType.objects.get_for_model(ConfirmacionVenta):
            return self.documento
        return None

    @property
    def solicitud_prestamo_materiales(self):
        if self.content_type == ContentType.objects.get_for_model(SolicitudPrestamoMateriales):
            return self.documento
        return None

    @property
    def devolucion_muestra(self):
        if self.content_type == ContentType.objects.get_for_model(DevolucionMuestra):
            return self.documento
        return None

    @property
    def documento(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    def __str__(self):
        return f"{self.documento} - {self.nota_salida}"



class ValidarSerieNotaSalidaDetalle(models.Model):
    nota_salida_detalle = models.ForeignKey(NotaSalidaDetalle, on_delete=models.PROTECT, related_name='ValidarSerieNotaSalidaDetalle_nota_salida_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieNotaSalidaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieNotaSalidaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Nota de Salida Detalle'
        verbose_name_plural = 'Validar Series Notas de Salida Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.nota_salida_detalle , str(self.serie))
        
        
class Despacho(models.Model):
    ESTADOS_DESPACHO = (
    (1, 'EN PROCESO'),
    (2, 'DESPACHADO'),
    (3, 'ANULADO'),
    (4, 'CONCLUIDO SIN GUIA'),
    (5, 'CONCLUIDO CON GUIA'),
    (6, 'GUIA ANULADA'),
)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE,blank=True, null=True)
    nota_salida = models.ForeignKey(NotaSalida, on_delete=models.CASCADE,blank=True, null=True, related_name='Despacho_nota_salida')
    numero_despacho = models.IntegerField('Número Despacho', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True, null=True)
    fecha_despacho = models.DateField('Fecha Despacho', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_DESPACHO, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Despacho_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Despacho_updated_by', editable=False)

    class Meta:

        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['-numero_despacho',]

    @property
    def detalles(self):
        return self.DespachoDetalle_despacho.all()

    @property
    def fecha(self):
        return self.fecha_despacho

    def __str__(self):
        return "%s - %s" % (numeroXn(self.numero_despacho, 6), self.cliente)

class DespachoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad_despachada = models.DecimalField('Cantidad Despachada', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    despacho = models.ForeignKey(Despacho, on_delete=models.CASCADE, related_name='DespachoDetalle_despacho')
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DespachoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DespachoDetalle_updated_by', editable=False)

    class Meta:

        verbose_name = 'Despacho Detalle'
        verbose_name_plural = 'Despachos Detalle'
        ordering = [
            'despacho',
            'item',
            ]
    
    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def unidad(self):
        return self.producto.unidad_base

    def __str__(self):
        return str(self.producto)


class ImagenesDespacho(models.Model):
    imagen = ResizedImageField(force_format="WEBP", quality=75, upload_to="img/imagenes-despacho/")
    despacho = models.ForeignKey(Despacho, on_delete=models.CASCADE, related_name='ImagenesDespacho_despacho')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ImagenesDespacho_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ImagenesDespacho_updated_by', editable=False)

    class Meta:
        verbose_name = 'Imagenes Despacho'
        verbose_name_plural = 'Imagenes Despachos'

    def __str__(self):
        return str(self.imagen)


class InventarioMateriales(models.Model):

    ESTADOS_INVENTARIO = [
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        ]
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE,blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    fecha_inventario = models.DateField('Fecha de Inventario', auto_now=False, auto_now_add=True, blank=True, null=True)
    hora_inventario = models.TimeField('Hora de Inventario',  auto_now=False, auto_now_add=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMateriales_responsable', verbose_name='Responsable')
    estado = models.IntegerField('Estado', choices=ESTADOS_INVENTARIO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMateriales_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Inventario Materiales'
        verbose_name_plural = 'Inventarios Materiales'

    def __str__(self):
        return str(self.id)


class InventarioMaterialesDetalle(models.Model):

    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE,blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    inventario_materiales = models.ForeignKey(InventarioMateriales, on_delete=models.CASCADE, related_name='InventarioMaterialesDetalle_inventario_materiales')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMaterialesDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioMaterialesDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Inventario Materiales Detalle'
        verbose_name_plural = 'Inventarios Materiales Detalle'
        ordering = [
            'inventario_materiales',
            'item',
            ]

    @property
    def AjusteInventarioMaterialesDetalle_inventario_materiales_detalle(self):
        ajuste_inventario_materiales_detalle = AjusteInventarioMaterialesDetalle.objects.filter(
            material = self.material,
        )
        return ajuste_inventario_materiales_detalle

    def __str__(self):
        return str(self.material)


class AjusteInventarioMateriales(models.Model):

    ESTADOS_AJUSTE_INVENTARIO = [
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        (3, 'ANULADO'),
        ]
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    fecha_ajuste_inventario = models.DateField('Fecha de Inventario', auto_now=False, auto_now_add=True, blank=True, null=True)
    hora_ajuste_inventario = models.TimeField('Hora de Inventario',  auto_now=False, auto_now_add=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMateriales_responsable', verbose_name='Responsable')
    observacion = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_AJUSTE_INVENTARIO, default=1)
    inventario_materiales = models.ForeignKey(InventarioMateriales, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMateriales_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMateriales_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Ajuste Inventario Materiales'
        verbose_name_plural = 'Ajuste Inventarios Materiales'

    @property
    def fecha(self):
        return self.fecha_ajuste_inventario

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        return str(self.id)


class AjusteInventarioMaterialesDetalle(models.Model):

    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE,blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    cantidad_stock = models.DecimalField('Cantidad Stock', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    cantidad_contada = models.DecimalField('Cantidad Contada', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    ajuste_inventario_materiales = models.ForeignKey(AjusteInventarioMateriales, on_delete=models.CASCADE, related_name='AjusteInventarioMaterialesDetalle_ajuste_inventario_materiales')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMaterialesDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AjusteInventarioMaterialesDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Ajuste Inventario Materiales Detalle'
        verbose_name_plural = 'Ajuste Inventarios Materiales Detalle'
        ordering = [
            'ajuste_inventario_materiales',
            'item',
            ]

    def __str__(self):
        return str(self.material)
