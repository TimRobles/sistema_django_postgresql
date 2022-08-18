from django import forms
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.material.models import Material, ProveedorMaterial
from .models import ArchivoOfertaProveedor, OfertaProveedor, OfertaProveedorDetalle

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

class OfertaProveedorDetalleUpdateForm(BSModalModelForm):
    name = forms.CharField(max_length=50)
    brand = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'name',
            'brand',
            'description',
            'tipo_igv',
            'cantidad',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'igv',
            'total',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorDetalleUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.instance.proveedor_material.name
        self.fields['brand'].initial = self.instance.proveedor_material.brand
        self.fields['description'].initial = self.instance.proveedor_material.description
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
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

    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'material',
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        lista_materiales = kwargs.pop('materiales')
        super(AgregarMaterialOfertaProveedorForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = lista_materiales
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CrearMaterialOfertaProveedorForm(BSModalForm):
    name = forms.CharField( max_length=100 )
    brand = forms.CharField( max_length=100 )
    description = forms.CharField( max_length=255 )

    class Meta:
        model = OfertaProveedorDetalle
        fields=(
            'name',
            'brand',
            'description',
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
