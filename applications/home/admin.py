from django.contrib import admin

from .models import AplicacionDos, AplicacionUno

class AplicacionUnoAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'app_name',
        'url_name',
        'logo',
        )

class AplicacionDosAdmin(admin.ModelAdmin):
    list_display = (
        'orden',
        'nombre',
        'app_name',
        'url_name',
        'aplicacion_uno',
        'logo',
        )

admin.site.register(AplicacionUno, AplicacionUnoAdmin)
admin.site.register(AplicacionDos, AplicacionDosAdmin)