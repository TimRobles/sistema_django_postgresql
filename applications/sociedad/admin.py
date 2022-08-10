from django.contrib import admin

from applications.sociedad.models import (
    Sociedad, 
    Documento, 
    TipoRepresentanteLegal, 
    RepresentanteLegal,
    )

from applications.sociedad.forms import (
    TipoRepresentanteLegalForm,    
    )
# Register your models here.

class SociedadAdmin(admin.ModelAdmin):
    '''Admin View for Sociedad'''

    list_display = (
        'id',
        'razon_social',
        'nombre_comercial',
        'abreviatura',
        'ruc',
        'direccion_legal',
        'ubigeo',
        'distrito',
        'estado_sunat',
        'condicion_sunat',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    exclude = (
        'tipo_documento',
        'razon_social',
        'direccion_legal',
        'ubigeo',
        'distrito',
        'estado_sunat',
        'condicion_sunat',
        'logo',
        'color',
        )

    ordering = (
        'razon_social',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class DocumentoAdmin(admin.ModelAdmin):
    '''Admin View for Sociedad'''

    list_display = (
        'nombre_documento',
        'descripcion_documento',
        'documento',
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

class TipoRepresentanteLegalAdmin(admin.ModelAdmin):
    '''Admin View for TipoRepresentanteLegal'''

    list_display = (
        'nombre',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = TipoRepresentanteLegalForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class RepresentanteLegalAdmin(admin.ModelAdmin):
    '''Admin View for TipoRepresentanteLegal'''

    list_display = (
        'usuario',
        'sociedad',
        'tipo_representante_legal',
        'fecha_registro',
        'fecha_baja',
        'estado',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )
    exclude = (
        'fecha_baja',
        'estado',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Sociedad, SociedadAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(TipoRepresentanteLegal, TipoRepresentanteLegalAdmin)
admin.site.register(RepresentanteLegal, RepresentanteLegalAdmin)
