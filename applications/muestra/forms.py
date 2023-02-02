from django import forms
from applications.almacenes.models import Almacen
from applications.muestra.models import DevolucionMuestra, DevolucionMuestraDetalle, NotaIngresoMuestra, NotaIngresoMuestraDetalle
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class NotaIngresoMuestraAgregarMaterialForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.all())
    class Meta:
        fields=(
            'producto',
            'cantidad',
            'almacen',
            )
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        try:
            nota_ingreso_muestra_detalle = kwargs.pop('nota_ingreso_muestra_detalle')
        except:
            pass
        super(NotaIngresoMuestraAgregarMaterialForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        try:
            valor = "%s|%s" % (nota_ingreso_muestra_detalle.content_type.id, nota_ingreso_muestra_detalle.id_registro)
            self.fields['producto'].initial = valor
            self.fields['cantidad'].initial = nota_ingreso_muestra_detalle.cantidad_total
            self.fields['almacen'].initial = nota_ingreso_muestra_detalle.almacen
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraGuardarForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMuestra
        fields = (
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraGuardarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraAnularForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMuestra
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMuestra
        fields = (
            'sociedad',
            'proveedor',
            'fecha_ingreso',
            )
        widgets = {
            'fecha_ingreso' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoMuestraGenerarNotaIngresoForm(BSModalForm):
    fecha_ingreso = forms.DateField(
        widget=forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    class Meta:
        fields=(
            'fecha_ingreso',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoMuestraGenerarNotaIngresoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DevolucionMuestraAgregarMaterialForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.all())
    stock_disponible = forms.CharField(required=False)
    class Meta:
        fields=(
            'producto',
            'almacen',
            'cantidad',
            'stock_disponible',
            )
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        try:
            devolucion_muestra_detalle = kwargs.pop('devolucion_muestra_detalle')
        except:
            pass
        super(DevolucionMuestraAgregarMaterialForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        try:
            valor = "%s|%s" % (devolucion_muestra_detalle.content_type.id, devolucion_muestra_detalle.id_registro)
            self.fields['producto'].initial = valor
            self.fields['cantidad'].initial = devolucion_muestra_detalle.cantidad_devolucion
            self.fields['almacen'].initial = devolucion_muestra_detalle.almacen
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['stock_disponible'].disabled = True


class DevolucionMuestraGuardarForm(BSModalModelForm):    
    class Meta:
        model = DevolucionMuestra
        fields = (
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(DevolucionMuestraGuardarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DevolucionMuestraAnularForm(BSModalModelForm):    
    class Meta:
        model = DevolucionMuestra
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(DevolucionMuestraAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DevolucionMuestraForm(BSModalModelForm):    
    class Meta:
        model = DevolucionMuestra
        fields = (
            'sociedad',
            'sede',
            'proveedor',
            'fecha_devolucion',
            )
        widgets = {
            'fecha_devolucion' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(DevolucionMuestraForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DevolucionMuestraDetalleSeriesForm(BSModalModelForm):
    cantidad_ingresada = forms.DecimalField(label='Cantidad Ingresada', max_digits=22, decimal_places=10, required=False)
    serie = forms.CharField(required=False)
    class Meta:
        model = DevolucionMuestraDetalle
        fields=(
            'serie',
            'cantidad_devolucion',
            'cantidad_ingresada',
            )

    def __init__(self, *args, **kwargs):
        cantidad_devolucion = kwargs.pop('cantidad_devolucion')
        cantidad_ingresada = kwargs.pop('cantidad_ingresada')
        super(DevolucionMuestraDetalleSeriesForm, self).__init__(*args, **kwargs)
        self.fields['cantidad_devolucion'].initial = cantidad_devolucion
        self.fields['cantidad_ingresada'].initial = cantidad_ingresada
        if cantidad_ingresada == cantidad_devolucion:
            self.fields['serie'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            self.fields['cantidad_devolucion'].disabled = True
            self.fields['cantidad_ingresada'].disabled = True