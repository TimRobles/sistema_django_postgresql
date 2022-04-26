from django.contrib import admin

from .models import (
    Moneda,
    Magnitud, 
    Unidad, 
    Area, 
    Cargo,
    TipoInterlocutor, 
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
)

class MonedaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'abreviatura',
        'simbolo',
        'estado',
        )

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
        'magnitud',
        'nombre',
        'simbolo',
        'unidad_sunat',
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

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'area',
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

        
class TipoInterlocutorAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class BancoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
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
        'modelo',
        'serie',
        'rango_inicial',
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
        'modelo',
        'serie',
        'rango_inicial',
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
        'sociedad',
        'banco',
        'moneda',
        'numero_cuenta',
        'numero_cuenta_interbancaria',
        'estado',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class CuentaBancariaPersonalAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'banco',
        'moneda',
        'numero_cuenta',
        'numero_cuenta_interbancaria',
        'estado',
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


admin.site.register(Moneda, MonedaAdmin)
admin.site.register(Magnitud, MagnitudAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(TipoInterlocutor, TipoInterlocutorAdmin)

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
