from django import forms
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.material.models import Material, ProveedorMaterial
from .models import ArchivoOfertaProveedor, OfertaProveedor, OfertaProveedorDetalle
from applications.datos_globales.models import Unidad

class OfertaProveedorForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedor
        fields=(
            'numero_oferta',
            'incoterms',
            'condiciones',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class OfertaProveedorUpdateForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedor
        fields=(
            'puerto_origen',
            'forma_pago',
            'tiempo_estimado_entrega',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorComentarioForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedor
        fields=(
            'condiciones',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorComentarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorMonedaForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedor
        fields=(
            'moneda',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMonedaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorDetalleUpdateForm(BSModalModelForm):
    name = forms.CharField(max_length=50)
    brand = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    unidad = forms.CharField(label='Unidad Base', required=False)
    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'name',
            'brand',
            'description',
            'tipo_igv',
            'unidad',
            'cantidad',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'igv',
            'total',
            'imagen',
            'especificaciones_tecnicas',
            )
    
    def clean_precio_final_con_igv(self):
        precio_final_con_igv = self.cleaned_data.get('precio_final_con_igv')
        precio_unitario_con_igv = self.cleaned_data.get('precio_unitario_con_igv')
        if precio_final_con_igv > precio_unitario_con_igv:
            self.add_error('precio_final_con_igv', 'El precio final no puede ser mayor al precio unitario.')
    
        return precio_final_con_igv

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorDetalleUpdateForm, self).__init__(*args, **kwargs)
        internacional_nacional = self.instance.oferta_proveedor.internacional_nacional
        self.fields['name'].initial = self.instance.proveedor_material.name
        self.fields['brand'].initial = self.instance.proveedor_material.brand
        self.fields['description'].initial = self.instance.proveedor_material.description
        if internacional_nacional == 1:
            self.fields['tipo_igv'].widget = forms.HiddenInput()
            self.fields['precio_unitario_sin_igv'].widget = forms.HiddenInput()
            self.fields['sub_total'].widget = forms.HiddenInput()
            self.fields['igv'].widget = forms.HiddenInput()
            self.fields['precio_unitario_con_igv'].label = "Precio Unitario"
            self.fields['precio_final_con_igv'].label = "Precio Final"
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 1
        self.fields['unidad'].initial = self.instance.proveedor_material.unidad
        self.fields['precio_unitario_con_igv'].widget.attrs['min'] = 0
        self.fields['precio_final_con_igv'].widget.attrs['min'] = 0
        
class OfertaProveedorDetalleProveedorMaterialUpdateForm(BSModalForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all())
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    class Meta:
        fields=(
            'content_type',
            'material',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorDetalleProveedorMaterialUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AgregarMaterialOfertaProveedorForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=None)
    unidad = forms.CharField(label='Unidad Base', required=False)

    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'material',
            'cantidad',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        lista_materiales = kwargs.pop('materiales')
        super(AgregarMaterialOfertaProveedorForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        self.fields['unidad'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CrearMaterialOfertaProveedorForm(BSModalForm):
    name = forms.CharField( max_length=100 )
    brand = forms.CharField( max_length=100 )
    description = forms.CharField( max_length=255 )
    unidad = forms.ModelChoiceField(queryset=Unidad.objects.all())

    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'name',
            'brand',
            'description',
            'unidad',
            )

    def __init__(self, *args, **kwargs):
        super(CrearMaterialOfertaProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ArchivoOfertaProveedorForm(BSModalModelForm):

    class Meta:
        model = ArchivoOfertaProveedor
        fields=(
            'archivo',
            )

    def __init__(self, *args, **kwargs):
        super(ArchivoOfertaProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OrdenCompraSociedadForm(BSModalForm):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1))
    class Meta:
        fields=(
            'sociedad',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraSociedadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
