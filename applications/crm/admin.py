from django.contrib import admin

from .models import (
    # ClienteCRM, 
    ClienteCRMDetalle, 
    EventoCRM, 
    EventoCRMDetalle, 
    EventoCRMDetalleInformacionAdicional, 
    PreguntaCRM, 
    EncuestaCRM, 
    AlternativaCRM, 
    RespuestaCRM, 
    RespuestaDetalleCRM,
    )

# @admin.register(ClienteCRM)
# class ClienteCRMAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'cliente_crm',
#         'medio',
#         'fecha_registro',
#         'estado',
#         'created_by',
#         'created_at',
#         'updated_by',
#         'updated_at',        
#         )
        
    # def save_model(self, request, obj, form, change):
    #     if obj.created_by == None:
    #         obj.created_by = request.user
    #     obj.updated_by = request.user
    #     super().save_model(request, obj, form, change)

@admin.register(ClienteCRMDetalle)
class ClienteCRMDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'tipo_actividad',
        # 'interlocutor',
        'fecha',
        'lugar',
        'motivo',
        'descripcion',
        'acuerdos',
        'quejas',
        'numero_caso',
        'tecnico_asignado',
        'nombre',
        'archivo',
        # 'cantidad',
        'cliente_crm',
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

@admin.register(EventoCRM)
class EventoCRMAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'titulo',
        'pais',
        'ubicacion',
        'encargado',
        'fecha_inicio',
        'fecha_cierre',
        'presupuesto_asignado',
        'presupuesto_utilizado',
        'moneda',
        'total_merchandising',
        'descripcion',
        'sorteo',
        'sociedad',
        'sede_origen',
        'estado',        
        )
        
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(EventoCRMDetalle)
class EventoDetalleCRMAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'item',
        'content_type',
        'id_registro',
        'almacen_origen',
        'tipo_stock',
        'cantidad_asignada',
        'cantidad_utilizada',
        'cantidad_restante',
        'unidad',
        'evento_crm',
        )
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(EventoCRMDetalleInformacionAdicional)
class EventoDetalleCRMInformacionAdicionalAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'fecha',
        'comentario',
        'evento_crm',
        )
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(PreguntaCRM)
class PreguntaCRMAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'tipo_pregunta',
        'texto',
        'orden',
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

@admin.register(EncuestaCRM)
class EncuestaCRMAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'tipo_encuesta',
        'titulo',
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

@admin.register(AlternativaCRM)
class AlternativaCRMAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'orden',
        'texto',
        'mostrar',
        'pregunta_crm',
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

@admin.register(RespuestaCRM)
class RespuestaCRMAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'cliente_crm',
        'interlocutor',
        'nombre_interlocutor',
        'encuesta_crm',
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

@admin.register(RespuestaDetalleCRM)
class RespuestaDetalleCRMAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'alternativa_crm',
        'pregunta_crm',
        'respuesta_crm',
        'texto',
        'borrador',
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
