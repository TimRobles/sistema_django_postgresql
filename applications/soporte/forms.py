from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.forms import BSModalModelForm
from applications.variables import ESTADO_PROBLEMAS, ESTADO_SOLICITUD
from .models import (
    Problema,
    ProblemaDetalle,
    Solicitud,
    SolicitudDetalle,
)

class ProblemaBuscarForm(forms.Form): 
    titulo = forms.CharField(label = 'Titulo', max_length=100, required=False)
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADO_PROBLEMAS, required=False)
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)

 
    def __init__(self, *args, **kwargs): 
        filtro_titulo = kwargs.pop('filtro_titulo')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')

        super(ProblemaBuscarForm, self).__init__(*args, **kwargs) 
        self.fields['titulo'].initial = filtro_titulo
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario

        for visible in self.visible_fields(): 
            visible.field.widget.attrs['class'] = 'form-control' 



class ProblemaForm(BSModalModelForm):
    class Meta:
        model = Problema
        fields = (
            'titulo', 
            'descripcion'
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProblemaUpdateForm(BSModalModelForm):
    class Meta:
        model = Problema
        fields = (
            'titulo', 
            'descripcion'
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProblemaComentarioForm(BSModalModelForm):
    class Meta:
        model = Problema
        fields = (
            'comentario',
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaComentarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProblemaDetalleForm(BSModalModelForm):

    class Meta:
        model = ProblemaDetalle
        fields = (
            'imagen',
            'url',
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProblemaDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = ProblemaDetalle
        fields=(
            'imagen',
            'url',
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProblemaDetalleNotaSolucionForm(BSModalModelForm):
    class Meta:
        model = ProblemaDetalle
        fields=(
            'nota_solucion',
            )

    def __init__(self, *args, **kwargs):
        super(ProblemaDetalleNotaSolucionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SolicitudBuscarForm(forms.Form): 
    titulo = forms.CharField(label = 'Titulo', max_length=100, required=False)
    estado = forms.ChoiceField(choices=((None, '--------------------'),) + ESTADO_SOLICITUD, required=False)
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)

 
    def __init__(self, *args, **kwargs): 
        filtro_titulo = kwargs.pop('filtro_titulo')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')

        super(SolicitudBuscarForm, self).__init__(*args, **kwargs) 
        self.fields['titulo'].initial = filtro_titulo
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario

        for visible in self.visible_fields(): 
            visible.field.widget.attrs['class'] = 'form-control' 



class SolicitudForm(BSModalModelForm):
    class Meta:
        model = Solicitud
        fields = (
            'titulo', 
            'descripcion'
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudUpdateForm(BSModalModelForm):
    class Meta:
        model = Solicitud
        fields = (
            'titulo', 
            'descripcion'
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudDetalleForm(BSModalModelForm):

    class Meta:
        model = SolicitudDetalle
        fields = (
            'imagen',
            'url',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudDetalleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudDetalleUpdateForm(BSModalModelForm):
    class Meta:
        model = SolicitudDetalle
        fields=(
            'imagen',
            'url',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudDetalleUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SolicitudMotivoRechazoUpdateForm(BSModalModelForm):
    class Meta:
        model = Solicitud
        fields=(
            'motivo_rechazo',
            )

    def __init__(self, *args, **kwargs):
        super(SolicitudMotivoRechazoUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

