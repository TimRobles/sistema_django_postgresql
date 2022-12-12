from django import forms
from django.contrib.auth import get_user_model
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

    def __init__(self, *args, **kwargs):
        super(EnvioTrasladoProductoForm, self).__init__(*args, **kwargs)   
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

    class Meta:
        model = EnvioTrasladoProductoDetalle
        fields=(
            'material',
            'cantidad_envio',
            'almacen_origen',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        
        super(EnvioTrasladoProductoMaterialDetalleForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EnvioTrasladoProductoMaterialActualizarDetalleForm(BSModalModelForm):
    class Meta:
        model = EnvioTrasladoProductoDetalle
        fields=(
            'cantidad_envio',
            'almacen_origen',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        super(EnvioTrasladoProductoMaterialActualizarDetalleForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class RecepcionTrasladoProductoForm(BSModalModelForm):
    class Meta:
        model = RecepcionTrasladoProducto
        fields=(
            'numero_recepcion_traslado',
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
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad_recepcion = forms.DecimalField(max_digits=22, decimal_places=10)

    class Meta:
        model = RecepcionTrasladoProductoDetalle
        fields=(
            'material',
            'cantidad_recepcion',
            'almacen_destino',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        
        super(RecepcionTrasladoProductoMaterialDetalleForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RecepcionTrasladoProductoMaterialActualizarDetalleForm(BSModalModelForm):
    class Meta:
        model = RecepcionTrasladoProductoDetalle
        fields=(
            'cantidad_recepcion',
            'almacen_destino',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        super(RecepcionTrasladoProductoMaterialActualizarDetalleForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


