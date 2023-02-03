from django import forms

from applications.sociedad.models import Sociedad


class NotaCreditoBuscarForm(forms.Form):
    cliente = forms.CharField(max_length=150, required=False)
    numero_nota = forms.CharField(max_length=10, required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    fecha = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )


    def __init__(self, *args, **kwargs):
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_numero_nota = kwargs.pop('filtro_numero_nota')
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_fecha = kwargs.pop('filtro_fecha')
        super(NotaCreditoBuscarForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].initial = filtro_cliente
        self.fields['numero_nota'].initial = filtro_numero_nota
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['fecha'].initial = filtro_fecha
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'