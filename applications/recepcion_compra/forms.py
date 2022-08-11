from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import ArchivoRecepcionCompra, FotoRecepcionCompra

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