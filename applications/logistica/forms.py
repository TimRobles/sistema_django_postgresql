from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.logistica.models import DocumentoPrestamoMateriales, NotaSalida, NotaSalidaDetalle, SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle
from django import forms

from applications.material.models import Material

class SolicitudPrestamoMaterialesForm(BSModalModelForm):
    class Meta:
        model = SolicitudPrestamoMateriales
        fields = (
            'sociedad',
            'cliente',
            'interlocutor_cliente',
            'fecha_prestamo',
            'comentario',
            )

        widgets = {
            'fecha_prestamo' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudPrestamoMaterialesDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad_prestamo = forms.DecimalField(label = 'Cantidad Prestamo', max_digits=22, decimal_places=10)
    observacion = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        fields = (
            'material',
            'cantidad_prestamo',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudPrestamoMaterialesDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    class Meta:
        model = SolicitudPrestamoMaterialesDetalle
        fields=(
            'material',
            'cantidad_prestamo',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        self.fields['material'].initial = busqueda_material.descripcion_venta
        self.fields['material'].disabled = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudPrestamoMaterialesAnularForm(BSModalModelForm):
    class Meta:
        model = SolicitudPrestamoMateriales
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DocumentoPrestamoMaterialesForm(BSModalModelForm):
    class Meta:
        model = DocumentoPrestamoMateriales
        fields=(
            'comentario',
            'documento',
            )

    def __init__(self, *args, **kwargs):
        super(DocumentoPrestamoMaterialesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaForm(BSModalModelForm):
    class Meta:
        model = NotaSalida
        fields = (
            'observacion_adicional',
            )

    def __init__(self, *args, **kwargs):
        super(NotaSalidaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaDetalleForm(BSModalModelForm):
    class Meta:
        model = NotaSalidaDetalle
        fields = (
            'confirmacion_venta_detalle',
            'solicitud_prestamo_materiales_detalle',
            'sede',
            'almacen',
            'cantidad_salida',
            )

    def __init__(self, *args, **kwargs):
        super(NotaSalidaDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'