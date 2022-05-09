from django import forms
from django.db.models import Max

from applications.programas.models import NivelUno

class NivelUnoForm(forms.ModelForm):
    class Meta:
        model = NivelUno
        fields = (
            'orden',
            'nombre',
            'icono',
            )
    
    def __init__(self, *args, **kwargs):
        max_orden = NivelUno.objects.aggregate(Max('orden'))['orden__max']
        if max_orden == None:
            max_orden = 0
        super(NivelUnoForm, self).__init__(*args, **kwargs)
        self.fields['orden'].initial = max_orden + 1
        
    