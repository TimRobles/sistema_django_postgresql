from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.logistica.models import DocumentoPrestamoMateriales, NotaSalida, NotaSalidaDetalle, SolicitudPrestamoMateriales, SolicitudPrestamoMaterialesDetalle
from django import forms

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
    cantidad_prestamo = forms.DecimalField(label = 'Cantidad Prestamo', max_digits=22, decimal_places=10)
    observacion = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        fields = (
            'material',
            'cantidad_prestamo',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudPrestamoMaterialesDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    class Meta:
        model = SolicitudPrestamoMaterialesDetalle
        fields=(
            'material',
            'cantidad_prestamo',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudPrestamoMaterialesDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        self.fields['material'].initial = busqueda_material.descripcion_venta
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
 #.....XxRonnyxX
class NotaSalidaDetalleForm(BSModalModelForm):  #.....XxRonnyxX
    material = forms.ModelChoiceField(queryset=None) #.....XxRonnyxX
 #.....XxRonnyxX
    class Meta: #.....XxRonnyxX
        model = NotaSalidaDetalle #.....XxRonnyxX
        fields=( #.....XxRonnyxX
            'material', #.....XxRonnyxX
            ) #.....XxRonnyxX
 #.....XxRonnyxX
    def __init__(self, *args, **kwargs): #.....XxRonnyxX
        lista_materiales = kwargs.pop('materiales') #.....XxRonnyxX
        super(NotaSalidaDetalleForm, self).__init__(*args, **kwargs) #.....XxRonnyxX
        self.fields['material'].queryset = lista_materiales #.....XxRonnyxX
        for visible in self.visible_fields(): #.....XxRonnyxX
            visible.field.widget.attrs['class'] = 'form-control' #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaDetalleUpdateForm(BSModalModelForm): #.....XxRonnyxX
    cantidad_prestamo = forms.DecimalField(label = 'Cantidad Prestamo', max_digits=22, decimal_places=10) #.....XxRonnyxX
    class Meta: #.....XxRonnyxX
        model = NotaSalidaDetalle #.....XxRonnyxX
        fields = ( #.....XxRonnyxX
            'sede', #.....XxRonnyxX
            'almacen', #.....XxRonnyxX
            'cantidad_prestamo', #.....XxRonnyxX
            'cantidad_salida', #.....XxRonnyxX
            ) #.....XxRonnyxX
 #.....XxRonnyxX    
    def clean_sede(self): #.....XxRonnyxX
        sede = self.cleaned_data.get('sede') #.....XxRonnyxX
        almacen = self.fields['almacen'] #.....XxRonnyxX
        almacen.queryset = Almacen.objects.filter(sede = sede) #.....XxRonnyxX    
        return sede #.....XxRonnyxX
 #.....XxRonnyxX   
    def __init__(self, *args, **kwargs): #.....XxRonnyxX
        solicitud = kwargs.pop('solicitud') #.....XxRonnyxX
        super(NotaSalidaDetalleUpdateForm, self).__init__(*args, **kwargs) #.....XxRonnyxX
        self.fields['cantidad_prestamo'].initial = solicitud.cantidad_prestamo #.....XxRonnyxX
        self.fields['almacen'].queryset = Almacen.objects.none() #.....XxRonnyxX
        self.fields['sede'].required = True #.....XxRonnyxX
        self.fields['almacen'].required = True #.....XxRonnyxX
        self.fields['cantidad_salida'].required = True #.....XxRonnyxX
        self.fields['cantidad_prestamo'].disabled = True #.....XxRonnyxX
        try: #.....XxRonnyxX
            almacen = self.instance.almacen #.....XxRonnyxX
            sede = almacen.sede #.....XxRonnyxX
 #.....XxRonnyxX            
            self.fields['sede'].initial = sede #.....XxRonnyxX
            self.fields['almacen'].queryset = Almacen.objects.filter(sede = sede) #.....XxRonnyxX
        except: #.....XxRonnyxX
            pass #.....XxRonnyxX
        for visible in self.visible_fields(): #.....XxRonnyxX
            visible.field.widget.attrs['class'] = 'form-control' #.....XxRonnyxX
 #.....XxRonnyxX
class NotaSalidaAnularForm(BSModalModelForm): #.....XxRonnyxX
    class Meta: #.....XxRonnyxX
        model = NotaSalida #.....XxRonnyxX
        fields=( #.....XxRonnyxX
            'motivo_anulacion', #.....XxRonnyxX
            ) #.....XxRonnyxX

    def __init__(self, *args, **kwargs): #.....XxRonnyxX
        super(NotaSalidaAnularForm, self).__init__(*args, **kwargs) #.....XxRonnyxX
        for visible in self.visible_fields(): #.....XxRonnyxX
            visible.field.widget.attrs['class'] = 'form-control' #.....XxRonnyxX