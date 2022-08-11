from django import forms
from django.contrib.auth import get_user_model
from applications.almacenes.models import Almacen
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class NotaIngresoAgregarMaterialForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Almacen.objects.none())
    cantidad = forms.IntegerField()
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.all())
    class Meta:
        fields=(
            'material',
            'cantidad',
            'almacen',
            )
        
    def __init__(self, *args, **kwargs):
        super(NotaIngresoAgregarMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'