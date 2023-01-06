from applications.clientes.models import Cliente
from applications.material.funciones import stock, stock_disponible, stock_sede_disponible
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS_NOTA_CALIDAD_STOCK
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.logistica.models import Despacho, DocumentoPrestamoMateriales, NotaSalida, NotaSalidaDetalle, SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle
from applications.sede.models import Sede
from django import forms
from django.contrib.contenttypes.models import ContentType

from applications.material.models import Material
from applications.almacenes.models import Almacen

class SolicitudPrestamoMaterialesForm(BSModalModelForm):
    class Meta:
        model = SolicitudPrestamoMateriales
        fields = (
            'sociedad',
            'cliente',
            'interlocutor_cliente',
            'fecha_prestamo',
            'comentario',
            )

        widgets = {
            'fecha_prestamo' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudPrestamoMaterialesDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    stock = forms.IntegerField(required=False, initial=0, disabled=True)
    cantidad_prestamo = forms.DecimalField(label = 'Cantidad Prestamo', max_digits=22, decimal_places=10)
    observacion = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        fields = (
            'material',
            'stock',
            'cantidad_prestamo',
            'observacion',
            )

    def clean_cantidad_prestamo(self):
        cantidad_prestamo = self.cleaned_data.get('cantidad_prestamo')
        material = self.cleaned_data.get('material')
        stock_valor = stock(ContentType.objects.get_for_model(material), material.id, self.id_sociedad)
        if stock_valor < cantidad_prestamo:
            self.add_error('cantidad_prestamo', 'La cantidad prestada no puede ser mayor al stock disponible.')
    
        return cantidad_prestamo

    def __init__(self, *args, **kwargs):
        self.id_sociedad = kwargs.pop('id_sociedad')
        super(SolicitudPrestamoMaterialesDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad_prestamo'].widget.attrs['min']=0

class SolicitudPrestamoMaterialesDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    stock = forms.IntegerField(required=False, initial=0, disabled=True)
    class Meta:
        model = SolicitudPrestamoMaterialesDetalle
        fields=(
            'material',
            'stock',
            'cantidad_prestamo',
            'observacion',
            )

    def clean_cantidad_prestamo(self):
        cantidad_prestamo = self.cleaned_data.get('cantidad_prestamo')
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        
        if busqueda_material.stock < cantidad_prestamo:
            self.add_error('cantidad_prestamo', 'La cantidad prestada no puede ser mayor al stock disponible.')
    
        return cantidad_prestamo

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        self.fields['material'].initial = busqueda_material.descripcion_venta
        self.fields['stock'].initial = busqueda_material.stock
        self.fields['material'].disabled = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudPrestamoMaterialesAnularForm(BSModalModelForm):
    class Meta:
        model = SolicitudPrestamoMateriales
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DocumentoPrestamoMaterialesForm(BSModalModelForm):
    class Meta:
        model = DocumentoPrestamoMateriales
        fields=(
            'comentario',
            'documento',
            )

    def __init__(self, *args, **kwargs):
        super(DocumentoPrestamoMaterialesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaForm(BSModalModelForm):
    class Meta:
        model = NotaSalida
        fields = (
            'observacion_adicional',
            )

    def __init__(self, *args, **kwargs):
        super(NotaSalidaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaDetalleForm(BSModalModelForm): 
    material = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = NotaSalidaDetalle
        fields=(
            'material',
            )

    def __init__(self, *args, **kwargs):
        lista_materiales = kwargs.pop('materiales')
        super(NotaSalidaDetalleForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaDetalleUpdateForm(BSModalModelForm):
    cantidad_prestamo = forms.DecimalField(label='Cantidad Prestamo', max_digits=22, decimal_places=10)
    stock = forms.DecimalField(required=False, initial=0, max_digits=22, decimal_places=10, disabled=True)
    class Meta:
        model = NotaSalidaDetalle
        fields = (
            'sede',
            'almacen',
            'stock',
            'cantidad_prestamo',
            'cantidad_salida',
            )
    
    def clean(self):
        cleaned_data = super().clean()
        cantidad_salida = cleaned_data.get('cantidad_salida')
        cantidad_prestamo = cleaned_data.get('cantidad_prestamo')
        suma = self.suma
        valor_max = cantidad_prestamo - suma

        if cantidad_salida > valor_max:
            self.add_error('cantidad_salida', 'Se ha sobrepasado la cantidad de prestamo')

    def clean_sede(self):
        sede = self.cleaned_data.get('sede')
        almacen = self.fields['almacen']
        almacen.queryset = Almacen.objects.filter(sede = sede)    
        return sede
   
    def __init__(self, *args, **kwargs):
        self.solicitud = kwargs.pop('solicitud')
        self.suma = kwargs.pop('suma')
        self.id_sociedad = kwargs.pop('id_sociedad')
        super(NotaSalidaDetalleUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.solicitud_prestamo_materiales_detalle:
            material = self.instance.solicitud_prestamo_materiales_detalle.producto
            self.fields['cantidad_prestamo'].initial = self.solicitud.cantidad_prestamo
        else:
            material = self.instance.confirmacion_venta_detalle.producto
            self.fields['cantidad_prestamo'].initial = self.solicitud.cantidad_confirmada
            self.fields['cantidad_prestamo'].label = 'Cantidad Confirmada'
        self.fields['almacen'].queryset = Almacen.objects.none()
        self.fields['sede'].required = True
        self.fields['sede'].queryset = Sede.objects.filter(estado=1)
        self.fields['almacen'].required = True
        self.fields['stock'].initial = stock_disponible(ContentType.objects.get_for_model(material), material.id, self.id_sociedad)
        self.fields['cantidad_salida'].required = True
        self.fields['cantidad_salida'].widget.attrs['min'] = 0
        self.fields['cantidad_prestamo'].disabled = True
        try:
            almacen = self.instance.almacen
            sede = almacen.sede
            self.fields['sede'].initial = sede
            self.fields['almacen'].queryset = Almacen.objects.filter(sede = sede)
            self.fields['stock'].initial = stock_sede_disponible(ContentType.objects.get_for_model(material), material.id, self.id_sociedad, sede.id)
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaAnularForm(BSModalModelForm):
    class Meta:
        model = NotaSalida
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaSalidaAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NotaSalidaDetalleSeriesForm(BSModalModelForm):
    cantidad_ingresada = forms.DecimalField(label='Cantidad Ingresada', max_digits=22, decimal_places=10, required=False)
    serie = forms.CharField(required=False)
    class Meta:
        model = NotaSalidaDetalle
        fields=(
            'serie',
            'cantidad_salida',
            'cantidad_ingresada',
            )

    def __init__(self, *args, **kwargs):
        cantidad_salida = kwargs.pop('cantidad_salida')
        cantidad_ingresada = kwargs.pop('cantidad_ingresada')
        super(NotaSalidaDetalleSeriesForm, self).__init__(*args, **kwargs)
        self.fields['cantidad_salida'].initial = cantidad_salida
        self.fields['cantidad_ingresada'].initial = cantidad_ingresada
        if cantidad_ingresada == cantidad_salida:
            self.fields['serie'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            self.fields['cantidad_salida'].disabled = True
            self.fields['cantidad_ingresada'].disabled = True

class DespachoForm(BSModalModelForm):
    class Meta:
        model = Despacho
        fields = (
            'fecha_despacho',
            'observacion',
            )

        widgets = {
            'fecha_despacho' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(DespachoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
      
class DespachoAnularForm(BSModalModelForm):
    class Meta:
        model = Despacho
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(DespachoAnularForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



        # if self.request.session['primero']:
        #     series = form.cleaned_data['serie']
        #     nota_salida_detalle = NotaSalidaDetalle.objects.get(id = self.kwargs['pk'])
        #     serie_no_encontrada = []
        #     for serie in series.splitlines():
        #         buscar = Serie.objects.filter(
        #             serie_base=serie,
        #             content_type=ContentType.objects.get_for_model(nota_salida_detalle.producto),
        #             id_registro=nota_salida_detalle.producto.id,
        #         )
            
        #         if len(buscar) == 0:
        #             serie_no_encontrada.append(serie)
        #     if len(serie_no_encontrada) > 0:
        #         form.add_error('serie', "Serie no encontrada: %s" % ", ".join(serie_no_encontrada))
        #         return super().form_invalid(form)

        #     nota_salida_detalle = NotaSalidaDetalle.objects.get(id = self.kwargs['pk'])
        #     obj, created = ValidadSerieNotaSalidaDetalle.objects.get_or_create(
        #         nota_salida_detalle=nota_salida_detalle,
        #         serie=serie,
        #     )
        #     if created:
        #         obj.estado = 1
        #     self.request.session['primero'] = False
        # return super().form_valid(form)


class NotaSalidaBuscarForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado_sunat=1), required=False)
    estado = forms.ChoiceField(choices=((None, '---------'),) + ESTADOS_NOTA_CALIDAD_STOCK, required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_cliente = kwargs.pop('filtro_cliente')
        filtro_estado = kwargs.pop('filtro_estado')
        super(NotaSalidaBuscarForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['cliente'].initial = filtro_cliente
        self.fields['estado'].initial = filtro_estado
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'