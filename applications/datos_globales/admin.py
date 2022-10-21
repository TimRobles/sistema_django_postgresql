from django.contrib import admin

from applications.datos_globales.forms import (
    AreaForm,
    CargoForm,
    MonedaForm,
    TipoInterlocutorForm,
    PaisForm    
    )

from .models import (
    ImpuestoPromocionMunicipal,
    Moneda,
    Magnitud,
    NubefactAcceso,
    NubefactRespuesta,
    NubefactSerieAcceso,
    TipoCambioSunat,
    Unidad, 
    Area, 
    Cargo,
    TipoInterlocutor, 
    Pais,
    Departamento, 
    Provincia, 
    Distrito,
    Banco,
    DocumentoProceso,
    DocumentoFisico,
    RangoDocumentoProceso,
    RangoDocumentoFisico,
    CuentaBancariaSociedad,
    CuentaBancariaPersonal,
    SegmentoSunat,
    FamiliaSunat,
    ClaseSunat,
    ProductoSunat,
    TipoCambio, 
    RemuneracionMinimaVital,
    UnidadImpositivaTributaria,
    ImpuestoGeneralVentas,
    SeriesComprobante,
)

class MonedaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'abreviatura',
        'simbolo',
        'principal',
        'secundario',
        'moneda_pais',
        'nubefact',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    
    form = MonedaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class MagnitudAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        

class UnidadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'simbolo',
        'unidad_sunat',
        'magnitud',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class AreaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = AreaForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'area',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = CargoForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

        
class TipoInterlocutorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    
    form = TipoInterlocutorForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class PaisAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    
    form = PaisForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'departamento',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DistritoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'provincia',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    search_fields = (
        'codigo',
        'nombre',
    )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class BancoAdmin(admin.ModelAdmin):
    list_display = (
        'razon_social',
        'nombre_comercial',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DocumentoProcesoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
        'modelo',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DocumentoFisicoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
        'modelo',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class RangoDocumentoProcesoAdmin(admin.ModelAdmin):
    list_display = (
        'serie',
        'rango_inicial',
        'modelo',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class RangoDocumentoFisicoAdmin(admin.ModelAdmin):
    list_display = (
        'serie',
        'rango_inicial',
        'modelo',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class CuentaBancariaSociedadAdmin(admin.ModelAdmin):
    list_display = (
        'numero_cuenta',
        'numero_cuenta_interbancaria',
        'banco',
        'moneda',
        'sociedad',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class CuentaBancariaPersonalAdmin(admin.ModelAdmin):
    list_display = (
        'numero_cuenta',
        'numero_cuenta_interbancaria',
        'banco',
        'moneda',
        'usuario',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class SegmentoSunatAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'descripcion',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class FamiliaSunatAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'descripcion',
        'segmento',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ClaseSunatAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'descripcion',
        'familia',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ProductoSunatAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'descripcion',
        'clase',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TipoCambioAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'tipo_cambio_venta',
        'tipo_cambio_compra',
        'moneda_origen',
        'moneda_destino',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TipoCambioSunatAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'tipo_cambio_venta',
        'tipo_cambio_compra',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class RemuneracionMinimaVitalAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'monto',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class UnidadImpositivaTributariaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'monto',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ImpuestoGeneralVentasAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'monto',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class ImpuestoPromocionMunicipalAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inicio',
        'monto',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(SeriesComprobante)
class SeriesComprobanteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo_comprobante',
        'serie',
        'defecto',
        'contingencia',
        'mostrar',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Moneda, MonedaAdmin)
admin.site.register(Magnitud, MagnitudAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(TipoInterlocutor, TipoInterlocutorAdmin)

admin.site.register(Pais, PaisAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Distrito, DistritoAdmin)

admin.site.register(Banco, BancoAdmin)

admin.site.register(DocumentoProceso, DocumentoProcesoAdmin)
admin.site.register(DocumentoFisico, DocumentoFisicoAdmin)

admin.site.register(RangoDocumentoProceso, RangoDocumentoProcesoAdmin)
admin.site.register(RangoDocumentoFisico, RangoDocumentoFisicoAdmin)

admin.site.register(CuentaBancariaSociedad, CuentaBancariaSociedadAdmin)
admin.site.register(CuentaBancariaPersonal, CuentaBancariaPersonalAdmin)

admin.site.register(SegmentoSunat, SegmentoSunatAdmin)
admin.site.register(FamiliaSunat, FamiliaSunatAdmin)
admin.site.register(ClaseSunat, ClaseSunatAdmin)
admin.site.register(ProductoSunat, ProductoSunatAdmin)

admin.site.register(TipoCambio, TipoCambioAdmin)
admin.site.register(TipoCambioSunat, TipoCambioSunatAdmin)
admin.site.register(RemuneracionMinimaVital, RemuneracionMinimaVitalAdmin)
admin.site.register(UnidadImpositivaTributaria, UnidadImpositivaTributariaAdmin)
admin.site.register(ImpuestoGeneralVentas, ImpuestoGeneralVentasAdmin)
admin.site.register(ImpuestoPromocionMunicipal, ImpuestoPromocionMunicipalAdmin)


@admin.register(NubefactAcceso)
class NubefactAccesoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'descripcion',
        'ruta',
        'token',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(NubefactSerieAcceso)
class NubefactSerieAccesoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sociedad',
        'content_type',
        'serie_comprobante',
        'acceso',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(NubefactRespuesta)
class NubefactRespuestaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content_type',
        'id_registro',
        'aceptado',
        'error',
        'envio',
        'respuesta',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)