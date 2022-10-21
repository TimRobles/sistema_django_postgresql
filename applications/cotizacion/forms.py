from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from applications.cobranza.models import SolicitudCredito, SolicitudCreditoCuota
from applications.datos_globales.models import Moneda
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.cotizacion.models import ConfirmacionOrdenCompra, ConfirmacionVenta, ConfirmacionVentaCuota, CotizacionDescuentoGlobal, CotizacionObservacion, CotizacionOtrosCargos, CotizacionVenta, CotizacionVentaDetalle, PrecioListaMaterial
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.material.models import Material

class CotizacionVentaForm (BSModalForm):
    class Meta:
        model = CotizacionVenta
        fields = (
            'numero_cotizacion',
            'fecha_cotizacion',
        )

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CotizacionVentaClienteForm(BSModalModelForm):
    class Meta:
        model = CotizacionVenta
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
        super(CotizacionVentaClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente_interlocutor'].queryset = interlocutor_queryset
        self.fields['cliente_interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CotizacionVentaDescuentoGlobalForm(BSModalModelForm):
    class Meta:
        model = CotizacionDescuentoGlobal
        fields = ()

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaDescuentoGlobalForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CotizacionVentaObservacionForm(BSModalModelForm):
    class Meta:
        model = CotizacionObservacion
        fields = ()

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaObservacionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CotizacionVentaOtrosCargosForm(BSModalModelForm):
    class Meta:
        model = CotizacionOtrosCargos
        fields = ()

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaOtrosCargosForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CotizacionVentaMaterialDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    precio_lista = forms.DecimalField(max_digits=22, decimal_places=10, required=False, disabled=True)
    stock = forms.DecimalField(max_digits=22, decimal_places=10, required=False, disabled=True)
    class Meta:
        model = CotizacionVentaDetalle
        fields=(
            'material',
            'cantidad',
            'precio_lista',
            'stock',
            )

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaMaterialDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0


class CotizacionVentaMaterialDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = CotizacionVentaDetalle
        fields=(
            'tipo_igv',
            'cantidad',
            'precio_final_con_igv',
            'tiempo_entrega',
            )

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaMaterialDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        

        
class CotizacionVentaDetalleForm(BSModalModelForm):
    cantidad = forms.DecimalField(required=False, disabled=True)
    class Meta:
        model = CotizacionVentaDetalle
        fields = (
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control text-end'


class PrecioListaMaterialForm (BSModalModelForm):
    comprobante = forms.ChoiceField(choices=[(0,0)], required=False)
    class Meta:
        model = PrecioListaMaterial
        fields = (
            'comprobante',
            'moneda',
            'precio_compra',
            'logistico',
            'margen_venta',
            'precio_lista',
            'precio_sin_igv',
        )

    def __init__(self, *args, **kwargs):
        precios = kwargs.pop('precios')
        super(PrecioListaMaterialForm, self).__init__(*args, **kwargs)
        self.fields['comprobante'].choices = precios
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['precio_compra'].widget.attrs['min'] = 0
        self.fields['logistico'].widget.attrs['min'] = 0
        self.fields['margen_venta'].widget.attrs['min'] = 0
        self.fields['precio_lista'].widget.attrs['min'] = 0
        self.fields['precio_sin_igv'].widget.attrs['min'] = 0

class CotizacionVentaPdfsForm(BSModalForm):
    pass

    # TODO: Define form fields here


class ConfirmacionVentaFormaPagoForm(BSModalModelForm):
    class Meta:
        model = ConfirmacionVenta
        fields = (
            'tipo_venta',
            'condiciones_pago',
            )

    def __init__(self, *args, **kwargs):
        super(ConfirmacionVentaFormaPagoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ConfirmacionClienteForm(BSModalModelForm):
    class Meta:
        model = ConfirmacionVenta
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
        super(ConfirmacionClienteForm, self).__init__(*args, **kwargs)
        self.fields['cliente_interlocutor'].queryset = interlocutor_queryset
        self.fields['cliente_interlocutor'].initial = interlocutor
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SolicitudCreditoForm(BSModalModelForm):
    class Meta:
        model = SolicitudCredito
        fields = (
            'total_credito',
            'condiciones_pago',
            'interlocutor_solicita',
            )

    def clean_total_credito(self):
        total_credito = self.cleaned_data.get('total_credito')
        if total_credito == 0:
            self.add_error('total_credito', 'Ingrese un monto.')
        if total_credito > self.instance.total_cotizado:
            self.add_error('total_credito', 'El monto solicitado no puede ser mayor al monto cotizado.')
    
        return total_credito

    def __init__(self, *args, **kwargs):
        super(SolicitudCreditoForm, self).__init__(*args, **kwargs)
        lista_interlocutor = []
        for tabla in self.instance.cotizacion_venta.cliente.ClienteInterlocutor_cliente.all():
            lista_interlocutor.append(tabla.interlocutor.id)
        interlocutores = InterlocutorCliente.objects.filter(id__in=lista_interlocutor)
        self.fields['interlocutor_solicita'].queryset = interlocutores
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True


class SolicitudCreditoCuotaForm(BSModalModelForm):
    class Meta:
        model = SolicitudCreditoCuota
        fields = (
            'monto',
            'dias_pago',
            'fecha_pago',
            )
        widgets = {
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudCreditoCuotaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['monto'].widget.attrs['min'] = 0
        self.fields['dias_pago'].widget.attrs['min'] = 0


class ConfirmacionVentaCuotaForm(BSModalModelForm):
    class Meta:
        model = ConfirmacionVentaCuota
        fields = (
            'monto',
            'dias_pago',
            'fecha_pago',
            )
        widgets = {
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(ConfirmacionVentaCuotaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['monto'].widget.attrs['min'] = 0
        self.fields['dias_pago'].widget.attrs['min'] = 0


class ConfirmacionOrdenCompraForm(BSModalModelForm):
    class Meta:
        model = ConfirmacionOrdenCompra
        fields = (
            'numero_orden',
            'fecha_orden',
            'documento',
            )
        widgets = {
            'fecha_orden' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(ConfirmacionOrdenCompraForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            
class CosteadorForm (BSModalModelForm):
    comprobante = forms.ChoiceField(choices=[(0,0)], required=False)
    moneda = forms.ModelChoiceField(queryset=Moneda.objects.filter(estado=1))
    precio_compra = forms.DecimalField()
    logistico = forms.DecimalField()
    margen_venta = forms.DecimalField()
    precio_final = forms.DecimalField()
    precio_sin_igv = forms.DecimalField()
    class Meta:
        model = CotizacionVentaDetalle
        fields = (
            'comprobante',
            'moneda',
            'precio_compra',
            'logistico',
            'margen_venta',
            'precio_sin_igv',
            'precio_final',
        )
    
    def __init__(self, *args, **kwargs):
        precios = kwargs.pop('precios')
        precio_final = kwargs.pop('precio_final')
        super(CosteadorForm, self).__init__(*args, **kwargs)
        self.fields['comprobante'].choices = precios
        self.fields['precio_final'].initial = precio_final
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
