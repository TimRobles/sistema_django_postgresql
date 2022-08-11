from dataclasses import fields
from .models import ActivoBase
from bootstrap_modal_forms.forms import BSModalModelForm


class ActivoBaseForm(BSModalModelForm):
    class Meta:
        model = ActivoBase
        fields = (
            'descripcion_venta',
            'descripcion_corta',
            'unidad',
            'peso',
            'sub_familia',
            'depreciacion',
            'producto_sunat',
            'traduccion',
            'partida',
            )

    def __init__(self, *args, **kwargs):
        super(ActivoBaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'