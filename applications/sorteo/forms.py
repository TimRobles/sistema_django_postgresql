from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

from applications.sorteo.models import Sorteo, Ticket

class SorteoForm(BSModalModelForm):
    class Meta:
        model = Sorteo
        fields = (
            'nombre_sorteo',
            'nombre_dato_uno',
            'nombre_dato_dos',
            'nombre_dato_tres',
            'nombre_dato_cuatro',
            )
    
    def __init__(self, *args, **kwargs):
        super(SorteoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TicketForm(BSModalModelForm):
    class Meta:
        model = Ticket
        fields = (
            'dato_uno',
            'dato_dos',
            'dato_tres',
            'dato_cuatro',
            )
    
    def __init__(self, *args, **kwargs):
        sorteo = kwargs.pop('sorteo')
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['dato_uno'].label = sorteo.nombre_dato_uno
        self.fields['dato_dos'].label = sorteo.nombre_dato_dos
        print(sorteo.nombre_dato_tres)
        self.fields['dato_tres'].label = sorteo.nombre_dato_tres
        self.fields['dato_cuatro'].label = sorteo.nombre_dato_cuatro
        if not sorteo.nombre_dato_tres:
            self.fields['dato_tres'].widget = forms.HiddenInput()
        if not sorteo.nombre_dato_cuatro:
            self.fields['dato_cuatro'].widget = forms.HiddenInput()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CargarExcelForm(BSModalForm):
    excel = forms.FileField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(CargarExcelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
