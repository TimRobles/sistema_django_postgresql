from django import forms
from django.contrib.auth import get_user_model
from applications.datos_globales.models import Departamento
from bootstrap_modal_forms.forms import BSModalModelForm
from applications.sociedad.models import Sociedad
from applications.clientes.models import Cliente
from applications.cotizacion.models import CotizacionVenta
from applications.sede.models import Sede

class ReportesFiltrosForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all())
    fecha_inicio = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=False,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado_sunat = 1))

    def __init__(self, *args, **kwargs):
        filtro_sociedad = kwargs.pop('filtro_sociedad')
        filtro_fecha_inicio = kwargs.pop('filtro_fecha_inicio')
        filtro_fecha_fin = kwargs.pop('filtro_fecha_fin')
        filtro_cliente = kwargs.pop('filtro_cliente')
        super(ReportesFiltrosForm, self).__init__(*args, **kwargs)
        self.fields['sociedad'].initial = filtro_sociedad
        self.fields['sociedad'].required = False
        self.fields['fecha_inicio'].initial = filtro_fecha_inicio
        self.fields['fecha_fin'].initial = filtro_fecha_fin
        self.fields['cliente'].initial = filtro_cliente
        self.fields['cliente'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

####################################################  REPORTES PDF  ####################################################   

class ReporteStockSociedadPdfForm(forms.Form):
    CHOICES_TIPO = [
        (1, 'STOCK DISPONIBLE'),
        (2, 'STOCK MALOGRADO'),
    ]
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=True)
    tipo = forms.ChoiceField(choices=CHOICES_TIPO, required=True)

    def __init__(self, *args, **kwargs):
        super(ReporteStockSociedadPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteVentasDepartamentoPdfForm(forms.Form):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteVentasDepartamentoPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReporteDeudasPdfForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ReporteDeudasPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
class ReporteCobranzaPdfForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ReporteCobranzaPdfForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

####################################################  REPORTES CRM  ####################################################   

class ReporteFacturacionAsesorComercialExcelForm(forms.Form):
    asesor_comercial = forms.ModelChoiceField(queryset=get_user_model().objects.filter(id__in = [cotizacion.vendedor.id for cotizacion in CotizacionVenta.objects.all()]), required=False)
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteFacturacionAsesorComercialExcelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteVentasDepartamentoExcelForm(forms.Form):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteVentasDepartamentoExcelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteFacturacionGeneralExcelForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteFacturacionGeneralExcelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteComportamientoClienteExcelForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ReporteComportamientoClienteExcelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReporteTasaConversionClienteForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
    )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteTasaConversionClienteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


####################################################  REPORTES EXCEL  ####################################################   

class ReportesContadorForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=True)
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReportesContadorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReportesRotacionForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ReportesRotacionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            
class ReporteDepositoCuentasBancariasForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=False)
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteDepositoCuentasBancariasForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReporteResumenStockProductosForm(forms.Form):
    sede = forms.ModelChoiceField(queryset=Sede.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ReporteResumenStockProductosForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReporteVentasFacturadasForm(forms.Form):
    sociedad = forms.ModelChoiceField(queryset=Sociedad.objects.all(), required=True)
    fecha_inicio = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )
    fecha_fin = forms.DateField(
        required=True,
        widget = forms.DateInput(
                attrs ={
                    'type':'date',
                    },
                format = '%Y-%m-%d',
                )
        )

    def __init__(self, *args, **kwargs):
        super(ReporteVentasFacturadasForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'