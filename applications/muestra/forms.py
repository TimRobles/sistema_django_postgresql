from django import forms
from applications.muestra.models import NotaIngresoMuestra
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class NotaIngresoMuestraAgregarMaterialForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        fields=(
            'producto',
            'cantidad',
            )
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        try:
            nota_ingreso_muestra_detalle = kwargs.pop('nota_ingreso_muestra_detalle')
        except:
            pass
        super(NotaIngresoMuestraAgregarMaterialForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        try:
            valor = "%s|%s" % (nota_ingreso_muestra_detalle.content_type.id, nota_ingreso_muestra_detalle.id_registro)
            self.fields['producto'].initial = valor
            self.fields['cantidad'].initial = nota_ingreso_muestra_detalle.cantidad_total
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraGuardarForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMuestra
        fields = (
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraGuardarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraAnularForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMuestra
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMuestra
        fields = (
            'sociedad',
            'fecha_ingreso',
            )
        widgets = {
            'fecha_ingreso' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraGenerarNotaIngresoForm(BSModalForm):
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
        super(NotaIngresoMuestraGenerarNotaIngresoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'