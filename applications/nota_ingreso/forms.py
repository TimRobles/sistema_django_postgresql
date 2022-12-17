from django import forms
from django.contrib.auth import get_user_model
from applications.almacenes.models import Almacen
from applications.nota_ingreso.models import NotaIngreso, NotaStockInicial
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.contrib.contenttypes.models import ContentType

class NotaIngresoAgregarMaterialForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.IntegerField()
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.none())
    class Meta:
        fields=(
            'producto',
            'cantidad',
            'almacen',
            )
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        almacenes = kwargs.pop('almacenes')
        try:
            nota_ingreso_detalle = kwargs.pop('nota_ingreso_detalle')
        except:
            pass
        super(NotaIngresoAgregarMaterialForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        self.fields['almacen'].queryset = almacenes
        try:
            detalle = nota_ingreso_detalle.comprobante_compra_detalle
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            self.fields['producto'].initial = valor
            self.fields['cantidad'].initial = nota_ingreso_detalle.cantidad_conteo
            self.fields['almacen'].initial = nota_ingreso_detalle.almacen
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoFinalizarConteoForm(BSModalModelForm):    
    class Meta:
        model = NotaIngreso
        fields = (
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoFinalizarConteoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoAnularConteoForm(BSModalModelForm):    
    class Meta:
        model = NotaIngreso
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoAnularConteoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


##########################################

class NotaStockInicialAgregarMaterialForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.IntegerField()
    class Meta:
        fields=(
            'producto',
            'cantidad',
            )
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        try:
            nota_stock_inicial_detalle = kwargs.pop('nota_stock_inicial_detalle')
        except:
            pass
        super(NotaStockInicialAgregarMaterialForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        try:
            valor = "%s|%s" % (nota_stock_inicial_detalle.content_type.id, nota_stock_inicial_detalle.id_registro)
            self.fields['producto'].initial = valor
            self.fields['cantidad'].initial = nota_stock_inicial_detalle.cantidad_total
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaStockInicialGuardarForm(BSModalModelForm):    
    class Meta:
        model = NotaStockInicial
        fields = (
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(NotaStockInicialGuardarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaStockInicialAnularForm(BSModalModelForm):    
    class Meta:
        model = NotaStockInicial
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaStockInicialAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaStockInicialForm(BSModalModelForm):    
    class Meta:
        model = NotaStockInicial
        fields = (
            'sociedad',
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
        super(NotaStockInicialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaStockInicialGenerarNotaIngresoForm(BSModalForm):
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
        super(NotaStockInicialGenerarNotaIngresoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'