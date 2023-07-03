from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import ArchivoRecepcionCompra, DocumentoReclamoDetalle, FotoRecepcionCompra, RecepcionCompra

class ArchivoRecepcionCompraForm(BSModalModelForm):
    class Meta:
        model = ArchivoRecepcionCompra
        fields=(
            'archivo',
            )

    def __init__(self, *args, **kwargs):
        super(ArchivoRecepcionCompraForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FotoRecepcionCompraForm(BSModalModelForm):
    class Meta:
        model = FotoRecepcionCompra
        fields=(
            'foto',
            )

    def __init__(self, *args, **kwargs):
        super(FotoRecepcionCompraForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RecepcionCompraGenerarNotaIngresoForm(BSModalForm):
    fecha_ingreso = forms.DateField(
        widget=forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    class Meta:
        fields=(
            'fecha_ingreso',
            )

    def __init__(self, *args, **kwargs):
        super(RecepcionCompraGenerarNotaIngresoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RecepcionCompraAnularForm(BSModalModelForm):
    class Meta:
        model = RecepcionCompra
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(RecepcionCompraAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DocumentoReclamoDetalleForm(BSModalModelForm):
    class Meta:
        model = DocumentoReclamoDetalle
        fields=(
            'accion',
            )

    def __init__(self, *args, **kwargs):
        super(DocumentoReclamoDetalleForm, self).__init__(*args, **kwargs)
        detalle = kwargs['instance']
        if detalle.tipo == 1:
            ACCION_RECLAMO_DETALLE = (
                (2, 'NO HACER NADA'),
                (3, 'POR PAGAR'),
            )
        else:
            ACCION_RECLAMO_DETALLE = (
                (1, 'DESCONTAR'),
                (2, 'NO HACER NADA'),
            )
        self.fields['accion'].choices = ACCION_RECLAMO_DETALLE
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DocumentoReclamoDetalleMontoForm(BSModalModelForm):
    class Meta:
        model = DocumentoReclamoDetalle
        fields=(
            'factor',
            'adicional',
            )

    def __init__(self, *args, **kwargs):
        super(DocumentoReclamoDetalleMontoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'