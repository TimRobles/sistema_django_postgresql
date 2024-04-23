from django.contrib import admin


from . models import(
    Notificaciones,
)

@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'titulo',
        'mensaje',
        'leido',
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