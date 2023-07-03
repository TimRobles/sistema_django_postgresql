from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat, Unidad
from applications.proveedores.models import Proveedor
from .models import (
    AjusteInventarioMerchandising,
    AjusteInventarioMerchandisingDetalle,
    ClaseMerchandising, 
    ComponenteMerchandising, 
    AtributoMerchandising, 
    FamiliaMerchandising,
    InventarioMerchandising,
    InventarioMerchandisingDetalle, 
    SubFamiliaMerchandising, 
    ModeloMerchandising, 
    MarcaMerchandising, 
    Merchandising, 
    RelacionMerchandisingComponente, 
    EspecificacionMerchandising, 
    DatasheetMerchandising,
    ImagenMerchandising,
    VideoMerchandising,
    ProveedorMerchandising,
    EquivalenciaUnidadMerchandising,
    IdiomaMerchandising)
from applications.cotizacion.models import PrecioListaMaterial
from applications.comprobante_compra.models import ComprobanteCompraPI
from django.contrib.auth import get_user_model

class ClaseMerchandisingForm(forms.ModelForm):
    class Meta:
        model = ClaseMerchandising
        fields = (
            'nombre',
            'imagen',
            'descripcion',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = ClaseMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Clase con este nombre')

        return nombre

class ComponenteMerchandisingForm(forms.ModelForm):
    class Meta:
        model = ComponenteMerchandising
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = ComponenteMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Componente con este nombre')

        return nombre

class AtributoMerchandisingForm(forms.ModelForm):
    class Meta:
        model = AtributoMerchandising
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = AtributoMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Atributo con este nombre')

        return nombre

class FamiliaMerchandisingForm(forms.ModelForm):
    class Meta:
        model = FamiliaMerchandising
        fields = (
            'nombre',
            'atributos',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = FamiliaMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Familia con este nombre')

        return nombre

class SubFamiliaMerchandisingForm(forms.ModelForm):
    class Meta:
        model = SubFamiliaMerchandising
        fields = (
            'nombre',
            'familia',
            'unidad',
            'componentes',
            )

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        familia = cleaned_data.get('familia')
        filtro = SubFamiliaMerchandising.objects.filter(nombre__unaccent__iexact = nombre, familia = familia)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una SubFamilia con este nombre')

class ModeloMerchandisingForm(BSModalModelForm):
    class Meta:
        model = ModeloMerchandising
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = ModeloMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Modelo con este nombre')

        return nombre

class MarcaMerchandisingForm(BSModalModelForm):
    class Meta:
        model = MarcaMerchandising
        fields=(
            'nombre',
            'modelos',
            )

        widgets = {
            'modelos': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        filtro = MarcaMerchandising.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Marca con este nombre')

    def __init__(self, *args, **kwargs):
        super(MarcaMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'

class MerchandisingBuscarForm(forms.Form): 
    buscar = forms.CharField(max_length=150, required=False) 

 
    def __init__(self, *args, **kwargs): 
        filtro = kwargs.pop('filtro') 
        super(MerchandisingBuscarForm, self).__init__(*args, **kwargs) 
        self.fields['buscar'].initial = filtro 
        for visible in self.visible_fields(): 
            visible.field.widget.attrs['class'] = 'form-control' 
 
class MerchandisingForm(BSModalModelForm):
    familia = forms.ModelChoiceField(label = 'Familia', queryset = FamiliaMerchandising.objects.all(), required=False)
    
    class Meta:
        model = Merchandising
        fields=(
            'descripcion_venta',
            'descripcion_corta',
            'familia',
            'subfamilia',
            'unidad_base',
            'peso_unidad_base',
            'marca',
            'modelo',
            'clase',
            'control_serie',
            'control_lote',
            'control_calidad',
            'mostrar',
            )

    def clean_familia(self):
        familia = self.cleaned_data.get('familia')
        subfamilia = self.fields['subfamilia']
        subfamilia.queryset = SubFamiliaMerchandising.objects.filter(familia = familia)   
        return familia
    
    def clean_subfamilia(self):
        subfamilia = self.cleaned_data.get('subfamilia')
        unidad= self.fields['unidad_base']
        unidad.queryset = subfamilia.unidad.all()
        return subfamilia

    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        modelo = self.fields['modelo']
        if marca:
            modelo.queryset = marca.modelos.all()
        return marca
        
    def clean_descripcion_venta(self):
        descripcion_venta = self.cleaned_data.get('descripcion_venta')
        filtro = Merchandising.objects.filter(descripcion_venta__unaccent__iexact = descripcion_venta)
        if descripcion_venta != self.instance.descripcion_venta:
            if len(filtro)>0:
                self.add_error('descripcion_venta', 'Ya existe un merchandising con esa descripción de venta')
        return descripcion_venta

    def clean_descripcion_corta(self):
        descripcion_corta = self.cleaned_data.get('descripcion_corta')
        filtro = Merchandising.objects.filter(descripcion_corta__unaccent__iexact = descripcion_corta)
        if descripcion_corta != self.instance.descripcion_corta:
            if len(filtro)>0:
                self.add_error('descripcion_corta', 'Ya existe un merchandising con esa descripción corta')
        return descripcion_corta

    def __init__(self, *args, **kwargs):
        super(MerchandisingForm, self).__init__(*args, **kwargs)
        self.fields['subfamilia'].queryset = SubFamiliaMerchandising.objects.none()
        self.fields['unidad_base'].queryset = Unidad.objects.none()
        try:
            subfamilia = self.instance.subfamilia 
            familia = subfamilia.familia
            marca = self.instance.marca 
            
            self.fields['familia'].initial = familia
            self.fields['subfamilia'].queryset = SubFamiliaMerchandising.objects.filter(familia = familia)
            self.fields['unidad_base'].queryset = subfamilia.unidad.all()
            self.fields['modelo'].queryset = marca.modelos.all()
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['control_serie'].widget.attrs['class'] = 'form-check-input'
        self.fields['control_lote'].widget.attrs['class'] = 'form-check-input'
        self.fields['control_calidad'].widget.attrs['class'] = 'form-check-input'
        self.fields['mostrar'].widget.attrs['class'] = 'form-check-input'
        self.fields['peso_unidad_base'].widget.attrs['min'] = 0

        
class RelacionMerchandisingComponenteForm(BSModalModelForm):
    class Meta:
        model = RelacionMerchandisingComponente
        fields=(
            'componentemerchandising',
            'cantidad',
            )


    def __init__(self, *args, **kwargs):
        componentes = kwargs.pop('componentes')
        super(RelacionMerchandisingComponenteForm, self).__init__(*args, **kwargs)
        self.fields['componentemerchandising'].queryset = componentes
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
   
class EspecificacionMerchandisingForm(BSModalModelForm):
    class Meta:
        model = EspecificacionMerchandising
        fields=(
            'orden',
            'atributomerchandising',
            'valor',
            )

    def __init__(self, *args, **kwargs):
        atributos = kwargs.pop('atributos')
        super(EspecificacionMerchandisingForm, self).__init__(*args, **kwargs)   
        self.fields['atributomerchandising'].queryset = atributos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DatasheetMerchandisingForm(BSModalModelForm):
    class Meta:
        model = DatasheetMerchandising
        fields=(
            'descripcion',
            'archivo',
            )

    def __init__(self, *args, **kwargs):
        super(DatasheetMerchandisingForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DatosImportacionMerchandisingForm(BSModalModelForm):
    class Meta:
        model = Merchandising
        fields=(
            'traduccion',
            'partida',
            'uso_funcion',
            'compuesto_por',
            'es_componente',
            )

    def __init__(self, *args, **kwargs):
        super(DatosImportacionMerchandisingForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['es_componente'].widget.attrs['class'] = 'form-check-input'

class ProductoSunatMerchandisingForm(BSModalModelForm):
    segmento_sunat = forms.ModelChoiceField(label = 'Segmento Sunat', queryset = SegmentoSunat.objects.all(), required=False)
    familia_sunat = forms.ModelChoiceField(label = 'Familia Sunat', queryset = FamiliaSunat.objects.none(), required=False)
    clase_sunat = forms.ModelChoiceField(label = 'Clase Sunat', queryset = ClaseSunat.objects.none(), required=False)
    producto_sunat = forms.ModelChoiceField(label = 'Producto Sunat', queryset = ProductoSunat.objects.none(), required=False)
    class Meta:
        model = Merchandising
        fields=(
            'segmento_sunat',
            'familia_sunat',
            'clase_sunat',
            'producto_sunat',
            )

    def clean_segmento_sunat(self):
        segmento_sunat = self.cleaned_data.get('segmento_sunat')
        familia_sunat = self.fields['familia_sunat']
        familia_sunat.queryset = FamiliaSunat.objects.filter(segmento = segmento_sunat.codigo)
        
        return segmento_sunat

    def clean_familia_sunat(self):
        familia_sunat = self.cleaned_data.get('familia_sunat')
        clase_sunat = self.fields['clase_sunat']
        clase_sunat.queryset = ClaseSunat.objects.filter(familia = familia_sunat.codigo)
    
        return familia_sunat

    def clean_clase_sunat(self):
        clase_sunat = self.cleaned_data.get('clase_sunat')
        producto_sunat = self.fields['producto_sunat']
        producto_sunat.queryset = ProductoSunat.objects.filter(clase = clase_sunat.codigo)
    
        return clase_sunat

    def __init__(self, *args, **kwargs):
        super(ProductoSunatMerchandisingForm, self).__init__(*args, **kwargs)
        producto_sunat = self.instance.producto_sunat
        if producto_sunat:
            clase_sunat = producto_sunat.clase
            familia_sunat = clase_sunat.familia
            segmento_sunat = familia_sunat.segmento
            self.fields['segmento_sunat'].initial = segmento_sunat
            self.fields['familia_sunat'].queryset = FamiliaSunat.objects.filter(segmento = segmento_sunat.codigo)
            self.fields['familia_sunat'].initial = familia_sunat
            self.fields['clase_sunat'].queryset = ClaseSunat.objects.filter(familia = familia_sunat.codigo)
            self.fields['clase_sunat'].initial = clase_sunat
            self.fields['producto_sunat'].queryset = ProductoSunat.objects.filter(clase = clase_sunat.codigo)
            self.fields['producto_sunat'].initial = producto_sunat
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProductoSunatBuscarForm(BSModalModelForm):
    vacio = forms.CharField(required=False)
    producto_sunat = forms.ModelChoiceField(label = 'Producto Sunat', queryset = ProductoSunat.objects.none(), required=False)
    class Meta:
        model = Merchandising
        fields=(
            'vacio',
            'producto_sunat',
            )
    
    def clean_vacio(self):
        vacio = self.cleaned_data.get('vacio')
        producto_sunat = self.fields['producto_sunat']
        producto_sunat.queryset = ProductoSunat.objects.all()
        return vacio

    def __init__(self, *args, **kwargs):
        super(ProductoSunatBuscarForm, self).__init__(*args, **kwargs)
        producto_sunat = self.instance.producto_sunat
        if producto_sunat:
            self.fields['producto_sunat'].queryset = ProductoSunat.objects.filter(codigo = producto_sunat.codigo)
            self.fields['producto_sunat'].initial = producto_sunat
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['vacio'].widget.attrs['class'] = 'form-control ocultar'

class ImagenMerchandisingForm(BSModalModelForm):
    class Meta:
        model = ImagenMerchandising
        fields =(
            'descripcion',
            'imagen',
        )
    
    def __init__(self, *args, **kwargs):
        super(ImagenMerchandisingForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class VideoMerchandisingForm(BSModalModelForm):
    class Meta:
        model = VideoMerchandising
        fields =(
            'descripcion',
            'url',
        )
    
    def __init__(self, *args, **kwargs):
        super(VideoMerchandisingForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProveedorMerchandisingForm(BSModalModelForm):
    class Meta:
        model = ProveedorMerchandising
        fields=(
            'proveedor',
            'name',
            'brand',
            'description',
            )

    def __init__(self, *args, **kwargs):
        super(ProveedorMerchandisingForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor.objects.filter(estado = 1)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
   
class EquivalenciaUnidadMerchandisingForm(BSModalModelForm):
    unidad_base = forms.CharField(max_length=50)
    class Meta:
        model = EquivalenciaUnidadMerchandising
        fields =(
            'cantidad_base',
            'unidad_base',
            'cantidad_nueva_unidad',
            'nueva_unidad',
        )
    
    def __init__(self, *args, **kwargs):
        merchandising = kwargs.pop('merchandising')
        super(EquivalenciaUnidadMerchandisingForm, self).__init__(*args, **kwargs) 
        self.fields['unidad_base'].initial = merchandising.unidad_base
        self.fields['nueva_unidad'].queryset = merchandising.subfamilia.unidad.all().exclude(id = merchandising.unidad_base.id)
        self.fields['unidad_base'].disabled = True
         
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class IdiomaMerchandisingForm(BSModalModelForm):
    class Meta:
        model = IdiomaMerchandising
        fields = (
            'idioma',
            'traduccion',
        )

    def __init__(self, *args, **kwargs):
        super(IdiomaMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

######################################################---INVENTARIO MERCHANDISING---######################################################

class InventarioMerchandisingForm(BSModalModelForm):
    class Meta:
        model = InventarioMerchandising
        fields = (
            'sociedad',
            'sede',
            'responsable',
            )

    def __init__(self, *args, **kwargs):
        super(InventarioMerchandisingForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].queryset = get_user_model().objects.exclude(first_name = "")
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class InventarioMerchandisingUpdateForm(BSModalModelForm):
    class Meta:
        model = InventarioMerchandising
        fields = (
            'responsable',
            )

    def __init__(self, *args, **kwargs):
        super(InventarioMerchandisingUpdateForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].queryset = get_user_model().objects.exclude(first_name = "")
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class InventarioMerchandisingDetalleForm(BSModalModelForm):
    almacen = forms.ModelChoiceField(queryset=None)
    class Meta:
        model = InventarioMerchandisingDetalle
        fields = (
            'merchandising',
            'almacen',
            'tipo_stock',
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        lista_almacenes = kwargs.pop('almacenes')
        super(InventarioMerchandisingDetalleForm, self).__init__(*args, **kwargs)
        self.fields['almacen'].queryset = lista_almacenes
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AjusteInventarioMerchandisingForm(BSModalModelForm):
    class Meta:
        model = AjusteInventarioMerchandising
        fields = (
            'responsable',
            'observacion',
            )

    def __init__(self, *args, **kwargs):
        super(AjusteInventarioMerchandisingForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].queryset = get_user_model().objects.exclude(first_name = "")
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AjusteInventarioMerchandisingDetalleForm(BSModalModelForm): 
    producto = forms.ModelChoiceField(label='Merchandising', queryset=None)

    class Meta:
        model = AjusteInventarioMerchandisingDetalle
        fields=(
            'producto',
            )

    def __init__(self, *args, **kwargs):
        lista_merchandising = kwargs.pop('merchandising')
        super(AjusteInventarioMerchandisingDetalleForm, self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = lista_merchandising
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'