from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.cotizacion.models import CotizacionDescuentoGlobal, CotizacionObservacion, CotizacionVenta, CotizacionVentaDetalle, PrecioListaMaterial
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


class CotizacionVentaMaterialDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = CotizacionVentaDetalle
        fields=(
            'tipo_igv',
            'cantidad',
            'precio_final_con_igv',
            )

    def __init__(self, *args, **kwargs):
        super(CotizacionVentaMaterialDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        

        
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

class CotizacionVentaPdfsForm(BSModalForm):
    pass

    # TODO: Define form fields here
