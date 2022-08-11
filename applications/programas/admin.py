from django.contrib import admin

from applications.programas.forms import NivelUnoForm, NivelDosForm, NivelTresForm, NivelCuatroForm

from .models import NivelCuatro, NivelTres, NivelDos, NivelUno

# Register your models here.
class NivelUnoAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'icono',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = NivelUnoForm

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
        'url_name',
        'nivel_uno',
        'icono',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = NivelDosForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class NivelTresAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'app_name',
        'url_name',
        'nivel_dos',
        'icono',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = NivelTresForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class NivelCuatroAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'app_name',
        'url_name',
        'nivel_tres',
        'icono',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        )

    form = NivelCuatroForm

    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(NivelUno, NivelUnoAdmin)
admin.site.register(NivelDos, NivelDosAdmin)
admin.site.register(NivelTres, NivelTresAdmin)
admin.site.register(NivelCuatro, NivelCuatroAdmin)