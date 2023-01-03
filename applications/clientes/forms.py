from datetime import date
from django import forms
from applications.datos_globales.models import Distrito
from applications.variables import TIPO_DOCUMENTO_CHOICES, TIPO_REPRESENTANTE_LEGAL_SUNAT
from applications import datos_globales
from .models import (
    Cliente,
    ClienteAnexo,
    ClienteInterlocutor,
    CorreoCliente, 
    InterlocutorCliente,
    RepresentanteLegalCliente, 
    TelefonoInterlocutorCliente,
    CorreoInterlocutorCliente,
    TipoInterlocutorCliente, 
    )

from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class ClienteForm(BSModalModelForm):
    class Meta:
        model = Cliente
        fields = (
            'tipo_documento',
            'numero_documento',
            'razon_social',
            'nombre_comercial',
            'direccion_fiscal',
            'distrito',
            'ubigeo',
            'estado_sunat',
            'condicion_sunat',
            )
        
    def clean_direccion_fiscal(self):
        direccion_fiscal = self.cleaned_data.get('direccion_fiscal')
        self.fields['distrito'].queryset = Distrito.objects.all()
        return direccion_fiscal

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        try:
            distrito = kwargs['instance'].distrito
            self.fields['distrito'].queryset = Distrito.objects.filter(codigo = distrito.codigo)
            self.fields['distrito'].initial = distrito
        except:
            self.fields['distrito'].queryset = Distrito.objects.none()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_tipo_documento(self):
        tipo_documento = self.cleaned_data.get('tipo_documento')
        if tipo_documento == '-' or tipo_documento == '0':
            self.fields['numero_documento'].required = False
            self.fields['ubigeo'].required = False
        else:
            self.fields['numero_documento'].required = True
            self.fields['ubigeo'].required = True
    
        return tipo_documento
    
    def clean_ubigeo(self):
        ubigeo = self.cleaned_data.get('ubigeo')
        try:
            datos_globales.models.Distrito.objects.get(codigo = ubigeo)
        except:
            if self.fields['ubigeo'].required:
                self.add_error('ubigeo', 'Usar un ubigeo válido')
    
        return ubigeo

    def clean(self):
        cleaned_data = super().clean()
        numero_documento = cleaned_data.get('numero_documento')
        filtro = Cliente.objects.filter(numero_documento__unaccent__iexact = numero_documento).exclude(numero_documento=None).exclude(numero_documento="")
        if numero_documento != self.instance.numero_documento:
            if len(filtro)>0:
                self.add_error('numero_documento', 'Ya existe un Cliente con este Número de documento')

class ClienteBuscarForm(forms.Form):
    razon_social = forms.CharField(label = 'Razón Social', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        filtro_razon_social = kwargs.pop('filtro_razon_social')
        super(ClienteBuscarForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].initial = filtro_razon_social
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TipoInterlocutorClienteForm(forms.ModelForm):
    class Meta:
        model = TipoInterlocutorCliente
        fields = (
            'nombre',
            )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        filtro = TipoInterlocutorCliente.objects.filter(nombre__unaccent__iexact = nombre)
        if nombre != self.instance.nombre:
            if len(filtro)>0:
                self.add_error('nombre', 'Ya existe un Tipo de Interlocutor Cliente con este nombre')

        return nombre

class InterlocutorClienteForm(BSModalForm):
    tipo_documento = forms.ChoiceField(label = 'Tipo de Documento', choices = TIPO_DOCUMENTO_CHOICES)
    numero_documento = forms.CharField(label = 'Número de Documento', max_length=15, required=False)
    nombre_completo = forms.CharField(label = 'Nombre Completo', max_length=120, required=True)
    tipo_interlocutor = forms.ModelChoiceField(label = 'Tipo de Interlocutor', queryset = TipoInterlocutorCliente.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(InterlocutorClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InterlocutorClienteUpdateForm(BSModalModelForm):
    tipo_interlocutor = forms.ModelChoiceField(label = 'Tipo de Interlocutor', queryset = TipoInterlocutorCliente.objects.all())
    class Meta:
        model = InterlocutorCliente
        fields = (
            'tipo_documento',
            'numero_documento',
            'nombre_completo',
            'tipo_interlocutor',
            )

    def __init__(self, *args, **kwargs):
        super(InterlocutorClienteUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tipo_interlocutor'].initial = self.instance.ClienteInterlocutor_interlocutor.all()[0].tipo_interlocutor
        self.fields['numero_documento'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CorreoClienteForm(BSModalModelForm):
    class Meta:
        model = CorreoCliente
        fields = (
            'correo',
            )

    def __init__(self, *args, **kwargs):
        self.lista_correos = kwargs.pop('correos')
        self.cliente_id = kwargs.pop('cliente_id')
        super(CorreoClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        filtro = CorreoCliente.objects.filter(correo__unaccent__iexact = correo, cliente = self.cliente_id, estado = 1)
        if len(self.lista_correos) < 3:
            if correo != self.instance.correo:
                if len(filtro) > 0:
                    self.add_error('correo', 'El correo ingresado ya se encuentra registrado')
        elif len(self.lista_correos) == 3:
            if (self.instance.id) in (self.lista_correos):
                if correo != self.instance.correo:
                    if len(filtro) > 0:
                        self.add_error('correo', 'El correo ingresado ya se encuentra registrado')
            else:
                self.add_error('correo', 'No se pueden registrar mas correos')

class CorreoClienteDarBajaForm(BSModalModelForm):
    class Meta:
        model = CorreoCliente
        fields = (
            'fecha_baja',
            )

        widgets = {
            'fecha_baja' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    
    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        if fecha_baja > date.today():
            self.add_error('fecha_baja', 'La fecha de baja no puede ser mayor a la fecha de hoy.')
        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(CorreoClienteDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class RepresentanteLegalClienteForm(BSModalForm):
    interlocutor = forms.ModelChoiceField(label = 'Interlocutor', queryset = InterlocutorCliente.objects.all(), required=False)
    tipo_representante_legal = forms.ChoiceField(label = 'Tipo de Representante Legal', choices = TIPO_REPRESENTANTE_LEGAL_SUNAT)
    fecha_inicio = forms.DateField(
        label = 'Fecha de Inicio',
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    
    def __init__(self, *args, **kwargs):
        lista_interlocutores = kwargs.pop('interlocutores')
        super(RepresentanteLegalClienteForm, self).__init__(*args, **kwargs)
        self.fields['interlocutor'].queryset = lista_interlocutores
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RepresentanteLegalClienteDarBajaForm(BSModalModelForm):
    class Meta:
        model = RepresentanteLegalCliente
        fields = (
            'fecha_baja',
            )

        widgets = {
            'fecha_baja' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    
    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        if fecha_baja > date.today():
            self.add_error('fecha_baja', 'La fecha de baja no puede ser mayor a la fecha de hoy.')
        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(RepresentanteLegalClienteDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class TelefonoInterlocutorForm(BSModalModelForm):
    class Meta:
        model = TelefonoInterlocutorCliente
        fields = (
            'numero',
            )
    
    def __init__(self, *args, **kwargs):
        super(TelefonoInterlocutorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['numero'].widget.attrs['placeholder'] = 'ej.: +12125552368'

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get('numero')
        filtro = TelefonoInterlocutorCliente.objects.filter(numero__unaccent__iexact = numero, estado = 1)
        if numero != self.instance.numero:
            if len(filtro)>0:
                self.add_error('numero', 'Ya existe un Teléfono con este numero')

class TelefonoInterlocutorDarBajaForm(BSModalModelForm):
    class Meta:
        model = TelefonoInterlocutorCliente
        fields = (
            'fecha_baja',
            )

        widgets = {
            'fecha_baja' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    
    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        if fecha_baja > date.today():
            self.add_error('fecha_baja', 'La fecha de baja no puede ser mayor a la fecha de hoy.')
        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(TelefonoInterlocutorDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class CorreoInterlocutorForm(BSModalModelForm):
    class Meta:
        model = CorreoInterlocutorCliente
        fields = (
            'correo',
            )

    def __init__(self, *args, **kwargs):
        super(CorreoInterlocutorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        filtro = CorreoInterlocutorCliente.objects.filter(correo__unaccent__iexact = correo, estado = 1)
        if correo != self.instance.correo:
            if len(filtro)>0:
                self.add_error('correo', 'El correo ingresado ya se encuentra registrado')

class CorreoInterlocutorDarBajaForm(BSModalModelForm):
    class Meta:
        model = CorreoInterlocutorCliente
        fields = (
            'fecha_baja',
            )

        widgets = {
            'fecha_baja' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    
    def clean_fecha_baja(self):
        fecha_baja = self.cleaned_data.get('fecha_baja')
        if fecha_baja > date.today():
            self.add_error('fecha_baja', 'La fecha de baja no puede ser mayor a la fecha de hoy.')
        return fecha_baja

    def __init__(self, *args, **kwargs):
        super(CorreoInterlocutorDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class ClienteAnexoForm(BSModalModelForm):
    ubigeo = forms.ModelChoiceField(queryset=Distrito.objects.none(), required=False)
    class Meta:
        model = ClienteAnexo
        fields = (
            'direccion',
            'ubigeo',
            )
    
    def __init__(self, *args, **kwargs):
        super(ClienteAnexoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if 'ubigeo' in self.data:
            self.fields['ubigeo'].queryset=Distrito.objects.all()



class ClienteAnexoDarBajaForm(BSModalModelForm):
    class Meta:
        model = ClienteAnexo
        fields = (
            'fecha_baja',
            )

        widgets = {
            'fecha_baja' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
            
    def __init__(self, *args, **kwargs):
        super(ClienteAnexoDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True