from django import forms
from applications.envio_clientes.models import Transportista
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class TransportistaForm(BSModalModelForm):
    class Meta:
        model = Transportista
        fields = (
            'tipo_documento',
            'numero_documento',
            'razon_social',
            )

    def __init__(self, *args, **kwargs):
        super(TransportistaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_tipo_documento(self):
        tipo_documento = self.cleaned_data.get('tipo_documento')
        if tipo_documento == '-':
            self.fields['numero_documento'].required = False
        else:
            self.fields['numero_documento'].required = True
    
        return tipo_documento
    
    def clean(self):
        cleaned_data = super().clean()
        numero_documento = cleaned_data.get('numero_documento')
        filtro = Transportista.objects.filter(numero_documento__unaccent__iexact = numero_documento)
        if numero_documento != self.instance.numero_documento:
            if len(filtro)>0:
                self.add_error('numero_documento', 'Ya existe un Transportista con este Número de documento')

class TransportistaBuscarForm(forms.Form):
    razon_social = forms.CharField(label = 'Razón Social', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        filtro_razon_social = kwargs.pop('filtro_razon_social')
        super(TransportistaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].initial = filtro_razon_social
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'