from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

from applications.variables import CHOICE_VACIO, ESTADOS, ESTADOS_CONFIRMACION, MESES, YEARS, TIPO_PAGO_BOLETA
from applications.material.models import Material
from applications.usuario.models import DatosUsuario
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Moneda
from .models import (
    Cheque,
    ChequeFisico,
    ChequeVueltoExtra,
    ComisionFondoPensiones,
    DatosPlanilla,
    EsSalud,
    BoletaPago,
    ReciboBoletaPago,
    Servicio,
    ReciboServicio,
    Telecredito,
    TipoServicio,
    Institucion,
    MedioPago,
    )


class ComisionFondoPensionesForm(BSModalModelForm):
    class Meta:
        model = ComisionFondoPensiones
        fields = (
            'fondo_pensiones',
            'fecha_vigencia',
            'aporte_obligatorio',
            'comision_flujo',
            'comision_flujo_mixta',
            'prima_seguro',
            )
        widgets = {
            'fecha_vigencia' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ComisionFondoPensionesForm, self).__init__(*args, **kwargs)
        if not self.fields['fecha_vigencia'].initial:
            self.fields['fecha_vigencia'].initial = date.today()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DatosPlanillaForm(BSModalModelForm):
    class Meta:
        model = DatosPlanilla
        fields = (
            'usuario',
            'sociedad',
            'fecha_inicio',
            'sueldo_bruto',
            'moneda',
            'movilidad',
            'planilla',
            'suspension_cuarta',
            'fondo_pensiones',
            'tipo_comision',
            'asignacion_familiar',
            'area',
            'cargo',
            )
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(DatosPlanillaForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = get_user_model().objects.filter(is_active=1)      
        self.fields['sociedad'].queryset = Sociedad.objects.filter(estado_sunat=1)    

        if not self.fields['fecha_inicio'].initial:
            self.fields['fecha_inicio'].initial = date.today()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['planilla'].widget.attrs['class'] = 'form-check-input'
        self.fields['suspension_cuarta'].widget.attrs['class'] = 'form-check-input'
        self.fields['asignacion_familiar'].widget.attrs['class'] = 'form-check-input'

class DatosPlanillaDarBajaForm(BSModalModelForm):
    class Meta:
        model = DatosPlanilla
        fields = (
            'fecha_baja',
            )
        widgets = {
            'fecha_baja': forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ), 
            }

    
    def __init__(self, *args, **kwargs):
        super(DatosPlanillaDarBajaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EsSaludForm(BSModalModelForm):
    class Meta:
        model = EsSalud
        fields = (
            'fecha_inicio',
            'porcentaje',
            'ley30334',
            )
        widgets = {
            'fecha_inicio' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(EsSaludForm, self).__init__(*args, **kwargs)
        if not self.fields['fecha_inicio'].initial:
            self.fields['fecha_inicio'].initial = date.today()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['ley30334'].widget.attrs['class'] = 'form-check-input'


class BoletaPagoForm(BSModalModelForm):
    class Meta:
        model = BoletaPago
        fields = (
            'datos_planilla',
            'year',
            'month',
            'tipo',
            )

    def __init__(self, *args, **kwargs):
        super(BoletaPagoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BoletaPagoActualizarForm(BSModalModelForm):
    class Meta:
        model = BoletaPago
        fields = (
            'datos_planilla',
            'year',
            'month',
            'tipo',
            'haber_mensual',
            'lic_con_goce_haber',
            'dominical',
            'movilidad',
            'asig_familiar',
            'vacaciones',
            'compra_vacaciones',
            'gratificacion',
            'ley29351',
            'cts',
            'dias_trabajados',
            'bonif_1mayo',
            'essalud',
            'aporte_obligatorio',
            'comision',
            'prima_seguro',
            'impuesto_quinta',
            'neto_recibido',
            )

    def __init__(self, *args, **kwargs):
        super(BoletaPagoActualizarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['datos_planilla'].required = False
        self.fields['datos_planilla'].disabled = True


class ReciboBoletaPagoForm(BSModalModelForm):
    class Meta:
        model = ReciboBoletaPago
        fields = (
            'boleta_pago',
            'fecha_pagar',
            'tipo_pago',
            )
        widgets = {
            'fecha_pagar' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    def __init__(self, *args, **kwargs):
        super(ReciboBoletaPagoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReciboBoletaPagoActualizarForm(BSModalModelForm):
    class Meta:
        model = ReciboBoletaPago
        fields = (
            'boleta_pago',
            'fecha_pagar',
            'tipo_pago',
            'monto',
            )
        widgets = {
            'fecha_pagar' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    def __init__(self, *args, **kwargs):
        super(ReciboBoletaPagoActualizarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ServicioForm(BSModalModelForm):
    class Meta:
        model = Servicio
        fields = (
            'institucion',
            'tipo_servicio',
            'numero_referencia',
            'titular_servicio',
            'direccion',
            'alias',
            'sociedad',
            )

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReciboServicioForm(BSModalModelForm):
    class Meta:
        model = ReciboServicio
        fields = (
            'servicio',
            'foto',
            'fecha_emision',
            'fecha_vencimiento',
            'monto',
            'moneda',
            )
        widgets = {
            'fecha_emision' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            'fecha_vencimiento' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }
    def __init__(self, *args, **kwargs):
        super(ReciboServicioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TipoServicioForm(BSModalModelForm):
    class Meta:
        model = TipoServicio
        fields = (
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InstitucionForm(BSModalModelForm):
    class Meta:
        model = Institucion
        fields = (
            'nombre',
            'url',
            'tipo_servicio',
            'medio_pago',
            )

    def __init__(self, *args, **kwargs):
        super(InstitucionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class MedioPagoForm(BSModalModelForm):
    class Meta:
        model = MedioPago
        fields = (
            'nombre',
            )

    def __init__(self, *args, **kwargs):
        super(MedioPagoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChequeForm(BSModalModelForm):
    class Meta:
        model = Cheque
        fields = (
            'concepto',
            'moneda',
            'monto_cheque',
            # 'usuario',
            )

    def clean_monto(self):
        monto_cheque = self.cleaned_data.get('monto_cheque')

        if monto_cheque  <= 0:
            self.add_error('monto_cheque', "El monto debe ser mayor a cero.")
    
        return monto_cheque

    def __init__(self, *args, **kwargs):
        super(ChequeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True


class ChequeReciboBoletaPagoAgregarForm(BSModalForm):
    recibo_boleta_pago = forms.ModelChoiceField(queryset=None)

    class Meta:
        fields=(
            'recibo_boleta_pago',
            )

    def __init__(self, *args, **kwargs):
        lista_recibos = kwargs.pop('recibos')
        super(ChequeReciboBoletaPagoAgregarForm, self).__init__(*args, **kwargs)
        self.fields['recibo_boleta_pago'].queryset = lista_recibos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            

class ChequeReciboBoletaPagoUpdateForm(BSModalModelForm):
    class Meta:
        model = ReciboBoletaPago
        fields = (
            'monto_pagado',
            'fecha_pago',
            'voucher',
            )

        widgets = {
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    # 'required':'required',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ChequeReciboBoletaPagoUpdateForm, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChequeReciboServicioAgregarForm(BSModalForm):
    recibo_servicio = forms.ModelChoiceField(queryset=None)

    class Meta:
        fields=(
            'recibo_servicio',
            )

    def __init__(self, *args, **kwargs):
        lista_recibos = kwargs.pop('recibos')
        super(ChequeReciboServicioAgregarForm, self).__init__(*args, **kwargs)
        self.fields['recibo_servicio'].queryset = lista_recibos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChequeReciboServicioUpdateForm(BSModalModelForm):
    class Meta:
        model = ReciboServicio
        fields = (
            'monto_pagado',
            'fecha_pago',
            'voucher',
            )

        widgets = {
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    # 'required':'required',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ChequeReciboServicioUpdateForm, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChequeReciboCajaChicaAgregarForm(BSModalForm):
    recibo_caja_chica = forms.ModelChoiceField(queryset=None)

    class Meta:
        fields=(
            'recibo_caja_chica',
            )

    def __init__(self, *args, **kwargs):
        lista_recibos = kwargs.pop('recibos')
        super(ChequeReciboCajaChicaAgregarForm, self).__init__(*args, **kwargs)
        self.fields['recibo_caja_chica'].queryset = lista_recibos
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChequeFisicoForm(BSModalModelForm):
    class Meta:
        model = ChequeFisico
        fields = (
            'banco',
            'numero',
            'responsable',
            'monto',
            'fecha_emision',
            'foto',
            'sociedad',
            )
        widgets = {
            'fecha_emision' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ChequeFisicoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True


class ChequeFisicoCobrarForm(BSModalModelForm):
    class Meta:
        model = ChequeFisico
        fields = (
            'comision',
            'monto_recibido',
            'fecha_cobro',
            )
        widgets = {
            'fecha_cobro' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(ChequeFisicoCobrarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = True

class ChequeVueltoExtraForm(BSModalModelForm):
    moneda_cheque = forms.ModelChoiceField(queryset=Moneda.objects.all())
    class Meta:
        model = ChequeVueltoExtra
        fields = (
            'vuelto_original', 
            'moneda', 
            'tipo_cambio', 
            'vuelto_extra', 
            'moneda_cheque', 
            )

    def __init__(self, *args, **kwargs):
        moneda_cheque = kwargs.pop('moneda_cheque')
        super(ChequeVueltoExtraForm, self).__init__(*args, **kwargs)
        self.fields['moneda_cheque'].initial = moneda_cheque
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        for field in self.fields:
            self.fields[field].required = True
        

class TelecreditoForm(BSModalModelForm):
    class Meta:
        model = Telecredito
        fields = (
            'banco',
            'concepto',
            'numero',
            'fecha_emision',
            'sociedad',
            )

        widgets = {
            'fecha_emision' : forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(TelecreditoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TelecreditoReciboPagoForm(BSModalModelForm):
    recibo_boleta_pago = forms.ModelChoiceField(queryset=ReciboBoletaPago.objects.filter(id_registro=None), required=True)
    class Meta:
        model = ReciboBoletaPago
        fields = (
            'recibo_boleta_pago',
            )

    def __init__(self, *args, **kwargs):
        super(TelecreditoReciboPagoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TelecreditoReciboPagoUpdateForm(BSModalModelForm):
    class Meta:
        model = ReciboBoletaPago
        fields = (
            'monto_pagado',
            'fecha_pago',
            'voucher',
            )

        widgets = {
            'fecha_pago' : forms.DateInput(
                attrs ={
                    'type':'date',
                    # 'required':'required',
                    },
                format = '%Y-%m-%d',
                ),
            }

    def __init__(self, *args, **kwargs):
        super(TelecreditoReciboPagoUpdateForm, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BoletaPagoBuscarForm(forms.Form):
    year = forms.ChoiceField(choices=CHOICE_VACIO + YEARS, required=False)
    month = forms.ChoiceField(choices=CHOICE_VACIO + MESES, required=False)
    tipo = forms.ChoiceField(choices=CHOICE_VACIO + TIPO_PAGO_BOLETA, required=False)
    estado = forms.ChoiceField(choices=CHOICE_VACIO + ESTADOS, required=False)
    usuario = forms.ModelChoiceField(queryset=get_user_model().objects, required=False)
    
    def __init__(self, *args, **kwargs):
        filtro_year = kwargs.pop('filtro_year')
        filtro_month = kwargs.pop('filtro_month')
        filtro_tipo = kwargs.pop('filtro_tipo')
        filtro_estado = kwargs.pop('filtro_estado')
        filtro_usuario = kwargs.pop('filtro_usuario')
        super(BoletaPagoBuscarForm, self).__init__(*args, **kwargs)
        self.fields['year'].initial = filtro_year
        self.fields['month'].initial = filtro_month
        self.fields['tipo'].initial = filtro_tipo
        self.fields['estado'].initial = filtro_estado
        self.fields['usuario'].initial = filtro_usuario
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'