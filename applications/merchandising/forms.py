from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat, Unidad
from applications.proveedores.models import Proveedor
from applications.sociedad.models import Sociedad
from applications.almacenes.models import Almacen
from applications.sede.models import Sede
from django.contrib.contenttypes.models import ContentType

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
    IdiomaMerchandising,
    ListaRequerimientoMerchandising,
    ListaRequerimientoMerchandisingDetalle,
    OfertaProveedorMerchandising,
    OfertaProveedorMerchandisingDetalle,
    ComprobanteCompraMerchandising,
    ComprobanteCompraMerchandisingDetalle,
    OrdenCompraMerchandising,
    NotaIngresoMerchandising, 
    NotaIngresoMerchandisingDetalle,
    )
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
            'descripcion_corta',
            'familia',
            'subfamilia',
            )

    def clean_familia(self):
        familia = self.cleaned_data.get('familia')
        subfamilia = self.fields['subfamilia']
        subfamilia.queryset = SubFamiliaMerchandising.objects.filter(familia = familia)   
        return familia
    
    def clean_subfamilia(self):
        subfamilia = self.cleaned_data.get('subfamilia')
        # unidad= self.fields['unidad_base']
        # unidad.queryset = subfamilia.unidad.all()
        return subfamilia

    # def clean_marca(self):
    #     marca = self.cleaned_data.get('marca')
    #     modelo = self.fields['modelo']
    #     if marca:
    #         modelo.queryset = marca.modelos.all()
    #     return marca
        
    # def clean_descripcion_venta(self):
    #     descripcion_venta = self.cleaned_data.get('descripcion_venta')
    #     filtro = Merchandising.objects.filter(descripcion_venta__unaccent__iexact = descripcion_venta)
    #     if descripcion_venta != self.instance.descripcion_venta:
    #         if len(filtro)>0:
    #             self.add_error('descripcion_venta', 'Ya existe un merchandising con esa descripción de venta')
    #     return descripcion_venta

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
            # self.fields['familia'].disabled = True
            visible.field.required = False
            


        
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

########################Nuevo Merchandising#########################################################
class ListaRequerimientoMerchandisingBuscarForm(forms.Form):
    titulo = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        filtro_titulo = kwargs.pop('filtro_titulo')
        super(ListaRequerimientoMerchandisingBuscarForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].initial = filtro_titulo
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ListaRequerimientoMerchandisingForm(BSModalForm):
    titulo = forms.CharField(max_length=150, required=True)

    class Meta:
        fields = (
            'titulo',
        )
    
    def __init__(self, *args, **kwargs):
        try:
            kwargs_2 = kwargs.pop('instance')
            titulo = kwargs_2.pop('titulo')

        except:
            try:
                titulo = kwargs.pop('titulo')
            except:
                titulo = None

        super(ListaRequerimientoMerchandisingForm, self).__init__(*args, **kwargs)
        if titulo:
            self.fields['titulo'].initial = titulo
        else:
            self.fields['titulo'].initial = titulo

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ListaRequerimientoMerchandisingDetalleForm(BSModalForm):
    merchandising = forms.CharField(max_length=150, required=True)
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    comentario = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = ListaRequerimientoMerchandisingDetalle
        fields=(
            'merchandising',
            'cantidad',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ListaRequerimientoMerchandisingDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001

class ListaRequerimientoMerchandisingDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = ListaRequerimientoMerchandisingDetalle
        fields=(
            'merchandising',
            'cantidad',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ListaRequerimientoMerchandisingDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001



class OfertaProveedorMerchandisingCrearForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandising
        fields=(
            'proveedor',
            )
    
    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingCrearForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class OfertaProveedorMerchandisingUpdateForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandising
        fields=(
            'forma_pago',
            'tiempo_estimado_entrega',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class OfertaProveedorMerchandisingMonedaForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandising
        fields=(
            'moneda',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingMonedaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorMerchandisingDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandisingDetalle
        fields=(
            'cantidad',
            'tipo_igv',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'igv',
            'total',
            'archivo',
            )

    def clean_precio_final_con_igv(self):
        precio_final_con_igv = self.cleaned_data.get('precio_final_con_igv')
        precio_unitario_con_igv = self.cleaned_data.get('precio_unitario_con_igv')
        if precio_final_con_igv > precio_unitario_con_igv:
            self.add_error('precio_final_con_igv', 'El precio final no puede ser mayor al precio unitario.')
    
        return precio_final_con_igv
    
    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingDetalleUpdateForm, self).__init__(*args, **kwargs)
        internacional_nacional = self.instance.oferta_proveedor_merchandising.internacional_nacional
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
        self.fields['cantidad'].widget.attrs['step'] = 0.001
        self.fields['precio_unitario_con_igv'].widget.attrs['min'] = 0
        self.fields['precio_final_con_igv'].widget.attrs['min'] = 0

class OfertaProveedorMerchandisingCondicionesForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandising
        fields=(
            'condiciones',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingCondicionesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorMerchandisingEvaluarForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandising
        fields=(
            'evaluada',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingEvaluarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['evaluada'].widget.attrs['class'] = 'form-check-input'




class AgregarMerchandisingOfertaProveedorForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandisingDetalle
        fields=(
            'merchandising',
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        super(AgregarMerchandisingOfertaProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UnirMerchandisingDetalleForm(BSModalModelForm):
    merch = forms.ModelChoiceField(queryset=Merchandising.objects.all())
    class Meta:
        model = OfertaProveedorMerchandisingDetalle
        fields=(
            'merch',
            )

    def __init__(self, *args, **kwargs):
        super(UnirMerchandisingDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OfertaProveedorMerchandisingForm(BSModalModelForm):
    class Meta:
        model = OfertaProveedorMerchandising
        fields=(
            'numero_oferta',
            'condiciones',
            )

    def __init__(self, *args, **kwargs):
        super(OfertaProveedorMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

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

#_______________________
class ComprobanteCompraMerchandisingBuscarForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.filter(estado_sunat=1), required=False)
    proveedor = forms.ModelChoiceField(queryset= Proveedor.objects.all(), required=False)
    merchandising = forms.ModelChoiceField(queryset= Merchandising.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_proveedor = kwargs.pop('filtro_proveedor')
        filtro_merchandising = kwargs.pop('filtro_merchandising')

        super(ComprobanteCompraMerchandisingBuscarForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['proveedor'].initial = filtro_proveedor
        self.fields['merchandising'].initial = filtro_merchandising

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
#_______________________


class OrdenCompraMerchandisingEnviarCorreoForm(BSModalForm):
    CHOICES = (
        (1, 'a'),
        (2, 'b'),
        (3, 'c'),
    )
    correos_proveedor = forms.MultipleChoiceField(choices=CHOICES, required=False, widget=forms.CheckboxSelectMultiple())
    correos_internos = forms.MultipleChoiceField(choices=[None], required=False, widget=forms.CheckboxSelectMultiple())

    class Meta:
        fields=(
            'correos_proveedor',
            'correos_internos',
            )

    def __init__(self, *args, **kwargs):
        proveedor = kwargs.pop('proveedor')

        CORREOS_PROVEEDOR = []
        for interlocutor_proveedor in proveedor.ProveedorInterlocutor_proveedor.all():
            for correo_interlocutor in interlocutor_proveedor.interlocutor.CorreoInterlocutorProveedor_interlocutor.filter(estado=1):
                CORREOS_PROVEEDOR.append((correo_interlocutor.correo, '%s %s (%s)' % (interlocutor_proveedor.interlocutor.nombres, interlocutor_proveedor.interlocutor.apellidos, correo_interlocutor.correo)))

        CORREOS_INTERNOS = []
        usuarios = get_user_model().objects.exclude(email='')
        for usuario in usuarios:
            CORREOS_INTERNOS.append((usuario.email, '%s (%s)' % (usuario.username, usuario.email)))

        super(OrdenCompraMerchandisingEnviarCorreoForm, self).__init__(*args, **kwargs)
        self.fields['correos_internos'].choices = CORREOS_INTERNOS
        self.fields['correos_proveedor'].choices = CORREOS_PROVEEDOR
        self.fields['correos_internos'].widget.attrs['class'] = 'nobull'
        self.fields['correos_proveedor'].widget.attrs['class'] = 'nobull'

class OrdenCompraMerchandisingProveedorForm(BSModalModelForm):
    class Meta:
        model = OrdenCompraMerchandising
        fields=(
            'proveedor_temporal',
            'interlocutor_temporal',
            )
        
    def __init__(self, *args, **kwargs):
        super(OrdenCompraMerchandisingProveedorForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ComprobanteCompraMerchandisingForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraMerchandising
        fields=(
            'fecha_comprobante',
            'numero_comprobante_compra',
            )
        widgets = {
            'fecha_comprobante' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ComprobanteCompraMerchandisingLlegadaForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraMerchandising
        fields=(
            'fecha_estimada_llegada',
            )
        widgets = {
            'fecha_estimada_llegada' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ComprobanteCompraMerchandisingLlegadaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# Recepción Comprobante
class RecepcionComprobanteCompraMerchandisingForm(BSModalForm):
    fecha_recepcion = forms.DateField(
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    usuario_recepcion = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    nro_bultos = forms.IntegerField()
    observaciones = forms.CharField(
        widget=forms.Textarea(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(RecepcionComprobanteCompraMerchandisingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RecepcionCompraGenerarNotaIngresoForm(BSModalForm):
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
        super(RecepcionCompraGenerarNotaIngresoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



# Nota de Ingreso
class NotaIngresoAgregarMerchandisingForm(BSModalForm):
    producto = forms.ChoiceField(choices=[('1', '1'), ('2', '2')])
    cantidad = forms.DecimalField(max_digits=8, decimal_places=2)
    sede = forms.ModelChoiceField(queryset=Sede.objects.filter(estado=1))
    almacen = forms.ModelChoiceField(queryset=Almacen.objects.none())
    class Meta:
        fields=(
            'producto',
            'cantidad',
            'sede',
            'almacen',
            )
    
    def clean_sede(self):
        sede = self.cleaned_data.get('sede')
        almacen = self.fields['almacen']
        almacen.queryset = Almacen.objects.filter(sede = sede)    
        return sede
        
    def __init__(self, *args, **kwargs):
        productos = kwargs.pop('productos')
        try:
            nota_ingreso_detalle = kwargs.pop('nota_ingreso_detalle')
        except:
            pass
        super(NotaIngresoAgregarMerchandisingForm, self).__init__(*args, **kwargs)
        self.fields['producto'].choices = productos
        try:
            detalle = nota_ingreso_detalle.comprobante_compra_detalle
            valor = "%s|%s" % (ContentType.objects.get_for_model(detalle).id, detalle.id)
            self.fields['producto'].initial = valor
            self.fields['cantidad'].initial = nota_ingreso_detalle.cantidad_conteo
            self.fields['sede'].initial = nota_ingreso_detalle.almacen.sede
            self.fields['almacen'].queryset = Almacen.objects.filter(sede = nota_ingreso_detalle.almacen.sede)
            self.fields['almacen'].initial = nota_ingreso_detalle.almacen
        except:
            pass
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoFinalizarConteoForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMerchandising
        fields = (
            'observaciones',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoFinalizarConteoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NotaIngresoAnularConteoForm(BSModalModelForm):    
    class Meta:
        model = NotaIngresoMerchandising
        fields = (
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(NotaIngresoAnularConteoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'