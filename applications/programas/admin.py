from django.contrib import admin

from .models import NivelCuatro, NivelTres, NivelDos, NivelUno

# Register your models here.
class NivelUnoAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'icono',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class NivelDosAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'app_name',
        'nivel_uno',
        'icono',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class NivelTresAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'url_name',
        'nivel_dos',
        'icono',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class NivelCuatroAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'url_name',
        'nivel_tres',
        'icono',
        )

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(NivelUno, NivelUnoAdmin)
admin.site.register(NivelDos, NivelDosAdmin)
admin.site.register(NivelTres, NivelTresAdmin)
admin.site.register(NivelCuatro, NivelCuatroAdmin)