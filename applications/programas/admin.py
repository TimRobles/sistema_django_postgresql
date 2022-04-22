from django.contrib import admin

from .models import NivelCuatro, NivelTres, NivelDos, NivelUno

# Register your models here.
class NivelUnoAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'icono',
        )

class NivelDosAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'app_name',
        'nivel_uno',
        'icono',
        )

class NivelTresAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'url_name',
        'nivel_dos',
        'icono',
        )

class NivelCuatroAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'url_name',
        'nivel_tres',
        'icono',
        )

admin.site.register(NivelUno, NivelUnoAdmin)
admin.site.register(NivelDos, NivelDosAdmin)
admin.site.register(NivelTres, NivelTresAdmin)
admin.site.register(NivelCuatro, NivelCuatroAdmin)