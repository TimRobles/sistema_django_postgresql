from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
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
    
    class Meta:
        model = OfertaProveedorDetalle
        fields=(
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
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




# class MaterialOfertaProveedorForm(BSModalForm):
#     material = forms.ModelChoiceField(queryset=None)
#     cantidad = forms.DecimalField(max_digits=22, decimal_places=10)
#     class Meta:
#         model = RequerimientoMaterialProveedorDetalle
#         fields=(
#             'material',
#             'cantidad',
#             )
    
#     def __init__(self, *args, **kwargs):
#         materiales = kwargs.pop('materiales')
#         lista_materiales = []
#         for material in materiales:
#             lista_materiales.append(material.id_registro)

#         super(RequerimientoMaterialProveedorDetalleForm, self).__init__(*args, **kwargs)
#         self.fields['material'].queryset = Material.objects.filter(id__in = lista_materiales)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'




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