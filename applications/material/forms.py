from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat, Unidad
from applications.proveedores.models import Proveedor
from .models import Clase, Componente, Atributo, Familia, SubFamilia, Modelo, Marca, Material, RelacionMaterialComponente, Especificacion, Datasheet,ImagenMaterial,VideoMaterial,ProveedorMaterial,EquivalenciaUnidad,Idioma,IdiomaMaterial
from applications.cotizacion.models import PrecioListaMaterial
from applications.comprobante_compra.models import ComprobanteCompraPI

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = (
            'nombre',
            'imagen',
            'descripcion',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Clase.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Clase con este nombre')

        return nombre

class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Componente.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Componente con este nombre')

        return nombre

class AtributoForm(forms.ModelForm):
    class Meta:
        model = Atributo
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Atributo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Atributo con este nombre')

        return nombre

class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = (
            'nombre',
            'atributos',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Familia.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Familia con este nombre')

        return nombre

class SubFamiliaForm(forms.ModelForm):
    class Meta:
        model = SubFamilia
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
        filtro = SubFamilia.objects.filter(nombre__unaccent__iexact = nombre, familia = familia)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una SubFamilia con este nombre')

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Modelo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Modelo con este nombre')

        return nombre

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
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
        filtro = Marca.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Marca con este nombre')

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'

class MaterialBuscarForm(forms.Form): 
    buscar = forms.CharField(max_length=150, required=False) 

 
    def __init__(self, *args, **kwargs): 
        filtro = kwargs.pop('filtro') 
        super(MaterialBuscarForm, self).__init__(*args, **kwargs) 
        self.fields['buscar'].initial = filtro 
        for visible in self.visible_fields(): 
            visible.field.widget.attrs['class'] = 'form-control' 
 
class MaterialForm(BSModalModelForm):
    familia = forms.ModelChoiceField(label = 'Familia', queryset = Familia.objects.all(), required=False)
    
    class Meta:
        model = Material
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
        subfamilia.queryset = SubFamilia.objects.filter(familia = familia)   
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
        filtro = Material.objects.filter(descripcion_venta__unaccent__iexact = descripcion_venta)
        if descripcion_venta != self.instance.descripcion_venta:
            if len(filtro)>0:
                self.add_error('descripcion_venta', 'Ya existe un material con esa descripción de venta')
        return descripcion_venta

    def clean_descripcion_corta(self):
        descripcion_corta = self.cleaned_data.get('descripcion_corta')
        filtro = Material.objects.filter(descripcion_corta__unaccent__iexact = descripcion_corta)
        if descripcion_corta != self.instance.descripcion_corta:
            if len(filtro)>0:
                self.add_error('descripcion_corta', 'Ya existe un material con esa descripción corta')
        return descripcion_corta

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['subfamilia'].queryset = SubFamilia.objects.none()
        self.fields['unidad_base'].queryset = Unidad.objects.none()
        try:
            subfamilia = self.instance.subfamilia 
            familia = subfamilia.familia
            marca = self.instance.marca 
            
            self.fields['familia'].initial = familia
            self.fields['subfamilia'].queryset = SubFamilia.objects.filter(familia = familia)
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

        
class RelacionMaterialComponenteForm(BSModalModelForm):
    class Meta:
        model = RelacionMaterialComponente
        fields=(
            'componentematerial',
            'cantidad',
            )


    def __init__(self, *args, **kwargs):
        componentes = kwargs.pop('componentes')
        super(RelacionMaterialComponenteForm, self).__init__(*args, **kwargs)
        self.fields['componentematerial'].queryset = componentes
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
   
class EspecificacionForm(BSModalModelForm):
    class Meta:
        model = Especificacion
        fields=(
            'orden',
            'atributomaterial',
            'valor',
            )

    def __init__(self, *args, **kwargs):
        atributos = kwargs.pop('atributos')
        super(EspecificacionForm, self).__init__(*args, **kwargs)   
        self.fields['atributomaterial'].queryset = atributos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DatasheetForm(BSModalModelForm):
    class Meta:
        model = Datasheet
        fields=(
            'descripcion',
            'archivo',
            )

    def __init__(self, *args, **kwargs):
        super(DatasheetForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DatosImportacionForm(BSModalModelForm):
    class Meta:
        model = Material
        fields=(
            'traduccion',
            'partida',
            'uso_funcion',
            'compuesto_por',
            'es_componente',
            )

    def __init__(self, *args, **kwargs):
        super(DatosImportacionForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['es_componente'].widget.attrs['class'] = 'form-check-input'

class ProductoSunatForm(BSModalModelForm):
    segmento_sunat = forms.ModelChoiceField(label = 'Segmento Sunat', queryset = SegmentoSunat.objects.all(), required=False)
    familia_sunat = forms.ModelChoiceField(label = 'Familia Sunat', queryset = FamiliaSunat.objects.none(), required=False)
    clase_sunat = forms.ModelChoiceField(label = 'Clase Sunat', queryset = ClaseSunat.objects.none(), required=False)
    producto_sunat = forms.ModelChoiceField(label = 'Producto Sunat', queryset = ProductoSunat.objects.none(), required=False)
    class Meta:
        model = Material
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
        super(ProductoSunatForm, self).__init__(*args, **kwargs)
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

class ImagenMaterialForm(BSModalModelForm):
    class Meta:
        model = ImagenMaterial
        fields =(
            'descripcion',
            'imagen',
        )
    
    def __init__(self, *args, **kwargs):
        super(ImagenMaterialForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class VideoMaterialForm(BSModalModelForm):
    class Meta:
        model = VideoMaterial
        fields =(
            'descripcion',
            'url',
        )
    
    def __init__(self, *args, **kwargs):
        super(VideoMaterialForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProveedorMaterialForm(BSModalModelForm):
    class Meta:
        model = ProveedorMaterial
        fields=(
            'proveedor',
            'name',
            'brand',
            'description',
            )

    def __init__(self, *args, **kwargs):
        super(ProveedorMaterialForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor.objects.filter(estado = 1)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
   
class EquivalenciaUnidadForm(BSModalModelForm):
    unidad_base = forms.CharField(max_length=50)
    class Meta:
        model = EquivalenciaUnidad
        fields =(
            'cantidad_base',
            'unidad_base',
            'cantidad_nueva_unidad',
            'nueva_unidad',
        )
    
    def __init__(self, *args, **kwargs):
        material = kwargs.pop('material')
        super(EquivalenciaUnidadForm, self).__init__(*args, **kwargs) 
        self.fields['unidad_base'].initial = material.unidad_base
        self.fields['nueva_unidad'].queryset = material.subfamilia.unidad.all().exclude(id = material.unidad_base.id)
        self.fields['unidad_base'].disabled = True
         
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = Idioma.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe este Idioma.')
        return nombre

class IdiomaMaterialForm(BSModalModelForm):
    class Meta:
        model = IdiomaMaterial
        fields = (
            'idioma',
            'traduccion',
        )

    def __init__(self, *args, **kwargs):
        super(IdiomaMaterialForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PrecioListaMaterialForm (BSModalModelForm):
    comprobante = forms.ChoiceField(choices=[(0,0)], required=False)
    class Meta:
        model = PrecioListaMaterial
        fields = (
            'comprobante',
            'moneda',
            'precio_compra',
            'logistico',
            'margen_venta',
            'precio_sin_igv',
            'precio_lista',
        )

    def __init__(self, *args, **kwargs):
        precios = kwargs.pop('precios')
        super(PrecioListaMaterialForm, self).__init__(*args, **kwargs)
        self.fields['comprobante'].choices = precios
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
