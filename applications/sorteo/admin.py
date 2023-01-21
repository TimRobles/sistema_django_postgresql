from django.contrib import admin
from .models import Sorteo, Ticket

# Register your models here.
@admin.register(Sorteo)
class SorteoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_sorteo',
        'nombre_dato_uno',
        'nombre_dato_dos',
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

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dato_uno',
        'dato_dos',
        'premio',
        'elegido',
        'bloqueo',
        'sorteo',
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
