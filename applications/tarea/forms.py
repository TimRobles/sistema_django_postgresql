from django import forms
from django.contrib.auth import get_user_model
from .models import TipoTarea, Tarea, HistorialComentarioTarea
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente


class TipoTareaForm(BSModalModelForm):
    class Meta:
        model = TipoTarea
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(TipoTareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class TareaForm(BSModalModelForm):
    class Meta:
        model = Tarea
        fields=(
            'tipo_tarea',
            'fecha_inicio',
            'fecha_limite',
            'area',
            'encargado',
            'apoyo',
            'prioridad',
            )
        
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            
            'fecha_limite' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
                
            }


    def __init__(self, *args, **kwargs):
        super(TareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
        self.fields['apoyo'].widget.attrs['class'] = 'form-check'

class TareaDescripcionForm(BSModalModelForm):
    class Meta:
        model = Tarea
        fields=(
            'descripcion',
            )

    def __init__(self, *args, **kwargs):
        super(TareaDescripcionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class HistorialComentarioTareaForm(BSModalModelForm):
    class Meta:
        model = HistorialComentarioTarea
        fields=(
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(HistorialComentarioTareaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TareaClienteForm(BSModalModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    cliente_interlocutor = forms.ModelChoiceField(queryset=ClienteInterlocutor.objects.all(), required=False)
    class Meta:
        model = Tarea
        fields = (
            'cliente',
            'cliente_interlocutor',
            )

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if cliente:
            cliente_interlocutor = self.fields['cliente_interlocutor']
            lista = []
            relaciones = ClienteInterlocutor.objects.filter(cliente = cliente.id)
            for relacion in relaciones:
                lista.append(relacion.interlocutor.id)

            cliente_interlocutor.queryset = InterlocutorCliente.objects.filter(id__in = lista)

        return cliente

    def __init__(self, *args, **kwargs):
        interlocutor_queryset = kwargs.pop('interlocutor_queryset')
        interlocutor = kwargs.pop('interlocutor')
        super(TareaClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente_interlocutor'].queryset = interlocutor_queryset
        self.fields['cliente_interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
