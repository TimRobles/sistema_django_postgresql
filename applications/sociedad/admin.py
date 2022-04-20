from django.contrib import admin

from applications.sociedad.models import Sociedad, Documento, TipoRepresentanteLegal, RepresentanteLegal

# Register your models here.

class SociedadAdmin(admin.ModelAdmin):
    '''Admin View for Sociedad'''

    list_display = (
        'razon_social',
        'ruc',
        'direccion_legal',
        'ubigeo',
        'estado_sunat',
        )
    exclude = (
        'estado_sunat',
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
        )
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class TipoRepresentanteLegalAdmin(admin.ModelAdmin):
    '''Admin View for TipoRepresentanteLegal'''

    list_display = ('nombre',)

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
