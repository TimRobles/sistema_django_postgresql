from tabnanny import verbose
from webbrowser import get
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import Moneda
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from applications.proveedores.models import InterlocutorProveedor, Proveedor,ProveedorInterlocutor
from applications.material.models import Material, ProveedorMaterial
from applications.datos_globales.models import Moneda
from .models import ListaRequerimientoMaterialDetalle,RequerimientoMaterialProveedor,RequerimientoMaterialProveedorDetalle
from applications.variables import INTERNACIONAL_NACIONAL



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
    unidad = forms.CharField(label='Unidad Base', required=False)
    comentario = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = ListaRequerimientoMaterialDetalle
        fields=(
            'material',
            'cantidad',
            'unidad',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ListaRequerimientoMaterialDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001
        self.fields['unidad'].disabled = True

class ListaRequerimientoMaterialDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    unidad = forms.CharField(label='Unidad Base', required=False)
    class Meta:
        model = ListaRequerimientoMaterialDetalle
        fields=(
            'material',
            'cantidad',
            'unidad',
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ListaRequerimientoMaterialDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.content_type.get_object_for_this_type(id = self.instance.id_registro)
        self.fields['material'].initial = busqueda_material.descripcion_venta
        self.fields['material'].disabled = True
        self.fields['unidad'].initial = busqueda_material.unidad_base
        self.fields['unidad'].disabled = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001


class RequerimientoMaterialProveedorForm(BSModalModelForm):
    class Meta:
        model = RequerimientoMaterialProveedor
        fields=(
            'titulo',
            'proveedor',
            'interlocutor_proveedor',
            'comentario',
            'sociedad',
            )

    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialProveedorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True
        self.fields['comentario'].required = False

class RequerimientoMaterialProveedorDetalleUpdateForm(BSModalModelForm):
    material = forms.CharField(required=False)
    name = forms.CharField(required=False)
    brand = forms.CharField(required=False)
    description = forms.CharField(required=False)
    unidad = forms.CharField(label='Unidad Base', required=False)

    class Meta:
        model = RequerimientoMaterialProveedorDetalle
        fields=(
            'material',
            'name',
            'brand',
            'description',
            'unidad',
            'cantidad',
            )


    def __init__(self, *args, **kwargs):
        super(RequerimientoMaterialProveedorDetalleUpdateForm, self).__init__(*args, **kwargs)
        busqueda_material = self.instance.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id = self.instance.id_requerimiento_material_detalle.id_registro)
        proveedor_material = ProveedorMaterial.objects.get(
                content_type = self.instance.id_requerimiento_material_detalle.content_type,
                id_registro = self.instance.id_requerimiento_material_detalle.id_registro,
                proveedor = self.instance.requerimiento_material.proveedor,
                estado_alta_baja = 1,
            )
        self.fields['material'].initial = busqueda_material.descripcion_venta
        self.fields['unidad'].initial = busqueda_material.unidad_base
        self.fields['name'].initial = proveedor_material.name
        self.fields['brand'].initial = proveedor_material.brand
        self.fields['description'].initial = proveedor_material.description
        self.fields['material'].disabled = True
        self.fields['unidad'].disabled = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001

class RequerimientoMaterialProveedorDetalleForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=None)
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    unidad = forms.CharField(label='Unidad Base', required=False)
    class Meta:
        model = RequerimientoMaterialProveedorDetalle
        fields=(
            'material',
            'unidad',
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        materiales = kwargs.pop('materiales')
        lista_materiales = []
        for material in materiales:
            lista_materiales.append(material.id_registro)

        super(RequerimientoMaterialProveedorDetalleForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.filter(id__in = lista_materiales)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['unidad'].disabled = True
        self.fields['cantidad'].widget.attrs['min'] = 0
        self.fields['cantidad'].widget.attrs['step'] = 0.001

class RequerimientoMaterialProveedorEnviarCorreoForm(BSModalForm):
    CHOICES = (
        (1, 'a'),
        (2, 'b'),
        (3, 'c'),
    )
    correos_proveedor = forms.MultipleChoiceField(choices=CHOICES, required=False, widget=forms.CheckboxSelectMultiple())
    correos_internos = forms.MultipleChoiceField(choices=[None], required=False, widget=forms.CheckboxSelectMultiple())
    internacional_nacional = forms.ChoiceField(label = 'Internacional-Nacional', choices=INTERNACIONAL_NACIONAL, widget=forms.Select())

    class Meta:
        fields=(
            'correos_proveedor',
            'correos_internos',
            'internacional_nacional',
            )

    def clean_internacional_nacional(self):
        internacional_nacional = self.cleaned_data.get('internacional_nacional')
        if internacional_nacional==[]:
            self.add_error('internacional_nacional', 'Debe seleccionar tipo.')
    
        return internacional_nacional

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

        super(RequerimientoMaterialProveedorEnviarCorreoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['correos_internos'].choices = CORREOS_INTERNOS
        self.fields['correos_proveedor'].choices = CORREOS_PROVEEDOR
        self.fields['internacional_nacional'].choices = INTERNACIONAL_NACIONAL
        self.fields['correos_internos'].widget.attrs['class'] = 'nobull'
        self.fields['correos_proveedor'].widget.attrs['class'] = 'nobull'
