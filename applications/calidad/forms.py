from django import forms
from applications.nota_ingreso.models import NotaIngreso
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Unidad
from applications.material.funciones import stock, stock_disponible, stock_sede_disponible
from applications.variables import ESTADOS_NOTA_CALIDAD_STOCK
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import FallaMaterial, HistorialEstadoSerie, NotaControlCalidadStock, NotaControlCalidadStockDetalle, Serie, SerieCalidad, SolicitudConsumoInterno, Sede, Almacen, Material, SolicitudConsumoInternoDetalle, AprobacionConsumoInterno
from django.contrib.contenttypes.models import ContentType

class NotaControlCalidadStockBuscarForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    estado = forms.ChoiceField(choices=((None, '-----------------'),) + ESTADOS_NOTA_CALIDAD_STOCK, required=False)
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')
        super(NotaControlCalidadStockBuscarForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FallaMaterialForm(BSModalModelForm):
    class Meta:
        model = FallaMaterial
        fields=(
            'titulo',
            'comentario',
            'visible',
            )

    def __init__(self, *args, **kwargs):
        super(FallaMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['visible'].widget.attrs['class'] = 'form-check-input'

class NotaControlCalidadStockForm(BSModalModelForm):
    class Meta:
        model = NotaControlCalidadStock
        fields=(
            'nota_ingreso',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockForm, self).__init__(*args, **kwargs)
        self.fields['nota_ingreso'].queryset = NotaIngreso.objects.filter(estado=2)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockAnularForm(BSModalModelForm):
    class Meta:
        model = NotaControlCalidadStock
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockAnularForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockDetalleAgregarForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = NotaControlCalidadStockDetalle
        fields=(
            'material',
            'cantidad_calidad',
            'inspeccion',
            )
    
    def __init__(self, *args, **kwargs):
        lista_materiales = kwargs.pop('materiales')
        inspeccion = kwargs.pop('inspeccion')
        super(NotaControlCalidadStockDetalleAgregarForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        if inspeccion:
            self.fields['inspeccion'].choices = inspeccion
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    class Meta:
        model = NotaControlCalidadStockDetalle
        fields=(
            'material',
            'cantidad_calidad',
            'inspeccion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockDetalleUpdateForm, self).__init__(*args, **kwargs)
        self.fields['material'].initial = self.instance.material
        self.fields['material'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['material'].disabled = True

class NotaControlCalidadStockBuenoCreateForm(BSModalForm):
    serie_base = forms.CharField(max_length=200, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        fields=(
            'serie_base',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockBuenoCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaControlCalidadStockAgregarMaloCreateForm(BSModalForm):
    serie_base = forms.CharField(max_length=200, required=True)
    falla_material = forms.ModelChoiceField(queryset=None, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())
    class Meta:
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockAgregarMaloCreateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaControlCalidadStockAgregarMaloSinFallaCreateForm(BSModalForm):
    serie_base = forms.CharField(max_length=200, required=True)
    class Meta:
        fields=(
            'serie_base',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockAgregarMaloSinFallaCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaControlCalidadStockActualizarFallasCreateForm(BSModalForm):
    falla_material = forms.ModelChoiceField(queryset=None, required=True)
    class Meta:
        fields=(
            'falla_material',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockActualizarFallasCreateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockAgregarMaloSinSerieCreateForm(BSModalModelForm):
    serie_base = forms.CharField(max_length=200, required=True)
    falla_material = forms.ModelChoiceField(queryset=None, required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())
    class Meta:
        model = HistorialEstadoSerie
        fields=(
            'serie_base',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockAgregarMaloSinSerieCreateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockBuenoUpdateForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaControlCalidadStockBuenoUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockMaloUpdateForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockMaloUpdateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaControlCalidadStockMaloSinSerieUpdateForm(BSModalModelForm):
    class Meta:
        model = SerieCalidad
        fields=(
            'serie',
            'falla_material',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        falla_material = kwargs.pop('falla_material')
        super(NotaControlCalidadStockMaloSinSerieUpdateForm, self).__init__(*args, **kwargs)
        self.fields['falla_material'].queryset = falla_material
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SerieBuscarForm(BSModalForm):
    serie = forms.CharField(max_length=200, required=True)
    class Meta:
        fields=(
            'serie',
            )

    def __init__(self, *args, **kwargs):
        serie = kwargs.pop('serie')
        super(SerieBuscarForm, self).__init__(*args, **kwargs)
        self.fields['serie'].initial = serie
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SolicitudConsumoInternoForm(BSModalModelForm):
    class Meta:
        model = SolicitudConsumoInterno
        fields=(
            'sociedad',
            'fecha_solicitud',
            'solicitante',
            'fecha_consumo',
            'observacion',
            )
        widgets = {
            'fecha_solicitud' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            'fecha_consumo' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }    

    def __init__(self, *args, **kwargs):
        super(SolicitudConsumoInternoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SolicitudConsumoInternoDetalleForm(BSModalModelForm):
    sede = forms.ModelChoiceField(queryset=Sede.objects.filter(estado=1), required=False)
    unidad = forms.ModelChoiceField(queryset=Unidad.objects.all(), required=False, )
    stock = forms.DecimalField(required=False, initial=0, max_digits=22, decimal_places=10, disabled=True)
    # unidad = forms.CharField(required=False)
    class Meta:
        model = SolicitudConsumoInternoDetalle
        # fields = '__all__'
        fields=(
            'material',
            'unidad',
            'sede',
            'almacen',
            'stock',
            'cantidad',
            )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     cantidad = cleaned_data.get('cantidad')
    #     stock = cleaned_data.get('stock')
    #     if cantidad > stock:
    #         self.add_error('cantidad', 'Se ha sobrepasado la cantidad disponible')

    def clean_sede(self):
        sede = self.cleaned_data.get('sede')
        almacen = self.fields['almacen']
        almacen.queryset = Almacen.objects.filter(sede = sede)
        return sede
    
    def clean_material(self):
        material = self.cleaned_data.get('material')
        unidad = self.fields['unidad']
        unidad.queryset = Unidad.objects.filter(nombre = material.unidad_base.nombre)
        return material

    def __init__(self, *args, **kwargs):
        self.id_sociedad = kwargs.pop('id_sociedad')
        super(SolicitudConsumoInternoDetalleForm, self).__init__(*args, **kwargs)
        self.fields['almacen'].queryset = Almacen.objects.none()
        self.fields['unidad'].queryset = Unidad.objects.none()
        self.fields['unidad'].widget.attrs['readonly'] = True
        # self.fields['unidad'].widget.attrs['disabled'] = 'disabled'
        try:
            material = self.instance.material
            if material:
                unidad = material.unidad_base
                self.fields['unidad'].initial = unidad
                self.fields['unidad'].queryset = Unidad.objects.filter(nombre = material.unidad_base.nombre)
                self.fields['stock'].initial = stock_disponible(ContentType.objects.get_for_model(material), material.id, self.id_sociedad)
        except Exception as e:
            pass
        almacen = self.instance.almacen
        if almacen:
            sede = almacen.sede
            self.fields['sede'].initial = sede
            self.fields['almacen'].queryset = Almacen.objects.filter(sede = sede)
            self.fields['stock'].initial = stock_sede_disponible(ContentType.objects.get_for_model(material), material.id, self.id_sociedad, sede.id)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AprobacionConsumoInternoForm(BSModalModelForm):
    class Meta:
        model = AprobacionConsumoInterno
        fields = (
            'solicitud_consumo',
            'fecha_aprobacion',
            'responsable',
            'observacion',
            )
        widgets = {
            'fecha_aprobacion' : forms.DateInput(
                attrs = {
                    'type':'date',
                },
                format = '%Y-%m-%d',
                ),
        }    
    
    def __init__(self, *args, **kwargs):
        super(AprobacionConsumoInternoForm, self).__init__(*args, **kwargs)
        self.fields['solicitud_consumo'].queryset = SolicitudConsumoInterno.objects.filter(estado__in=[2,4,5,6])
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SolicitudConsumoInternoRechazarForm(BSModalModelForm):
    class Meta:
        model = SolicitudConsumoInterno
        fields = (
            'motivo_anulacion',
            # 'estado',
            )
    
    def __init__(self, *args, **kwargs):
        super(SolicitudConsumoInternoRechazarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SolicitudConsumoInternoDetalleSeriesForm(BSModalModelForm):
    cantidad_ingresada = forms.DecimalField(label='Cantidad Ingresada', max_digits=22, decimal_places=10, required=False)
    serie = forms.CharField(required=False)
    class Meta:
        model = SolicitudConsumoInternoDetalle
        fields=(
            'serie',
            'cantidad',
            'cantidad_ingresada',
            )

    def __init__(self, *args, **kwargs):
        cantidad = kwargs.pop('cantidad')
        cantidad_ingresada = kwargs.pop('cantidad_ingresada')
        super(SolicitudConsumoInternoDetalleSeriesForm, self).__init__(*args, **kwargs)
        self.fields['cantidad'].initial = cantidad
        self.fields['cantidad_ingresada'].initial = cantidad_ingresada
        if cantidad_ingresada == cantidad:
            self.fields['serie'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            self.fields['cantidad'].disabled = True
            self.fields['cantidad_ingresada'].disabled = True
            