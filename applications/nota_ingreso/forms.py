from django import forms
from django.contrib.auth import get_user_model
from applications.almacenes.models import Almacen
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class NotaIngresoAgregarMaterialForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.IntegerField()
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.all())
    class Meta:
        fields=(
            'producto',
            'cantidad',
            'almacen',
            )
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        super(NotaIngresoAgregarMaterialForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'