from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class RequerimientoForm(BSModalModelForm):
    class Meta:
        model = Requerimiento
        fields = (
            'fecha', 
            'monto', 
            'moneda', 
            'concepto', 
            'usuario_pedido',
            )

        widgets = {
            'fecha' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(RequerimientoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['usuario_pedido'].required = True


class RequerimientoAprobarForm(BSModalModelForm):
    class Meta:
        model = Requerimiento
        fields = (
            'concepto_final',
            'fecha_entrega',
            'monto_final',
            'moneda',
            'content_type',
            'id_registro',
            'tipo_cambio',
            )

        widgets = {
            'fecha_entrega': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field',
                }
            ),
        }

    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        
        if self.fecha > fecha_entrega:
            self.add_error('fecha_entrega', 'La fecha de entrega no puede ser menor a la fecha de solicitud.')
    
        return fecha_entrega

    def __init__(self, *args, **kwargs):
        moneda = kwargs.pop('moneda')
        self.fecha = kwargs.pop('fecha')
        super(RequerimientoAprobarForm, self).__init__(*args, **kwargs)
        self.fields['moneda'].initial = moneda
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        # for field in self.fields:
        #     self.fields[field].required = True
        
        self.fields['moneda'].disabled = True
        self.fields['monto_final'].required = False
        self.fields['fecha_entrega'].required = False


class RequerimientoRechazarForm(BSModalModelForm):
    class Meta:
        model = Requerimiento
        fields = (
            'motivo_rechazo',
            'dato_rechazado',
            )

    def __init__(self, *args, **kwargs):
        super(RequerimientoRechazarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True


class RequerimientoRechazarRendicionForm(BSModalModelForm):
    class Meta:
        model = Requerimiento
        fields = (
            'rechazo_rendicion',
            )

    def __init__(self, *args, **kwargs):
        super(RequerimientoRechazarRendicionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True


class RequerimientoDocumentoForm(BSModalModelForm):
    moneda_requerimiento = forms.ModelChoiceField(queryset=Moneda.objects.all())
    class Meta:
        model = RequerimientoDocumento
        fields = (
            'fecha', 
            'tipo', 
            'numero', 
            'establecimiento', 
            'moneda', 
            'total_documento', 
            'moneda_requerimiento', 
            'tipo_cambio', 
            'total_requerimiento', 
            'voucher',
            'sociedad',
            )

        widgets = {
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        moneda_requerimiento = kwargs.pop('moneda_requerimiento')
        tipo_cambio = kwargs.pop('tipo_cambio')
        super(RequerimientoDocumentoForm, self).__init__(*args, **kwargs)
        self.fields['moneda_requerimiento'].initial = moneda_requerimiento
        if tipo_cambio:
            self.fields['tipo_cambio'].initial = tipo_cambio

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True
        self.fields['establecimiento'].required = False
        self.fields['voucher'].required = False
        self.fields['tipo_cambio'].required = False
        self.fields['total_requerimiento'].required = False
        self.fields['moneda_requerimiento'].disabled = True


class RequerimientoDocumentoDetalleForm(BSModalModelForm):
    class Meta:
        model = RequerimientoDocumentoDetalle
        exclude = (
            'item', 
            'documento_requerimiento',
            )

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto')
        cantidad = kwargs.pop('cantidad')
        unidad = kwargs.pop('unidad')
        precio_unitario = kwargs.pop('precio_unitario')
        foto = kwargs.pop('foto')
        super(RequerimientoDocumentoDetalleForm, self).__init__(*args, **kwargs)
        if producto : self.fields['producto'].initial = producto
        if cantidad : self.fields['cantidad'].initial = cantidad
        if unidad : self.fields['unidad'].initial = unidad
        if precio_unitario : self.fields['precio_unitario'].initial = precio_unitario
        if foto : self.fields['foto'].initial = foto
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True
        self.fields['foto'].required = False