from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import FallaMaterial


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