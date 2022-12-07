from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from ..material.models import ProveedorMaterial
from .models import OrdenCompra, OrdenCompraDetalle
from applications.material.models import Material


class OrdenCompraForm(BSModalModelForm):
    class Meta:
        model = OrdenCompra
        fields=(
            'moneda',
            'descuento_global',
            'total_descuento',
            'total_anticipo',
            'total_gravada',
            'total_exonerada',
            'total_igv',
            'total_gratuita',
            'total_otros_cargos',
            'total_isc',
            'total',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OrdenCompraDetalleForm(BSModalModelForm):
    class Meta:
        model = OrdenCompraDetalle
        fields=(
            'item',
            'content_type',
            'id_registro',
            'cantidad',
            'precio_unitario_sin_igv',
            'precio_unitario_con_igv',
            'precio_final_con_igv',
            'descuento',
            'sub_total',
            'igv',
            'total',
            'tipo_igv',
            'orden_compra',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraDetalleForm, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OrdenCompraEnviarCorreoForm(BSModalForm):
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

        super(OrdenCompraEnviarCorreoForm, self).__init__(*args, **kwargs)
        self.fields['correos_internos'].choices = CORREOS_INTERNOS
        self.fields['correos_proveedor'].choices = CORREOS_PROVEEDOR
        self.fields['correos_internos'].widget.attrs['class'] = 'nobull'
        self.fields['correos_proveedor'].widget.attrs['class'] = 'nobull'


class OrdenCompraAnularForm(BSModalModelForm):
    class Meta:
        model = OrdenCompra
        fields=(
            'motivo_anulacion',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraAnularForm, self).__init__(*args, **kwargs)          
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OrdenCompraDetalleUpdateForm(BSModalModelForm):
    name = forms.CharField(max_length=50)
    brand = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    class Meta:
        model = OrdenCompraDetalle
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
        super(OrdenCompraDetalleUpdateForm, self).__init__(*args, **kwargs)
        proveedor = self.instance.orden_compra.proveedor
        proveedor_material = ProveedorMaterial.objects.get(
            content_type = self.instance.content_type,
            id_registro = self.instance.id_registro,
            proveedor = proveedor,
            estado_alta_baja = 1,
        )
        self.fields['name'].initial = proveedor_material.name
        self.fields['brand'].initial = proveedor_material.brand
        self.fields['description'].initial = proveedor_material.description
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['name'].disabled = True
        self.fields['brand'].disabled = True
        self.fields['description'].disabled = True
        self.fields['precio_unitario_sin_igv'].disabled = True
        self.fields['descuento'].disabled = True
        self.fields['sub_total'].disabled = True
        self.fields['igv'].disabled = True
        self.fields['total'].disabled = True


class OrdenCompraDetalleAgregarForm(BSModalForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
    class Meta:
        model = OrdenCompraDetalle
        fields=(
            'material',
            'cantidad',
            )

    def __init__(self, *args, **kwargs):
        super(OrdenCompraDetalleAgregarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'