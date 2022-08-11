from django.contrib import admin

from applications.encuesta.models import Alternativa, Encuesta, Pregunta, Respuesta, RespuestaDetalle

# Register your models here.
@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
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


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'texto',
        'tipo_pregunta',
        'orden',
        'mostrar',
        'encuesta',
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


@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pregunta',
        'orden',
        'texto',
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


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'interlocutor',
        'nombre_interlocutor',
        'tipo_interlocutor',
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


@admin.register(RespuestaDetalle)
class RespuestaDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'respuesta',
        'alternativa',
        'pregunta',
        'texto',
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