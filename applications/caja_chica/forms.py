from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.contabilidad.models import ReciboServicio
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
        usuario_pedido = kwargs.pop('usuario_pedido')
        super(RequerimientoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['usuario_pedido'].required = True
        self.fields['usuario_pedido'].queryset = usuario_pedido


class RequerimientoAprobarForm(BSModalModelForm):
    caja_cheque = forms.ChoiceField(label='Caja o Cheque', choices=[('0|0', '--------------------')], required=True)
    monto_entregado = forms.DecimalField(required=False)
    class Meta:
        model = Requerimiento
        fields = (
            'caja_cheque',
            'concepto_final',
            'fecha_entrega',
            'monto_final',
            'moneda',
            'tipo_cambio',
            'monto_entregado',
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

    def clean_caja_cheque(self):
        caja_cheque = self.cleaned_data.get('caja_cheque')
        
        if caja_cheque == '0|0':
            self.add_error('caja_cheque', 'Debe elegir una caja o un cheque.')
    
        return caja_cheque

    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        
        if self.fecha > fecha_entrega:
            self.add_error('fecha_entrega', 'La fecha de entrega no puede ser menor a la fecha de solicitud.')
    
        return fecha_entrega

    def __init__(self, *args, **kwargs):
        moneda = kwargs.pop('moneda')
        self.fecha = kwargs.pop('fecha')
        caja = kwargs.pop('caja')
        cheque = kwargs.pop('cheque')
        super(RequerimientoAprobarForm, self).__init__(*args, **kwargs)
        self.fields['moneda'].initial = moneda
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        self.fields['moneda'].disabled = True
        self.fields['monto_final'].required = True
        self.fields['fecha_entrega'].required = True
        self.fields['caja_cheque'].choices = [('0|0', '--------------------'),] + caja + cheque


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


class RequerimientoFinalizarRendicionForm(BSModalModelForm):
    vuelto_extra = forms.DecimalField(required=False)
    utilizado = forms.DecimalField(required=False)
    class Meta:
        model = Requerimiento
        fields = (
            'monto_final',
            'utilizado',
            'redondeo',
            'vuelto_extra',
            'vuelto',
            )

    def __init__(self, *args, **kwargs):
        utilizado = kwargs.pop('utilizado')
        vuelto_extra = kwargs.pop('vuelto_extra')
        super(RequerimientoFinalizarRendicionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True
        self.fields['utilizado'].initial = utilizado
        self.fields['vuelto_extra'].initial = vuelto_extra
        self.fields['redondeo'].widget.attrs['max'] = '0.1'
        self.fields['redondeo'].widget.attrs['min'] = '-0.1'


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


class RequerimientoVueltoExtraForm(BSModalModelForm):
    moneda_requerimiento = forms.ModelChoiceField(queryset=Moneda.objects.all())
    class Meta:
        model = RequerimientoVueltoExtra
        fields = (
            'vuelto_original', 
            'moneda', 
            'tipo_cambio', 
            'vuelto_extra', 
            'moneda_requerimiento', 
            )

    def __init__(self, *args, **kwargs):
        moneda_requerimiento = kwargs.pop('moneda_requerimiento')
        super(RequerimientoVueltoExtraForm, self).__init__(*args, **kwargs)
        self.fields['moneda_requerimiento'].initial = moneda_requerimiento
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
        print('///////////////////////////////////////////')
        print(tipo_cambio)
        if tipo_cambio:
            self.fields['tipo_cambio'].initial = tipo_cambio
            try:
                self.instance.tipo_cambio = tipo_cambio
            except:
                pass
        print('///////////////////////////////////////////')

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True
        self.fields['numero'].required = False
        self.fields['establecimiento'].required = False
        self.fields['voucher'].required = False
        self.fields['tipo_cambio'].required = False
        self.fields['total_requerimiento'].required = False
        self.fields['sociedad'].required = False
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


class CajaChicaCrearForm(BSModalModelForm):
    class Meta:
        model = CajaChica
        fields = (
            'month', 
            'year', 
            'saldo_inicial', 
            'moneda', 
            'saldo_inicial_caja_chica', 
            )

    def __init__(self, *args, **kwargs):
        caja_chicas = kwargs.pop('caja_chicas')
        super(CajaChicaCrearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['month'].required = True
        self.fields['year'].required = True
        self.fields['saldo_inicial_caja_chica'].required = False
        self.fields['saldo_inicial_caja_chica'].queryset = caja_chicas


class CajaChicaPrestamoCrearForm(BSModalModelForm):
    class Meta:
        model = CajaChicaPrestamo
        fields = (
            'fecha', 
            'caja_origen',
            'caja_destino',
            'monto',
            'tipo',
            'devolucion',
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
        super(CajaChicaPrestamoCrearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['devolucion'].required = False



class ReciboCajaChicaCrearForm(BSModalModelForm):
    class Meta:
        model = ReciboCajaChica
        fields = (
            'concepto',
            'fecha',
            'monto',
            'moneda',
            'caja_chica',
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
        caja_chica = kwargs.pop('caja_chica')
        super(ReciboCajaChicaCrearForm, self).__init__(*args, **kwargs)
        self.fields['caja_chica'].queryset = caja_chica
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




class CajaChicaReciboCrearForm(BSModalModelForm):
    class Meta:
        model = ReciboCajaChica
        fields = (
            'concepto',
            'fecha',
            'monto',
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
        super(CajaChicaReciboCrearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CajaChicaReciboServicioAgregarForm(BSModalForm):
    recibo_servicio = forms.ModelChoiceField(queryset=None)

    class Meta:
        fields=(
            'recibo_servicio',
            )

    def __init__(self, *args, **kwargs):
        lista_recibos = kwargs.pop('recibos')
        super(CajaChicaReciboServicioAgregarForm, self).__init__(*args, **kwargs)
        self.fields['recibo_servicio'].queryset = lista_recibos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CajaChicaReciboServicioUpdateForm(BSModalModelForm):
    class Meta:
        model = ReciboServicio
        fields = (
            'monto_pagado',
            'fecha_pago',
            'voucher',
            )

        widgets = {
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    # 'required':'required',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(CajaChicaReciboServicioUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

