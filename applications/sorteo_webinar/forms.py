from django import forms

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class CargarExcelForm(BSModalForm):
    excel = forms.FileField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(CargarExcelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
