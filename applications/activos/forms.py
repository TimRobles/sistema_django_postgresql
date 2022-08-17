from dataclasses import fields
from .models import ActivoBase, ArchivoAsignacionActivo, AsignacionActivo, AsignacionDetalleActivo, FamiliaActivo, SubFamiliaActivo
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms


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
