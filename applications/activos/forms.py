from datetime import date
from .models import (
    ActivoBase,
    ArchivoAsignacionActivo,
    ArchivoDevolucionActivo,
    ArchivoComprobanteCompraActivo,
    AsignacionActivo,
    AsignacionDetalleActivo,
    DevolucionActivo,
    DevolucionDetalleActivo,
    DocumentoInventarioActivo,
    FamiliaActivo,
    InventarioActivo,
    InventarioActivoDetalle,
    SubFamiliaActivo,
    Activo,
    ActivoUbicacion,
    ActivoSociedad,
    ComprobanteCompraActivo,
    ComprobanteCompraActivoDetalle,
    MarcaActivo,
    ModeloActivo,
    )
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth import get_user_model


class FamiliaActivoForm(forms.ModelForm):
    class Meta:
        model = FamiliaActivo
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = FamiliaActivo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una Familia con este nombre')

        return nombre


class SubFamiliaActivoForm(forms.ModelForm):
    class Meta:
        model = SubFamiliaActivo
        fields = (
            'nombre',
            'familia',
            )

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        familia = cleaned_data.get('familia')
        filtro = SubFamiliaActivo.objects.filter(nombre__unaccent__iexact = nombre, familia = familia)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe una SubFamilia con este nombre')


class ProductoSunatActivoForm(BSModalModelForm):
    segmento_sunat = forms.ModelChoiceField(label = 'Segmento Sunat', queryset = SegmentoSunat.objects.all(), required=False)
    familia_sunat = forms.ModelChoiceField(label = 'Familia Sunat', queryset = FamiliaSunat.objects.none(), required=False)
    clase_sunat = forms.ModelChoiceField(label = 'Clase Sunat', queryset = ClaseSunat.objects.none(), required=False)
    producto_sunat = forms.ModelChoiceField(label = 'Producto Sunat', queryset = ProductoSunat.objects.none(), required=False)
    class Meta:
        model = ActivoBase
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
        super(ProductoSunatActivoForm, self).__init__(*args, **kwargs)
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


class ActivoBaseForm(BSModalModelForm):
    familia = forms.ModelChoiceField(label = 'Familia', queryset = FamiliaActivo.objects.all(), required=False)
    
    class Meta:
        model = ActivoBase
        fields = (
            'descripcion_venta',
            'descripcion_corta',
            'unidad',
            'peso',
            'familia',
            'sub_familia',
            'depreciacion',
            'vida_util',
            'traduccion',
            'partida',
            )

    def clean_familia(self):
        familia = self.cleaned_data.get('familia')
        subfamilia = self.fields['sub_familia']
        subfamilia.queryset = SubFamiliaActivo.objects.filter(familia = familia)
        return familia

    def __init__(self, *args, **kwargs):
        super(ActivoBaseForm, self).__init__(*args, **kwargs)
        self.fields['sub_familia'].queryset = SubFamiliaActivo.objects.none()
        try:
            subfamilia = self.instance.sub_familia 
            familia = subfamilia.familia
            
            self.fields['familia'].initial = familia
            self.fields['sub_familia'].queryset = SubFamiliaActivo.objects.filter(familia = familia)
        except:
            pass

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class AsignacionActivoForm(BSModalModelForm):

    class Meta:
        model = AsignacionActivo
        fields = (
            'titulo',
            'colaborador',
            'fecha_asignacion',
            'observacion',
            )
        widgets = {
            'fecha_asignacion' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
        }

    def __init__(self, *args, **kwargs):
        super(AsignacionActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AsignacionDetalleActivoForm(BSModalModelForm):

    class Meta:
        model = AsignacionDetalleActivo
        fields = (
            'activo',
            )

    def __init__(self, *args, **kwargs):
        super(AsignacionDetalleActivoForm, self).__init__(*args, **kwargs)
        self.fields['activo'].queryset = Activo.objects.filter(estado=1) 
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class DevolucionActivoForm(BSModalModelForm):

    class Meta:
        model = DevolucionActivo
        fields = (
            'titulo',
            'colaborador',
            'fecha_devolucion',
            'observacion',
            'archivo',
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
        super(DevolucionActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            

class ArchivoAsignacionActivoForm(BSModalModelForm):

    class Meta:
        model = ArchivoAsignacionActivo
        fields=(
            'archivo',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ArchivoAsignacionActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ModeloActivoForm(BSModalModelForm):
    class Meta:
        model = ModeloActivo
        fields=(
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(ModeloActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = ModeloActivo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Modelo con este nombre')

        return nombre

class MarcaActivoForm(BSModalModelForm):
    class Meta:
        model = MarcaActivo
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
        filtro = MarcaActivo.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Marca con este nombre')

    def __init__(self, *args, **kwargs):
        super(MarcaActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelos'].widget.attrs['class'] = 'nobull'

class ActivoForm(BSModalModelForm):
    class Meta:
        model = Activo
        fields = (
            'numero_serie',
            'descripcion',
            'activo_base',
            'marca',
            'modelo',
            'fecha_compra',
            'tiempo_garantia',
            'color',
            'informacion_adicional',
            'declarable',
            )

        widgets = {
            'fecha_compra' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['declarable'].widget.attrs['class'] = 'form-check-input'

class ActivoSociedadForm(BSModalModelForm):
    class Meta:
        model = ActivoSociedad
        fields=(
            'sociedad',
            )

    def __init__(self, *args, **kwargs):
        super(ActivoSociedadForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ActivoUbicacionForm(BSModalModelForm):
    class Meta:
        model = ActivoUbicacion
        fields=(
            'sede',
            'piso',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ActivoUbicacionForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ComprobanteCompraActivoForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraActivo
        fields = (
            'numero_comprobante',
            'tipo_comprobante',
            'fecha_comprobante',
            'internacional_nacional',
            'sociedad',
            'incoterms',
            'orden_compra',
            'moneda',
            'condiciones',
            'logistico',
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
        super(ComprobanteCompraActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ComprobanteCompraActivoDetalleForm(BSModalModelForm):
    class Meta:
        model = ComprobanteCompraActivoDetalle
        fields=(
            'activo',
            'descripcion_comprobante',
            'orden_compra_detalle',
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
        super(ComprobanteCompraActivoDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DevolucionDetalleActivoForm(BSModalModelForm):

    class Meta:
        model = DevolucionDetalleActivo
        fields = (
            'asignacion',
            'activo',
            )

    def __init__(self, *args, **kwargs):
        super(DevolucionDetalleActivoForm, self).__init__(*args, **kwargs)
        self.fields['activo'].queryset = Activo.objects.filter(estado=3) 
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ArchivoDevolucionActivoForm(BSModalModelForm):

    class Meta:
        model = ArchivoDevolucionActivo
        fields=(
            'archivo',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ArchivoDevolucionActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ArchivoComprobanteCompraActivoDetalleForm(BSModalModelForm):
    class Meta:
        model = ArchivoComprobanteCompraActivo
        fields=(
            'archivo',
            )

    def __init__(self, *args, **kwargs):
        super(ArchivoComprobanteCompraActivoDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InventarioActivoForm(BSModalModelForm):
    class Meta:
        model = InventarioActivo
        fields=(
            'usuario',
            'fecha_inventario',
            )

        widgets = {
            'fecha_inventario' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def clean_fecha_inventario(self):
        fecha_inventario = self.cleaned_data.get('fecha_inventario')
        if fecha_inventario > date.today():
            self.add_error('fecha_inventario', 'La fecha de inventario no puede ser mayor a la fecha de hoy.')

        return fecha_inventario

    def __init__(self, *args, **kwargs):
        super(InventarioActivoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = get_user_model().objects.exclude(first_name = "")
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InventarioActivoDetalleCreateForm(BSModalModelForm):
    class Meta:
        model = InventarioActivoDetalle
        fields=(
            'activo',
            )

    def __init__(self, *args, **kwargs):
        lista_activos = kwargs.pop('activos')
        # self.inventario_activo_id = kwargs.pop('inventario_activo_id')
        super(InventarioActivoDetalleCreateForm, self).__init__(*args, **kwargs)
        self.fields['activo'].queryset = lista_activos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     activo = cleaned_data.get('activo')
    #     print('**************************')
    #     print(activo)
    #     print('**************************')
    #     filtro = InventarioActivoDetalle.objects.filter(activo__unaccent__iexact = activo, inventario_activo = self.inventario_activo_id)
    #     print('++++++++++++++++++++++++++++++++')
    #     print(self.instance)
    #     print('++++++++++++++++++++++++++++++++')
    #     if activo != self.instance.activo:
    #         if len(filtro)>0:
    #             self.add_error('activo', 'Ya existe un actvo con esta descripción')

class InventarioActivoDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = InventarioActivoDetalle
        fields=(
            'observacion',
            'estado',
            )

    def __init__(self, *args, **kwargs):
        super(InventarioActivoDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DocumentoInventarioActivoForm(BSModalModelForm):
    class Meta:
        model = DocumentoInventarioActivo
        fields=(
            'observacion',
            'documento',
            )

    def __init__(self, *args, **kwargs):
        super(DocumentoInventarioActivoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'