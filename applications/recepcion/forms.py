from django import forms

from .models import Visita

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class VisitaForm(BSModalModelForm):
    class Meta:
        model = Visita
        fields=(
            'nombre',
            'tipo_documento',
            'numero_documento',
            'usuario_atendio',
            'motivo_visita',
            'empresa_cliente',
            )

    def __init__(self, *args, **kwargs):
        super(VisitaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'