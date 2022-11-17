from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import FallaMaterial, NotaControlCalidadStock, NotaControlCalidadStockDetalle


class FallaMaterialForm(BSModalModelForm):
    class Meta:
        model = FallaMaterial
        fields=(
            'titulo',
            'comentario',
            'visible',
            )

    def __init__(self, *args, **kwargs):
        super(FallaMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['visible'].widget.attrs['class'] = 'form-check-input'

class NotaControlCalidadStockForm(BSModalModelForm):
    class Meta:
        model = NotaControlCalidadStock
        fields=(
            'nota_ingreso',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockAnularForm(BSModalModelForm):
    class Meta:
        model = NotaControlCalidadStock
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockAnularForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockDetalleAgregarForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = NotaControlCalidadStockDetalle
        fields=(
            'material',
            'cantidad_calidad',
            'inspeccion',
            )

    def __init__(self, *args, **kwargs):
        lista_materiales = kwargs.pop('materiales')
        super(NotaControlCalidadStockDetalleAgregarForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    class Meta:
        model = NotaControlCalidadStockDetalle
        fields=(
            'material',
            'cantidad_calidad',
            'inspeccion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockDetalleUpdateForm, self).__init__(*args, **kwargs)
        descripcion_material = self.instance.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
        self.fields['material'].initial = descripcion_material.content_type.get_object_for_this_type(id = descripcion_material.id_registro)
        self.fields['material'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['material'].disabled = True