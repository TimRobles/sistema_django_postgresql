from pyexpat import model
from django import forms
from django.contrib.contenttypes.models import ContentType
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.proveedores.models import InterlocutorProveedor, Proveedor,ProveedorInterlocutor
from applications.material.models import Material
from .models import ListaRequerimientoMaterialDetalle,RequerimientoMaterialProveedor,RequerimientoMaterialProveedorDetalle,RequerimientoMaterialDetalle


class ListaRequerimientoMaterialForm (BSModalForm):
    titulo = forms.CharField(max_length=150)
    
    class Meta:
        fields = (
            'titulo',
        )
    
    def clean_proveedor(self):
        titulo = self.cleaned_data.get('titulo')
        return titulo

    def __init__(self, *args, **kwargs):
        try:
            kwargs_2 = kwargs.pop('instance')
            titulo = kwargs_2.pop('titulo')

        except:
            try:
                titulo = kwargs.pop('titulo')
            except:
                titulo = None

        super(ListaRequerimientoMaterialForm, self).__init__(*args, **kwargs)
        if titulo:
            self.fields['titulo'].initial = titulo
        else:
            self.fields['titulo'].initial = titulo

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ListaRequerimientoMaterialDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    comentario = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = ListaRequerimientoMaterialDetalle
        fields=(
            'material',
            'cantidad',
            'comentario',
            )
    
    def __init__(self, *args, **kwargs):
        super(ListaRequerimientoMaterialDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ListaRequerimientoMaterialDetalleUpdateForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())

    class Meta:
        model = ListaRequerimientoMaterialDetalle
        fields=(
            'material',
            'cantidad',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ListaRequerimientoMaterialDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        self.fields['material'].initial = busqueda_material

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RequerimientoMaterialProveedorForm(BSModalModelForm):
    class Meta:
        model = RequerimientoMaterialProveedor
        fields=(
            'titulo',
            'proveedor',
            'interlocutor_proveedor',
            )

    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialProveedorForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RequerimientoMaterialProveedorDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)

    class Meta:
        model = RequerimientoMaterialProveedorDetalle
        fields=(
            'material',
            'cantidad',
            )
        

    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialProveedorDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id = self.instance.id_requerimiento_material_detalle.id_registro)
        self.fields['material'].initial = busqueda_material.descripcion_venta
        self.fields['material'].disabled = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RequerimientoMaterialProveedorDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    # comentario = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = RequerimientoMaterialProveedorDetalle
        fields=(
            'material',
            'cantidad',
            # 'comentario',
            )
    
    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialProveedorDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RequerimientoMaterialForm (BSModalForm):
    titulo = forms.CharField(max_length=150)
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all())
    interlocutor_proveedor = forms.ModelChoiceField(queryset=InterlocutorProveedor.objects.none(), required=False)
    class Meta:
        fields = (
            'titulo',
            'proveedor',
            'interlocutor_proveedor',
        )
    
    def clean_proveedor(self):
        titulo = self.cleaned_data.get('titulo')
        proveedor = self.cleaned_data.get('proveedor')
        interlocutor_proveedor = self.fields['interlocutor_proveedor']
        lista = []
        relaciones = ProveedorInterlocutor.objects.filter(proveedor = proveedor)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)
        interlocutor_proveedor.queryset = InterlocutorProveedor.objects.filter(id__in = lista)
        
        return proveedor

    def __init__(self, *args, **kwargs):
        try:
            kwargs_2 = kwargs.pop('instance')
            titulo = kwargs_2.pop('titulo')
            proveedor = kwargs_2.pop('proveedor')
            interlocutor = kwargs_2.pop('interlocutor')
        except:
            try:
                titulo = kwargs.pop('titulo')
                proveedor = kwargs.pop('proveedor')
                interlocutor = kwargs.pop('interlocutor')
            except:
                proveedor = None
                interlocutor = None
                titulo = None

        super(RequerimientoMaterialForm, self).__init__(*args, **kwargs)
        if titulo:
            self.fields['titulo'].initial = titulo
        else:
            self.fields['titulo'].initial = titulo


        if proveedor:
            self.fields['proveedor'].initial = proveedor

        if interlocutor:
            self.fields['interlocutor_proveedor'].queryset = ProveedorInterlocutor.objects.filter(proveedor = proveedor)
            self.fields['interlocutor_proveedor'].initial = interlocutor

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RequerimientoMaterialDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    class Meta:
        model = RequerimientoMaterialDetalle
        fields=(
            'material',
            'cantidad',
            )
    
    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RequerimientoMaterialDetalleUpdateForm(BSModalModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())

    class Meta:
        model = RequerimientoMaterialDetalle
        fields=(
            'material',
            'cantidad',
            )

    def clean_material(self):
        material = self.cleaned_data.get('material')

        self.instance.content_type = ContentType.objects.get_for_model(material)
        self.instance.id_registro = material.id
    
        return material

    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        self.fields['material'].initial = busqueda_material

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'