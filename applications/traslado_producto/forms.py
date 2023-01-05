from django import forms
from django.contrib.auth import get_user_model
from applications.sede.models import Sede
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import EnvioTrasladoProducto, EnvioTrasladoProductoDetalle, MotivoTraslado, RecepcionTrasladoProducto, RecepcionTrasladoProductoDetalle 
from applications.material.models import Material


class MotivoTrasladoForm(BSModalModelForm):
    class Meta:
        model = MotivoTraslado
        fields=(
            'motivo_traslado',
            'visible',
            )

    def __init__(self, *args, **kwargs):
        super(MotivoTrasladoForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EnvioTrasladoProductoForm(BSModalModelForm):
    class Meta:
        model = EnvioTrasladoProducto
        fields=(
            'sociedad',
            'sede_origen',
            'direccion_destino',
            'responsable',
            'motivo_traslado',
            )
        widgets = {
            'fecha_traslado' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }
    
    def clean_sociedad(self):
        sociedad = self.cleaned_data.get('sociedad')
        sede_origen = self.fields['sede_origen']
        sede_origen.queryset = sociedad.Sede_sociedad.filter(estado=1)
        
        return sociedad

    def __init__(self, *args, **kwargs):
        super(EnvioTrasladoProductoForm, self).__init__(*args, **kwargs)  
        try:
            self.fields['sede_origen'].queryset = kwargs['instance'].sociedad.Sede_sociedad.filter(estado=1)
        except:
            self.fields['sede_origen'].queryset = Sede.objects.none()
        self.fields['motivo_traslado'].queryset = MotivoTraslado.objects.filter(visible=True)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EnvioTrasladoProductoObservacionesForm(BSModalModelForm):
    class Meta:
        model = EnvioTrasladoProducto
        fields=(
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(EnvioTrasladoProductoObservacionesForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EnvioTrasladoProductoMaterialDetalleForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad_envio = forms.DecimalField(max_digits=22, decimal_places=10)
    stock_disponible = forms.CharField(required=False)

    class Meta:
        model = EnvioTrasladoProductoDetalle
        fields=(
            'material',
            'almacen_origen',
            'tipo_stock',
            'cantidad_envio',
            'stock_disponible',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        envio_traslado_producto = kwargs.pop('envio_traslado_producto')
        super(EnvioTrasladoProductoMaterialDetalleForm, self).__init__(*args, **kwargs)   
        self.fields['almacen_origen'].queryset = envio_traslado_producto.sede_origen.Almacen_sede.filter(estado_alta_baja=1)
        self.fields['stock_disponible'].disabled = True
        self.fields['almacen_origen'].required = True
        self.fields['cantidad_envio'].required = True
        self.fields['unidad'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EnvioTrasladoProductoMaterialActualizarDetalleForm(BSModalModelForm):
    stock_disponible = forms.CharField(required=False)
    class Meta:
        model = EnvioTrasladoProductoDetalle
        fields=(
            'almacen_origen',
            'tipo_stock',
            'cantidad_envio',
            'stock_disponible',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        envio_traslado_producto = kwargs.pop('envio_traslado_producto')
        super(EnvioTrasladoProductoMaterialActualizarDetalleForm, self).__init__(*args, **kwargs)   
        self.fields['almacen_origen'].queryset = envio_traslado_producto.sede_origen.Almacen_sede.filter(estado_alta_baja=1)
        self.fields['unidad'].queryset = kwargs['instance'].producto.subfamilia.unidad.all()
        self.fields['almacen_origen'].required = True
        self.fields['tipo_stock'].required = True
        self.fields['cantidad_envio'].required = True
        self.fields['unidad'].required = True
        self.fields['stock_disponible'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EnvioTrasladoProductoDetalleSeriesForm(BSModalModelForm):
    cantidad_ingresada = forms.DecimalField(label='Cantidad Ingresada', max_digits=22, decimal_places=10, required=False)
    serie = forms.CharField(required=False)
    class Meta:
        model = EnvioTrasladoProductoDetalle
        fields=(
            'serie',
            'cantidad_envio',
            'cantidad_ingresada',
            )

    def __init__(self, *args, **kwargs):
        cantidad_envio = kwargs.pop('cantidad_envio')
        cantidad_ingresada = kwargs.pop('cantidad_ingresada')
        super(EnvioTrasladoProductoDetalleSeriesForm, self).__init__(*args, **kwargs)
        self.fields['cantidad_envio'].initial = cantidad_envio
        self.fields['cantidad_ingresada'].initial = cantidad_ingresada
        if cantidad_ingresada == cantidad_envio:
            self.fields['serie'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            self.fields['cantidad_envio'].disabled = True
            self.fields['cantidad_ingresada'].disabled = True


class RecepcionTrasladoProductoForm(BSModalModelForm):
    class Meta:
        model = RecepcionTrasladoProducto
        fields=(
            'envio_traslado_producto',
            'sede_destino',
            'fecha_recepcion',
            'responsable',
            )
        widgets = {
            'fecha_recepcion' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(RecepcionTrasladoProductoForm, self).__init__(*args, **kwargs)   
        self.fields['envio_traslado_producto'].queryset = EnvioTrasladoProducto.objects.filter(estado=2)
        self.fields['sede_destino'].queryset = Sede.objects.filter(estado=1)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RecepcionTrasladoProductoActualizarForm(BSModalModelForm):
    class Meta:
        model = RecepcionTrasladoProducto
        fields=(
            'sede_destino',
            'fecha_recepcion',
            'responsable',
            )
        widgets = {
            'fecha_recepcion' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(RecepcionTrasladoProductoActualizarForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RecepcionTrasladoProductoObservacionesForm(BSModalModelForm):
    class Meta:
        model = RecepcionTrasladoProducto
        fields=(
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(RecepcionTrasladoProductoObservacionesForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RecepcionTrasladoProductoMaterialDetalleForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=RecepcionTrasladoProductoDetalle.objects.all())
    stock_disponible = forms.CharField(required=False)

    class Meta:
        model = RecepcionTrasladoProductoDetalle
        fields=(
            'material',
            'almacen_destino',
            'stock_disponible',
            )

    def __init__(self, *args, **kwargs):
        recepcion_traslado_producto = kwargs.pop('recepcion_traslado_producto')
        lista_materiales = kwargs.pop('lista_materiales')
        super(RecepcionTrasladoProductoMaterialDetalleForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        self.fields['almacen_destino'].queryset = recepcion_traslado_producto.sede_destino.Almacen_sede.filter(estado_alta_baja=1)
        self.fields['stock_disponible'].disabled = True
        self.fields['almacen_destino'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RecepcionTrasladoProductoMaterialActualizarDetalleForm(BSModalModelForm):
    stock_disponible = forms.CharField(required=False)
    class Meta:
        model = RecepcionTrasladoProductoDetalle
        fields=(
            'almacen_destino',
            'stock_disponible',
            )

    def __init__(self, *args, **kwargs):
        recepcion_traslado_producto = kwargs.pop('recepcion_traslado_producto')
        super(RecepcionTrasladoProductoMaterialActualizarDetalleForm, self).__init__(*args, **kwargs)   
        self.fields['almacen_destino'].queryset = recepcion_traslado_producto.sede_destino.Almacen_sede.filter(estado_alta_baja=1)
        self.fields['almacen_destino'].required = True
        self.fields['stock_disponible'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class MotivoTrasladoForm(BSModalModelForm):
    class Meta:
        model = MotivoTraslado
        fields = (
            'motivo_traslado',
            'visible',
            )
        
    def __init__(self, *args, **kwargs):
        super(MotivoTrasladoForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['visible'].widget.attrs['class'] = 'form-check-input'