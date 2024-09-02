from decimal import Decimal
from re import template
from django.db import models
from django.shortcuts import render
from django.core.paginator import Paginator
from applications.caja_chica.funciones import cheque_monto_usado
from applications.contabilidad.funciones import calcular_datos_boleta, movimientos_cheque, movimientos_telecredito
from applications.contabilidad.pdf import generarChequeCerrarPdf, generarChequeSolicitarPdf, generarTelecreditoCerrarPdf, generarTelecreditoSolicitarPdf
from applications.datos_globales.models import RemuneracionMinimaVital
from applications.funciones import registrar_excepcion
from applications.home.templatetags.funciones_propias import nombre_usuario
from django.template.defaultfilters import date as _date

from applications.importaciones import *
from applications.funciones import registrar_excepcion
from applications.caja_chica.models import ReciboCajaChica, Requerimiento
from applications.sociedad.models import Sociedad

from .forms import(
    BoletaPagoBuscarForm,
    ChequeCerrarForm,
    ChequeFisicoCobrarForm,
    ChequeFisicoForm,
    ChequeForm,
    ChequeReciboBoletaPagoAgregarForm,
    ChequeReciboBoletaPagoUpdateForm,
    ChequeReciboCajaChicaAgregarForm,
    ChequeReciboCajaChicaUpdateForm,
    ChequeReciboServicioAgregarForm,
    ChequeReciboServicioUpdateForm,
    ChequeVueltoExtraForm,
    ComisionFondoPensionesForm,
    DatosPlanillaForm,
    DatosPlanillaDarBajaForm,
    EsSaludForm,
    BoletaPagoForm,
    BoletaPagoActualizarForm,
    InstitucionBuscarForm,
    ReciboBoletaPagoForm,
    ReciboBoletaPagoActualizarForm,
    ServicioBuscarForm,
    ServicioForm,
    ReciboServicioForm,
    TelecreditoCobrarForm,
    TelecreditoForm,
    TelecreditoReciboPagoForm,
    TelecreditoReciboPagoUpdateForm,
    TipoServicioForm,
    InstitucionForm,
    MedioPagoForm,
    ServicioDarBajaForm,
)

from .models import(
    Cheque,
    ChequeFisico,
    ChequeVueltoExtra,
    FondoPensiones,
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

class ComisionFondoPensionesListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_comisionfondopensiones')
    template_name = "contabilidad/comision_fondo_pensiones/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesListView, self).get_context_data(**kwargs)
        comision = ComisionFondoPensiones.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(comision) > objectsxpage:
            paginator = Paginator(comision, objectsxpage)
            page_number = self.request.GET.get('page')
            comision = paginator.get_page(page_number)

        context['contexto_comision'] = comision
        context['contexto_pagina'] = comision
        context['contexto_filtro'] = '?'
        return context

def ComisionFondoPensionesTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/comision_fondo_pensiones/inicio_tabla.html'
        context = {}
        comision = ComisionFondoPensiones.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(comision) > objectsxpage:
            paginator = Paginator(comision, objectsxpage)
            page_number = request.GET.get('page')
            comision = paginator.get_page(page_number)

        context['contexto_comision'] = comision
        context['contexto_pagina'] = comision
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ComisionFondoPensionesCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_comisionfondopensiones')
    model = ComisionFondoPensiones
    template_name = "includes/formulario generico.html"
    form_class = ComisionFondoPensionesForm
    success_url = reverse_lazy('contabilidad_app:comision_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Comision Fondo Pensiones"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ComisionFondoPensionesUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_comisionfondopensiones')
    model = ComisionFondoPensiones
    template_name = "includes/formulario generico.html"
    form_class = ComisionFondoPensionesForm
    success_url = reverse_lazy('contabilidad_app:comision_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Comisiones"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ComisionFondoPensionesDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_comisionfondopensiones')
    model = ComisionFondoPensiones
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('contabilidad_app:comision_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Comisiones"
        return context

#---------------------------------------------------------------------------------

class DatosPlanillaListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_datosplanilla')
    template_name = "contabilidad/datos_planilla/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaListView, self).get_context_data(**kwargs)
        datos_planilla = DatosPlanilla.objects.all()
        objectsxpage =  20 # Show 20 objects per page.

        if len(datos_planilla) > objectsxpage:
            paginator = Paginator(datos_planilla, objectsxpage)
            page_number = self.request.GET.get('page')
            datos_planilla = paginator.get_page(page_number)

        context['contexto_datos_planilla'] = datos_planilla
        context['contexto_pagina'] = datos_planilla
        context['contexto_filtro'] = '?'
        return context

def DatosPlanillaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/datos_planilla/inicio_tabla.html'
        context = {}
        datos_planilla = DatosPlanilla.objects.all()
        objectsxpage =  20 # Show 20 objects per page.

        if len(datos_planilla) > objectsxpage:
            paginator = Paginator(datos_planilla, objectsxpage)
            page_number = request.GET.get('page')
            datos_planilla = paginator.get_page(page_number)

        context['contexto_datos_planilla'] = datos_planilla
        context['contexto_pagina'] = datos_planilla
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class DatosPlanillaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_datosplanilla')
    model = DatosPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosPlanillaForm
    success_url = reverse_lazy('contabilidad_app:datos_planilla_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Datos Planilla"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class DatosPlanillaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_datosplanilla')

    model = DatosPlanilla
    template_name = "contabilidad/datos_planilla/form.html"
    form_class = DatosPlanillaForm
    success_url = reverse_lazy('contabilidad_app:datos_planilla_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.estado = 1
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Datos Planilla'
        return context

class DatosPlanillaDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_datosplanilla')
    model = DatosPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosPlanillaDarBajaForm
    success_url = reverse_lazy('contabilidad_app:datos_planilla_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'Datos Planilla'
        return context

#---------------------------------------------------------------------------------

class EsSaludListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_essalud')
    template_name = "contabilidad/essalud/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(EsSaludListView, self).get_context_data(**kwargs)
        essalud = EsSalud.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(essalud) > objectsxpage:
            paginator = Paginator(essalud, objectsxpage)
            page_number = self.request.GET.get('page')
            essalud = paginator.get_page(page_number)

        context['contexto_essalud'] = essalud
        context['contexto_pagina'] = essalud
        context['contexto_filtro'] = '?'
        return context

def EsSaludTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/essalud/inicio_tabla.html'
        context = {}
        essalud = EsSalud.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(essalud) > objectsxpage:
            paginator = Paginator(essalud, objectsxpage)
            page_number = request.GET.get('page')
            essalud = paginator.get_page(page_number)

        context['contexto_essalud'] = essalud
        context['contexto_pagina'] = essalud
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class EsSaludCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_essalud')
    model = EsSalud
    template_name = "includes/formulario generico.html"
    form_class = EsSaludForm
    success_url = reverse_lazy('contabilidad_app:essalud_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EsSaludCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Datos Planilla"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class EsSaludUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_essalud')
    model = EsSalud
    template_name = "contabilidad/essalud/form.html"
    form_class = EsSaludForm
    success_url = reverse_lazy('contabilidad_app:essalud_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
       
    def form_valid(self, form):
        form.instance.estado = 1
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(EsSaludUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'EsSalud'
        return context

#---------------------------------------------------------------------------------

class BoletaPagoListView(PermissionRequiredMixin, FormView):
    permission_required = ('contabilidad.view_boletapago')

    form_class = BoletaPagoBuscarForm
    template_name = "contabilidad/boleta_pago/inicio.html"

    def get_form_kwargs(self):
        kwargs = super(BoletaPagoListView, self).get_form_kwargs()
        kwargs['filtro_year'] = self.request.GET.get('year')
        kwargs['filtro_month'] = self.request.GET.get('month')
        kwargs['filtro_tipo'] = self.request.GET.get('tipo')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_usuario'] = self.request.GET.get('usuario')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(BoletaPagoListView, self).get_context_data(**kwargs)
        boleta_pago = BoletaPago.objects.all()

        filtro_year = self.request.GET.get('year')
        filtro_month = self.request.GET.get('month')
        filtro_tipo = self.request.GET.get('tipo')
        filtro_estado = self.request.GET.get('estado')
        filtro_usuario = self.request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_year:
            condicion = Q(year = filtro_year)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"year={filtro_year}")

        if filtro_month:
            condicion = Q(month = filtro_month)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"month={filtro_month}")

        if filtro_tipo:
            condicion = Q(tipo = filtro_tipo)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"tipo={filtro_tipo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(datos_planilla__usuario = filtro_usuario)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  20 # Show 20 objects per page.

        if len(boleta_pago) > objectsxpage:
            paginator = Paginator(boleta_pago, objectsxpage)
            page_number = self.request.GET.get('page')
            boleta_pago = paginator.get_page(page_number)

        context['contexto_boleta_pago'] = boleta_pago
        context['contexto_pagina'] = boleta_pago
        return context

def BoletaPagoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/boleta_pago/inicio_tabla.html'
        context = {}
        boleta_pago = BoletaPago.objects.all()
        
        filtro_year = request.GET.get('year')
        filtro_month = request.GET.get('month')
        filtro_tipo = request.GET.get('tipo')
        filtro_estado = request.GET.get('estado')
        filtro_usuario = request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_year:
            condicion = Q(year = filtro_year)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"year={filtro_year}")

        if filtro_month:
            condicion = Q(month = filtro_month)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"month={filtro_month}")

        if filtro_tipo:
            condicion = Q(tipo = filtro_tipo)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"tipo={filtro_tipo}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(datos_planilla__usuario = filtro_usuario)
            boleta_pago = boleta_pago.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  20 # Show 20 objects per page.

        if len(boleta_pago) > objectsxpage:
            paginator = Paginator(boleta_pago, objectsxpage)
            page_number = request.GET.get('page')
            boleta_pago = paginator.get_page(page_number)

        context['contexto_boleta_pago'] = boleta_pago
        context['contexto_pagina'] = boleta_pago

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class BoletaPagoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_boletapago')
    model = BoletaPago
    template_name = "contabilidad/boleta_pago/form crear.html"
    form_class = BoletaPagoForm
    success_url = reverse_lazy('contabilidad_app:boleta_pago_inicio')

    def get_context_data(self, **kwargs):
        context = super(BoletaPagoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Boleta de Pago"
        return context

    def form_valid(self, form):
        calcular_datos_boleta(form.instance)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class BoletaPagoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_boletapago')
    model = BoletaPago
    template_name = "contabilidad/boleta_pago/form.html"
    form_class = BoletaPagoActualizarForm
    success_url = reverse_lazy('contabilidad_app:boleta_pago_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        boleta = self.get_object()
        context = super(BoletaPagoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Boleta de Pago'
        fecha_boleta = date(boleta.year, boleta.month, 1)
        if boleta.datos_planilla.fondo_pensiones:
            comision_fondo_pensiones = boleta.datos_planilla.fondo_pensiones.ComisionFondoPensiones_fondo_pensiones.filter(fecha_vigencia__lte=fecha_boleta).latest('fecha_vigencia')
            aporte_obligatorio = comision_fondo_pensiones.aporte_obligatorio
            comision_flujo_mixta = comision_fondo_pensiones.comision_flujo_mixta
            comision_flujo = comision_fondo_pensiones.comision_flujo
            prima_seguro = comision_fondo_pensiones.prima_seguro
        else:
            aporte_obligatorio = Decimal('0.00')
            comision_flujo_mixta = Decimal('0.00')
            comision_flujo = Decimal('0.00')
            prima_seguro = Decimal('0.00')
        context['aporte_obligatorio'] = aporte_obligatorio
        context['comision_flujo_mixta'] = comision_flujo_mixta
        context['comision_flujo'] = comision_flujo
        context['prima_seguro'] = prima_seguro
        context['tipo_comision'] = boleta.datos_planilla.tipo_comision
        context['rmv'] = RemuneracionMinimaVital.objects.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio').monto
        context['essalud'] = EsSalud.objects.filter(fecha_inicio__lte=fecha_boleta).latest('fecha_inicio').porcentaje
        context['asignacion_familiar'] = boleta.datos_planilla.asignacion_familiar
        context['movilidad'] = boleta.datos_planilla.movilidad
        context['planilla'] = boleta.datos_planilla.planilla
        return context

class BoletaPagoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_boletapago')
    model = BoletaPago
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:boleta_pago_inicio')

    def get_context_data(self, **kwargs):
        context = super(BoletaPagoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Boleta'
        context['item'] = self.get_object()
        return context

class BoletaPagoDetailView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_boletapago')
    template_name = "contabilidad/boleta_pago/boleta de pago.html"
    
    def get_context_data(self, **kwargs):
        context = super(BoletaPagoDetailView, self).get_context_data(**kwargs)
        boleta = BoletaPago.objects.get(pk=kwargs['pk'])
        
        context['boleta'] = boleta
        context['titulo'] = "Boleta de Pago - %s - %s" % (nombre_usuario(boleta.datos_planilla.usuario), boleta.periodo)
        context['previous'] = reverse_lazy('contabilidad:boleta_pago_inicio')
        return context
#---------------------------------------------------------------------------------

class ReciboBoletaPagoListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_reciboboletapago')
    template_name = "contabilidad/recibo_boleta_pago/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReciboBoletaPagoListView, self).get_context_data(**kwargs)
        recibo_boleta_pago = ReciboBoletaPago.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(recibo_boleta_pago) > objectsxpage:
            paginator = Paginator(recibo_boleta_pago, objectsxpage)
            page_number = self.request.GET.get('page')
            recibo_boleta_pago = paginator.get_page(page_number)

        context['contexto_recibo_boleta_pago'] = recibo_boleta_pago
        context['contexto_pagina'] = recibo_boleta_pago
        context['contexto_filtro'] = '?'
        return context

def ReciboBoletaPagoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/recibo_boleta_pago/inicio_tabla.html'
        context = {}
        recibo_boleta_pago = ReciboBoletaPago.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(recibo_boleta_pago) > objectsxpage:
            paginator = Paginator(recibo_boleta_pago, objectsxpage)
            page_number = request.GET.get('page')
            recibo_boleta_pago = paginator.get_page(page_number)

        context['contexto_recibo_boleta_pago'] = recibo_boleta_pago
        context['contexto_pagina'] = recibo_boleta_pago
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ReciboBoletaPagoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_reciboboletapago')
    model = ReciboBoletaPago
    template_name = "includes/formulario generico.html"
    form_class = ReciboBoletaPagoForm
    success_url = reverse_lazy('contabilidad_app:recibo_boleta_pago_inicio')

    def get_context_data(self, **kwargs):
        context = super(ReciboBoletaPagoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Recibo Boleta de Pago"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ReciboBoletaPagoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_reciboboletapago')
    model = ReciboBoletaPago
    template_name = "contabilidad/recibo_boleta_pago/form.html"
    form_class = ReciboBoletaPagoActualizarForm
    success_url = reverse_lazy('contabilidad_app:recibo_boleta_pago_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ReciboBoletaPagoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Boleta de Pago"
        return context

class ReciboBoletaPagoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_reciboboletapago')
    model = ReciboBoletaPago
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:boleta_pago_inicio')

    def get_context_data(self, **kwargs):
        context = super(ReciboBoletaPagoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Recibo'
        context['item'] = self.get_object()
        return context

#---------------------------------------------------------------------------------

class ServicioListView(PermissionRequiredMixin, FormView):
    permission_required = ('contabilidad.view_servicio')
    form_class = ServicioBuscarForm
    template_name = "contabilidad/servicio/inicio.html"

    def get_form_kwargs(self):
        kwargs = super(ServicioListView, self).get_form_kwargs()
        kwargs['filtro_institucion'] = self.request.GET.get('institucion')
        kwargs['filtro_tipo_servicio'] = self.request.GET.get('tipo_servicio')
        kwargs['filtro_numero_referencia'] = self.request.GET.get('numero_referencia')
        kwargs['filtro_titular_servicio'] = self.request.GET.get('titular_servicio')
        kwargs['filtro_alias'] = self.request.GET.get('alias')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ServicioListView, self).get_context_data(**kwargs)
        servicio = Servicio.objects.all().order_by('estado')

        filtro_institucion = self.request.GET.get('institucion')
        filtro_tipo_servicio = self.request.GET.get('tipo_servicio')
        filtro_numero_referencia = self.request.GET.get('numero_referencia')
        filtro_titular_servicio = self.request.GET.get('titular_servicio')
        filtro_alias = self.request.GET.get('alias')
        filtro_estado = self.request.GET.get('estado')
        filtro_sociedad = self.request.GET.get('sociedad')
        
        contexto_filtro = []

        if filtro_institucion:
            condicion = Q(institucion = filtro_institucion)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"institucion={filtro_institucion}")

        if filtro_tipo_servicio:
            condicion = Q(tipo_servicio = filtro_tipo_servicio)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"tipo_servicio={filtro_tipo_servicio}")

        if filtro_numero_referencia:
            condicion = Q(numero_referencia__unaccent__icontains = filtro_numero_referencia.split(" ")[0])
            for palabra in filtro_numero_referencia.split(" ")[1:]:
                condicion &= Q(numero_referencia__unaccent__icontains = palabra)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"numero_referencia={filtro_numero_referencia}")

        if filtro_titular_servicio:
            condicion = Q(titular_servicio__unaccent__icontains = filtro_titular_servicio.split(" ")[0])
            for palabra in filtro_titular_servicio.split(" ")[1:]:
                condicion &= Q(titular_servicio__unaccent__icontains = palabra)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"titular_servicio={filtro_titular_servicio}")

        if filtro_alias:
            condicion = Q(alias__unaccent__icontains = filtro_alias.split(" ")[0])
            for palabra in filtro_alias.split(" ")[1:]:
                condicion &= Q(alias__unaccent__icontains = palabra)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"alias={filtro_alias}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_sociedad:
            ids = []
            for nota in servicio.all():
                if str(nota.sociedad.id) == filtro_sociedad:
                    ids.append(nota.id)
            servicio = servicio.filter(id__in = ids)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  25 # Show 25 objects per page.

        if len(servicio) > objectsxpage:
            paginator = Paginator(servicio, objectsxpage)
            page_number = self.request.GET.get('page')
            servicio = paginator.get_page(page_number)

        context['contexto_servicio'] = servicio
        context['contexto_pagina'] = servicio
        return context

def ServicioTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/servicio/inicio_tabla.html'
        context = {}
        servicio = Servicio.objects.all().order_by('estado')
        
        filtro_institucion = request.GET.get('institucion')
        filtro_tipo_servicio = request.GET.get('tipo_servicio')
        filtro_numero_referencia = request.GET.get('numero_referencia')
        filtro_titular_servicio = request.GET.get('titular_servicio')
        filtro_alias = request.GET.get('alias')
        filtro_estado = request.GET.get('estado')
        filtro_sociedad = request.GET.get('sociedad')
        
        contexto_filtro = []

        if filtro_institucion:
            condicion = Q(institucion = filtro_institucion)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"institucion={filtro_institucion}")

        if filtro_tipo_servicio:
            condicion = Q(tipo_servicio = filtro_tipo_servicio)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"tipo_servicio={filtro_tipo_servicio}")

        if filtro_numero_referencia:
            condicion = Q(numero_referencia__unaccent__icontains = filtro_numero_referencia.split(" ")[0])
            for palabra in filtro_numero_referencia.split(" ")[1:]:
                condicion &= Q(numero_referencia__unaccent__icontains = palabra)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"numero_referencia={filtro_numero_referencia}")

        if filtro_titular_servicio:
            condicion = Q(titular_servicio__unaccent__icontains = filtro_titular_servicio.split(" ")[0])
            for palabra in filtro_titular_servicio.split(" ")[1:]:
                condicion &= Q(titular_servicio__unaccent__icontains = palabra)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"titular_servicio={filtro_titular_servicio}")

        if filtro_alias:
            condicion = Q(alias__unaccent__icontains = filtro_alias.split(" ")[0])
            for palabra in filtro_alias.split(" ")[1:]:
                condicion &= Q(alias__unaccent__icontains = palabra)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"alias={filtro_alias}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            servicio = servicio.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_sociedad:
            ids = []
            for nota in servicio.all():
                if str(nota.sociedad.id) == filtro_sociedad:
                    ids.append(nota.id)
            servicio = servicio.filter(id__in = ids)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  25 # Show 25 objects per page.

        if len(servicio) > objectsxpage:
            paginator = Paginator(servicio, objectsxpage)
            page_number = request.GET.get('page')
            servicio = paginator.get_page(page_number)

        context['contexto_servicio'] = servicio
        context['contexto_pagina'] = servicio

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ServicioCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_servicio')
    model = Servicio
    template_name = "includes/formulario generico.html"
    form_class = ServicioForm
    success_url = reverse_lazy('contabilidad_app:servicio_inicio')

    def get_context_data(self, **kwargs):
        context = super(ServicioCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Servicio"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ServicioUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_servicio')
    model = Servicio
    template_name = "contabilidad/servicio/form.html"
    form_class = ServicioForm
    success_url = reverse_lazy('contabilidad_app:servicio_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ServicioUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Servicio"
        return context


class ServicioDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_servicio')
    model = Servicio
    template_name = "includes/formulario generico.html"
    form_class = ServicioDarBajaForm
    success_url = reverse_lazy('contabilidad_app:servicio_inicio')


    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ServicioDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'Servicio'
        return context


#---------------------------------------------------------------------------------

class ReciboServicioListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_reciboservicio')
    
    template_name = "contabilidad/recibo_servicio/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReciboServicioListView, self).get_context_data(**kwargs)
        recibo_servicio = ReciboServicio.objects.all()
        objectsxpage =  25 # Show 25 objects per page.

        if len(recibo_servicio) > objectsxpage:
            paginator = Paginator(recibo_servicio, objectsxpage)
            page_number = self.request.GET.get('page')
            recibo_servicio = paginator.get_page(page_number)

        context['contexto_recibo_servicio'] = recibo_servicio
        context['contexto_pagina'] = recibo_servicio
        context['contexto_filtro'] = '?'
        return context

def ReciboServicioTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/recibo_servicio/inicio_tabla.html'
        context = {}
        recibo_servicio = ReciboServicio.objects.all()
        objectsxpage =  25 # Show 25 objects per page.

        if len(recibo_servicio) > objectsxpage:
            paginator = Paginator(recibo_servicio, objectsxpage)
            page_number = request.GET.get('page')
            recibo_servicio = paginator.get_page(page_number)

        context['contexto_recibo_servicio'] = recibo_servicio
        context['contexto_pagina'] = recibo_servicio
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ReciboServicioCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_reciboservicio')
    model = ReciboServicio
    template_name = "includes/formulario generico.html"
    form_class = ReciboServicioForm
    success_url = reverse_lazy('contabilidad_app:recibo_servicio_inicio')

    def get_context_data(self, **kwargs):
        context = super(ReciboServicioCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Recibo Servicio"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ReciboServicioUpdateView(BSModalUpdateView):
    permission_required = ('contabilidad.change_reciboservicio')
    model = ReciboServicio
    template_name = "contabilidad/recibo_servicio/form.html"
    form_class = ReciboServicioForm
    success_url = reverse_lazy('contabilidad_app:recibo_servicio_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ReciboServicioUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Servicio"
        return context

class ReciboServicioDeleteView(BSModalDeleteView):
    permission_required = ('contabilidad.delete_reciboservicio')
    model = ReciboServicio
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:recibo_servicio_inicio')

    def get_context_data(self, **kwargs):
        context = super(ReciboServicioDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Recibo de Servicio'
        context['item'] = self.get_object()
        return context


#---------------------------------------------------------------------------------

class TipoServicioListView(TemplateView):
    permission_required = ('contabilidad.view_tiposervicio')
    template_name = "contabilidad/tipo_servicio/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(TipoServicioListView, self).get_context_data(**kwargs)
        tipo_servicio = TipoServicio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_servicio) > objectsxpage:
            paginator = Paginator(tipo_servicio, objectsxpage)
            page_number = self.request.GET.get('page')
            tipo_servicio = paginator.get_page(page_number)

        context['contexto_tipo_servicio'] = tipo_servicio
        context['contexto_pagina'] = tipo_servicio
        context['contexto_filtro'] = '?'
        return context

def TipoServicioTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/tipo_servicio/inicio_tabla.html'
        context = {}
        tipo_servicio = TipoServicio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(tipo_servicio) > objectsxpage:
            paginator = Paginator(tipo_servicio, objectsxpage)
            page_number = request.GET.get('page')
            tipo_servicio = paginator.get_page(page_number)

        context['contexto_tipo_servicio'] = tipo_servicio
        context['contexto_pagina'] = tipo_servicio
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TipoServicioCreateView(BSModalCreateView):
    permission_required = ('contabilidad.add_tiposervicio')
    model = TipoServicio
    template_name = "includes/formulario generico.html"
    form_class = TipoServicioForm
    success_url = reverse_lazy('contabilidad_app:tipo_servicio_inicio')

    def get_context_data(self, **kwargs):
        context = super(TipoServicioCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Tipo de Servicio"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class TipoServicioUpdateView(BSModalUpdateView):
    permission_required = ('contabilidad.change_tiposervicio')
    model = TipoServicio
    template_name = "contabilidad/tipo_servicio/form.html"
    form_class = TipoServicioForm
    success_url = reverse_lazy('contabilidad_app:tipo_servicio_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TipoServicioUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tipo de Servicio"
        return context


#---------------------------------------------------------------------------------

class InstitucionListView(FormView):
    permission_required = ('contabilidad.view_institucion')
    template_name = "contabilidad/institucion/inicio.html"
    form_class = InstitucionBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(InstitucionListView, self).get_form_kwargs()
        kwargs['filtro_nombre'] = self.request.GET.get('nombre')
        kwargs['filtro_tipo_servicio'] = self.request.GET.get('tipo_servicio')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(InstitucionListView, self).get_context_data(**kwargs)
        institucion = Institucion.objects.all()

        filtro_nombre = self.request.GET.get('nombre')
        filtro_tipo_servicio = self.request.GET.get('tipo_servicio')

        contexto_filtro = []

        if filtro_nombre:
            condicion = Q(nombre__razon_social__unaccent__icontains = filtro_nombre.split(" ")[0])
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__razon_social__unaccent__icontains = palabra)
            institucion = institucion.filter(condicion)
            contexto_filtro.append("nombre=" + filtro_nombre)

        if filtro_tipo_servicio:
            condicion = Q(tipo_servicio = filtro_tipo_servicio)
            institucion = institucion.filter(condicion)
            contexto_filtro.append("tipo_servicio=" + filtro_tipo_servicio)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  30 # Show 10 objects per page.

        if len(institucion) > objectsxpage:
            paginator = Paginator(institucion, objectsxpage)
            page_number = self.request.GET.get('page')
            institucion = paginator.get_page(page_number)
   
        context['contexto_institucion'] = institucion
        context['contexto_pagina'] = institucion
        return context

def InstitucionTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/institucion/inicio_tabla.html'
        context = {}
        institucion = Institucion.objects.all()

        filtro_nombre = request.GET.get('nombre')
        filtro_tipo_servicio = request.GET.get('tipo_servicio')

        contexto_filtro = []

        if filtro_nombre:
            condicion = Q(nombre__razon_social__unaccent__icontains = filtro_nombre.split(" ")[0])
            for palabra in filtro_nombre.split(" ")[1:]:
                condicion &= Q(nombre__razon_social__unaccent__icontains = palabra)
            institucion = institucion.filter(condicion)
            contexto_filtro.append("nombre=" + filtro_nombre)

        if filtro_tipo_servicio:
            condicion = Q(tipo_servicio = filtro_tipo_servicio)
            institucion = institucion.filter(condicion)
            contexto_filtro.append("tipo_servicio=" + filtro_tipo_servicio)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  30 # Show 10 objects per page.

        if len(institucion) > objectsxpage:
            paginator = Paginator(institucion, objectsxpage)
            page_number = request.GET.get('page')
            institucion = paginator.get_page(page_number)
   
        context['contexto_institucion'] = institucion
        context['contexto_pagina'] = institucion

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class InstitucionCreateView(BSModalCreateView):
    permission_required = ('contabilidad.add_institucion')
    model = Institucion
    template_name = "includes/formulario generico.html"
    form_class = InstitucionForm
    success_url = reverse_lazy('contabilidad_app:institucion_inicio')

    def get_context_data(self, **kwargs):
        context = super(InstitucionCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Institución"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class InstitucionUpdateView(BSModalUpdateView):
    permission_required = ('contabilidad.change_institucion')
    model = Institucion
    template_name = "contabilidad/institucion/form.html"
    form_class = InstitucionForm
    success_url = reverse_lazy('contabilidad_app:institucion_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(InstitucionUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Institución"
        return context


class InstitucionDeleteView(BSModalDeleteView):
    permission_required = ('contabilidad.delete_institucion')
    model = Institucion
    template_name = "includes/eliminar generico.html"
    form_class = InstitucionForm
    success_url = reverse_lazy('contabilidad_app:institucion_inicio')
       
    def get_context_data(self, **kwargs):
        context = super(InstitucionDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Institución"
        context['item'] = self.get_object()
        return context

#---------------------------------------------------------------------------------

class MedioPagoListView(TemplateView):
    permission_required = ('contabilidad.view_mediopago')
    template_name = "contabilidad/medio_pago/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(MedioPagoListView, self).get_context_data(**kwargs)
        medio_pago = MedioPago.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(medio_pago) > objectsxpage:
            paginator = Paginator(medio_pago, objectsxpage)
            page_number = self.request.GET.get('page')
            medio_pago = paginator.get_page(page_number)

        context['contexto_medio_pago'] = medio_pago
        context['contexto_pagina'] = medio_pago
        context['contexto_filtro'] = '?'
        return context

def MedioPagoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/medio_pago/inicio_tabla.html'
        context = {}
        medio_pago = MedioPago.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(medio_pago) > objectsxpage:
            paginator = Paginator(medio_pago, objectsxpage)
            page_number = request.GET.get('page')
            medio_pago = paginator.get_page(page_number)

        context['contexto_medio_pago'] = medio_pago
        context['contexto_pagina'] = medio_pago
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class MedioPagoCreateView(BSModalCreateView):
    permission_required = ('contabilidad.add_mediopago')
    model = MedioPago
    template_name = "includes/formulario generico.html"
    form_class = MedioPagoForm
    success_url = reverse_lazy('contabilidad_app:medio_pago_inicio')

    def get_context_data(self, **kwargs):
        context = super(MedioPagoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Medio de Pago"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class MedioPagoUpdateView(BSModalUpdateView):
    permission_required = ('contabilidad.change_mediopago')
    model = MedioPago
    template_name = "contabilidad/medio_pago/form.html"
    form_class = MedioPagoForm
    success_url = reverse_lazy('contabilidad_app:medio_pago_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MedioPagoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Medio de Pago"
        return context


class ChequeListView(PermissionRequiredMixin, ListView): 
    permission_required = ('contabilidad.view_cheque')
                                                                    
    model = Cheque
    template_name = "contabilidad/cheque/inicio.html"
    context_object_name = 'contexto_cheques'
                                                                 
                                                                               
def ChequeTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/cheque/inicio_tabla.html'
        context = {}
        context['contexto_cheques'] = Cheque.objects.all()
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
                                                                             
                                                                     
class ChequeCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_cheque')
    model = Cheque
    template_name = "includes/formulario generico.html"
    form_class = ChequeForm
    success_url = reverse_lazy('contabilidad_app:cheque_inicio')
                                                                          
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
                                                                  
    def get_context_data(self, **kwargs):
        context = super(ChequeCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Cheque"
        return context


class ChequeUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    template_name = "includes/formulario generico.html"
    form_class = ChequeForm
    success_url = reverse_lazy('contabilidad_app:cheque_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cheque"
        return context


class ChequeDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_cheque')
    model = Cheque
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('contabilidad_app:cheque_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            cheque = self.get_object()
            for recibo in ReciboBoletaPago.objects.filter(content_type=ContentType.objects.get_for_model(cheque), id_registro=cheque.id):
                recibo.content_type = None
                recibo.id_registro = None
                recibo.save()
            for recibo in ReciboServicio.objects.filter(content_type=ContentType.objects.get_for_model(cheque), id_registro=cheque.id):
                recibo.content_type = None
                recibo.id_registro = None
                recibo.save()
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequeDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cheque"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class ChequeSolicitarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    template_name = "contabilidad/cheque/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequeSolicitarView, self).get_context_data(**kwargs)
        context['accion'] = "Solicitar"
        context['titulo'] = "Cheque"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    

class ChequeEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    template_name = "contabilidad/cheque/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequeEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Cheque"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    
class ChequePorCerrarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    template_name = "contabilidad/cheque/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        cheque = self.get_object()
        error_cobrado = False
        for cheque in ChequeFisico.objects.filter(cheque=cheque):
            if cheque.estado != 2:
                error_cobrado = True
        if error_cobrado:
            context['texto'] = 'Hay cheques pendientes de cobro'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_POR_CERRAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequePorCerrarView, self).get_context_data(**kwargs)
        context['accion'] = "Por Cerrar"
        context['titulo'] = "Cheque"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context

    
class ChequePorCerrarEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    template_name = "contabilidad/cheque/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequePorCerrarEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Cheque"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class ChequeCerrarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    form_class = ChequeCerrarForm
    template_name = "contabilidad/cheque/cerrar.html"
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        cheque = self.get_object()
        error_cancelado = False
        for requerimiento in Requerimiento.objects.filter(content_type=ContentType.objects.get_for_model(cheque), id_registro=cheque.id):
            if requerimiento.estado != 7:
                error_cancelado = True
        for recibo in ReciboCajaChica.objects.filter(cheque=cheque):
            if recibo.estado != 3:
                error_cancelado = True
        for recibo in ReciboBoletaPago.objects.filter(content_type=ContentType.objects.get_for_model(cheque), id_registro=cheque.id):
            if recibo.estado != 2:
                error_cancelado = True
        for recibo in ReciboServicio.objects.filter(content_type=ContentType.objects.get_for_model(cheque), id_registro=cheque.id):
            if recibo.estado != 2:
                error_cancelado = True

        if error_cancelado:
            context['texto'] = 'Hay comprobantes pendiente de cancelar'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.instance.estado = 4
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return super().form_invalid(form)
            
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cheque = self.get_object()
        comisiones = Decimal('0.00')
        for movimiento in movimientos_cheque(cheque):
            comisiones += movimiento[5] + movimiento[6]
        kwargs['recibido'] = cheque.recibido
        kwargs['comisiones'] = comisiones
        kwargs['vuelto_extra'] = cheque.vuelto_extra
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ChequeCerrarView, self).get_context_data(**kwargs)
        context['accion'] = "Cerrar"
        context['titulo'] = "Cheque"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    

class ChequeCerradoEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_cheque')
    model = Cheque
    template_name = "contabilidad/cheque/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            self.object.comision = Decimal('0.00')
            self.object.redondeo = Decimal('0.00')
            self.object.vuelto = Decimal('0.00')
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequeCerradoEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Cheque"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context

class ChequeDetalleView(PermissionRequiredMixin, DetailView):
    permission_required = ('contabilidad.view_cheque')
    model = Cheque
    template_name = "contabilidad/cheque/detalle.html"
    context_object_name = 'contexto_cheque_detalle'

    def get_context_data(self, **kwargs):
        cheque = Cheque.objects.get(id = self.kwargs['pk'])
        context = super(ChequeDetalleView, self).get_context_data(**kwargs)
        context['contexto_recibos_boleta_pago'] = ReciboBoletaPago.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_recibos_servicio'] = ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_recibos_caja_chica'] = ReciboCajaChica.objects.filter(cheque = cheque)
        context['contexto_requerimientos'] = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_cheques_fisicos'] = ChequeFisico.objects.filter(cheque = cheque)
        context['contexto_vuelto_extra'] = ChequeVueltoExtra.objects.filter(cheque = cheque)
        total_boleta_pago = Decimal('0.00')
        if context['contexto_recibos_boleta_pago']:
            total_boleta_pago = context['contexto_recibos_boleta_pago'].aggregate(models.Sum('monto'))['monto__sum']
        total_boleta_pago_pagado = Decimal('0.00')
        if context['contexto_recibos_boleta_pago']:
            total_boleta_pago_pagado = context['contexto_recibos_boleta_pago'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        total_servicio = Decimal('0.00')
        if context['contexto_recibos_servicio']:
            total_servicio = context['contexto_recibos_servicio'].aggregate(models.Sum('monto'))['monto__sum']
        total_servicio_pagado = Decimal('0.00')
        if context['contexto_recibos_servicio']:
            total_servicio_pagado = context['contexto_recibos_servicio'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        total_caja_chica = Decimal('0.00')
        if context['contexto_recibos_caja_chica']:
            total_caja_chica = context['contexto_recibos_caja_chica'].aggregate(models.Sum('monto'))['monto__sum']
        total_caja_chica_pagado = Decimal('0.00')
        if context['contexto_recibos_caja_chica']:
            total_caja_chica_pagado = context['contexto_recibos_caja_chica'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        total_requerimiento = Decimal('0.00')
        if context['contexto_requerimientos']:
            total_requerimiento = context['contexto_requerimientos'].aggregate(models.Sum('monto'))['monto__sum']
        total_requerimiento_usado = Decimal('0.00')
        if context['contexto_requerimientos']:
            total_requerimiento_usado = context['contexto_requerimientos'].aggregate(models.Sum('monto_usado'))['monto_usado__sum']
        total_cheque_fisico = Decimal('0.00')
        if context['contexto_cheques_fisicos']:
            total_cheque_fisico = context['contexto_cheques_fisicos'].aggregate(models.Sum('monto'))['monto__sum']
        total_cheque_fisico_comision = Decimal('0.00')
        if context['contexto_cheques_fisicos']:
            total_cheque_fisico_comision = context['contexto_cheques_fisicos'].aggregate(models.Sum('comision'))['comision__sum']
        total_cheque_fisico_recibido = Decimal('0.00')
        if context['contexto_cheques_fisicos']:
            total_cheque_fisico_recibido = context['contexto_cheques_fisicos'].aggregate(models.Sum('monto_recibido'))['monto_recibido__sum']
        
        context['total_boleta_pago'] = total_boleta_pago
        context['total_boleta_pago_pagado'] = total_boleta_pago_pagado
        context['total_servicio'] = total_servicio
        context['total_servicio_pagado'] = total_servicio_pagado
        context['total_caja_chica'] = total_caja_chica
        context['total_caja_chica_pagado'] = total_caja_chica_pagado
        context['total_requerimiento'] = total_requerimiento
        context['total_requerimiento_usado'] = total_requerimiento_usado
        context['total_cheque_fisico'] = total_cheque_fisico
        context['total_cheque_fisico_comision'] = total_cheque_fisico_comision
        context['total_cheque_fisico_recibido'] = total_cheque_fisico_recibido
        context['total_monto_requerido'] = context['total_boleta_pago'] + context['total_servicio'] + context['total_caja_chica'] + context['total_requerimiento']

        return context


def ChequeDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/cheque/detalle_tabla.html'
        context = {}
        cheque = Cheque.objects.get(id = pk)
        context['contexto_cheque_detalle'] = cheque
        context['contexto_recibos_boleta_pago'] = ReciboBoletaPago.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_recibos_servicio'] = ReciboServicio.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_recibos_caja_chica'] = ReciboCajaChica.objects.filter(cheque = cheque)
        context['contexto_requerimientos'] = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_cheques_fisicos'] = ChequeFisico.objects.filter(cheque = cheque)
        context['contexto_vuelto_extra'] = ChequeVueltoExtra.objects.filter(cheque = cheque)
        total_boleta_pago = Decimal('0.00')
        if context['contexto_recibos_boleta_pago']:
            total_boleta_pago = context['contexto_recibos_boleta_pago'].aggregate(models.Sum('monto'))['monto__sum']
        total_boleta_pago_pagado = Decimal('0.00')
        if context['contexto_recibos_boleta_pago']:
            total_boleta_pago_pagado = context['contexto_recibos_boleta_pago'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        total_servicio = Decimal('0.00')
        if context['contexto_recibos_servicio']:
            total_servicio = context['contexto_recibos_servicio'].aggregate(models.Sum('monto'))['monto__sum']
        total_servicio_pagado = Decimal('0.00')
        if context['contexto_recibos_servicio']:
            total_servicio_pagado = context['contexto_recibos_servicio'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        total_caja_chica = Decimal('0.00')
        if context['contexto_recibos_caja_chica']:
            total_caja_chica = context['contexto_recibos_caja_chica'].aggregate(models.Sum('monto'))['monto__sum']
        total_caja_chica_pagado = Decimal('0.00')
        if context['contexto_recibos_caja_chica']:
            total_caja_chica_pagado = context['contexto_recibos_caja_chica'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        total_requerimiento = Decimal('0.00')
        if context['contexto_requerimientos']:
            total_requerimiento = context['contexto_requerimientos'].aggregate(models.Sum('monto'))['monto__sum']
        total_requerimiento_usado = Decimal('0.00')
        if context['contexto_requerimientos']:
            total_requerimiento_usado = context['contexto_requerimientos'].aggregate(models.Sum('monto_usado'))['monto_usado__sum']
        total_cheque_fisico = Decimal('0.00')
        if context['contexto_cheques_fisicos']:
            total_cheque_fisico = context['contexto_cheques_fisicos'].aggregate(models.Sum('monto'))['monto__sum']
        total_cheque_fisico_comision = Decimal('0.00')
        if context['contexto_cheques_fisicos']:
            total_cheque_fisico_comision = context['contexto_cheques_fisicos'].aggregate(models.Sum('comision'))['comision__sum']
        total_cheque_fisico_recibido = Decimal('0.00')
        if context['contexto_cheques_fisicos']:
            total_cheque_fisico_recibido = context['contexto_cheques_fisicos'].aggregate(models.Sum('monto_recibido'))['monto_recibido__sum']
        
        context['total_boleta_pago'] = total_boleta_pago
        context['total_boleta_pago_pagado'] = total_boleta_pago_pagado
        context['total_servicio'] = total_servicio
        context['total_servicio_pagado'] = total_servicio_pagado
        context['total_caja_chica'] = total_caja_chica
        context['total_caja_chica_pagado'] = total_caja_chica_pagado
        context['total_requerimiento'] = total_requerimiento
        context['total_requerimiento_usado'] = total_requerimiento_usado
        context['total_cheque_fisico'] = total_cheque_fisico
        context['total_cheque_fisico_comision'] = total_cheque_fisico_comision
        context['total_cheque_fisico_recibido'] = total_cheque_fisico_recibido
        context['total_monto_requerido'] = context['total_boleta_pago'] + context['total_servicio'] + context['total_caja_chica'] + context['total_requerimiento']

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ChequeReciboBoletaPagoAgregarView(BSModalFormView):
    permission_required = ('contabilidad.add_reciboboletapago')
    template_name = 'includes/formulario generico.html'
    form_class = ChequeReciboBoletaPagoAgregarForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.kwargs['cheque_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
                recibo_boleta_pago = form.cleaned_data.get('recibo_boleta_pago')
                recibo_boleta_pago.content_type = ContentType.objects.get_for_model(cheque)
                recibo_boleta_pago.id_registro = cheque.id
                registro_guardar(recibo_boleta_pago, self.request)
                recibo_boleta_pago.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
        recibos = ReciboBoletaPago.objects.filter(
            content_type=None,
            id_registro=None,
            )
        if cheque.moneda:
            recibos = recibos.filter(boleta_pago__datos_planilla__moneda=cheque.moneda)
        kwargs = super().get_form_kwargs()
        kwargs['recibos'] = recibos
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ChequeReciboBoletaPagoAgregarView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Recibo Boleta de Pago'
        return context


class ChequeReciboBoletaPagoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_reciboboletapago')
    model = ReciboBoletaPago
    template_name = 'includes/formulario generico.html'
    form_class = ChequeReciboBoletaPagoUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeReciboBoletaPagoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Boleta de Pago"
        return context


class ChequeReciboBoletaPagoRemoverView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_cheque')
    model = ReciboBoletaPago
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                recibo_boleta_pago = self.get_object()
                recibo_boleta_pago.content_type = None
                recibo_boleta_pago.id_registro = None
                recibo_boleta_pago.monto_pagado = 0
                recibo_boleta_pago.fecha_pago = None
                recibo_boleta_pago.voucher = None
                registro_guardar(recibo_boleta_pago, self.request)
                recibo_boleta_pago.save()
                messages.success(request, MENSAJE_REMOVER_RECIBO_BOLETA_PAGO)
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ChequeReciboBoletaPagoRemoverView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Recibo Boleta de Pago"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class ChequeReciboServicioAgregarView(BSModalFormView):
    permission_required = ('contabilidad.add_reciboservicio')
    template_name = 'includes/formulario generico.html'
    form_class = ChequeReciboServicioAgregarForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.kwargs['cheque_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
                recibo_servicio = form.cleaned_data.get('recibo_servicio')
                recibo_servicio.content_type = ContentType.objects.get_for_model(cheque)
                recibo_servicio.id_registro = cheque.id
                registro_guardar(recibo_servicio, self.request)
                recibo_servicio.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        recibos = ReciboServicio.objects.filter(content_type = None, id_registro = None)
        kwargs = super().get_form_kwargs()
        kwargs['recibos'] = recibos
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ChequeReciboServicioAgregarView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Recibo Servicio'
        return context
    

class ChequeReciboServicioUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_reciboservicio')
    model = ReciboServicio
    template_name = 'includes/formulario generico.html'
    form_class = ChequeReciboServicioUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeReciboServicioUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Boleta de Pago"
        return context


class ChequeReciboServicioRemoverView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_cheque')
    model = ReciboServicio
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            recibo_servicio = self.get_object()
            recibo_servicio.content_type = None
            recibo_servicio.id_registro = None
            recibo_servicio.monto_pagado = 0
            recibo_servicio.fecha_pago = None
            recibo_servicio.voucher = None
            registro_guardar(recibo_servicio, self.request)
            recibo_servicio.save()
            messages.success(request, MENSAJE_REMOVER_RECIBO_SERVICIO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequeReciboServicioRemoverView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Recibo"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context
    

class ChequeReciboCajaChicaAgregarView(BSModalFormView):
    permission_required = ('contabilidad.add_recibocajachica')
    template_name = 'includes/formulario generico.html'
    form_class = ChequeReciboCajaChicaAgregarForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.kwargs['cheque_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
                recibo_caja_chica = form.cleaned_data.get('recibo_caja_chica')
                recibo_caja_chica.cheque = cheque
                registro_guardar(recibo_caja_chica, self.request)
                recibo_caja_chica.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        recibos = ReciboCajaChica.objects.filter(cheque = None)
        kwargs = super().get_form_kwargs()
        kwargs['recibos'] = recibos
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ChequeReciboCajaChicaAgregarView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Recibo Caja Chica'
        return context
    

class ChequeReciboCajaChicaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('caja_chica.change_recibocajachica')
    model = ReciboCajaChica
    template_name = 'includes/formulario generico.html'
    form_class = ChequeReciboCajaChicaUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeReciboCajaChicaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo Caja Chica"
        return context


class ChequeReciboCajaChicaRemoverView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_cheque')
    model = ReciboCajaChica
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            recibo_caja_chica = self.get_object()
            recibo_caja_chica.cheque = None
            recibo_caja_chica.monto_pagado = 0
            recibo_caja_chica.fecha_pago = None
            registro_guardar(recibo_caja_chica, self.request)
            recibo_caja_chica.save()
            messages.success(request, MENSAJE_REMOVER_RECIBO_SERVICIO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ChequeReciboCajaChicaRemoverView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Recibo"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context
    

class ChequeFisicoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_chequefisico')
    model = ChequeFisico
    template_name = "includes/formulario generico.html"
    form_class = ChequeFisicoForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.kwargs['cheque_id']})

    def form_valid(self, form):
        form.instance.cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeFisicoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Cheque Fisico"
        return context


class ChequeFisicoUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('contabilidad.change_chequefisico')
    model = ChequeFisico
    template_name = "includes/formulario generico.html"
    form_class = ChequeFisicoForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.object.cheque.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeFisicoUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Cheque Fisico"
        return context


class ChequeFisicoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_chequefisico')
    model = ChequeFisico
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.object.cheque.id})

    def get_context_data(self, **kwargs):
        context = super(ChequeFisicoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Cheque Fisico"
        return context
    
class ChequeFisicoCobrarView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('contabilidad.change_chequefisico')
    model = ChequeFisico
    template_name = "includes/formulario generico.html"
    form_class = ChequeFisicoCobrarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.object.cheque.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeFisicoCobrarView, self).get_context_data(**kwargs)
        context['accion']="Cobrar"
        context['titulo']="Cheque Fisico"
        return context
    
class ChequeFisicoCobrarEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_chequefisico')
    model = ChequeFisico
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.object.cheque.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.comision = Decimal('0.00')
        self.object.monto_recibido = Decimal('0.00')
        self.object.fecha_cobro = None
        self.object.estado = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(ChequeFisicoCobrarEditarView, self).get_context_data(**kwargs)
        context['accion']="Editar"
        context['titulo']="Cheque Fisico"
        context['dar_baja']=True
        return context


class ChequeVueltoExtraCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_chequevueltoextra')
    model = ChequeVueltoExtra
    template_name = "contabilidad/cheque/vuelto_extra.html"
    form_class = ChequeVueltoExtraForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.kwargs['cheque_id']})

    def get_form_kwargs(self):
        kwargs = super(ChequeVueltoExtraCreateView, self).get_form_kwargs()
        cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
        kwargs['moneda_cheque'] = cheque.moneda
        return kwargs

    def form_valid(self, form):
        cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
        form.instance.cheque = cheque
        print(form.instance.vuelto_original)
        print(form.instance.vuelto_extra)
        print(form.instance.moneda)
        print(form.instance.tipo_cambio)
        print(form.instance.cheque)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChequeVueltoExtraCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Vuelto Extra"
        return context


class ChequeVueltoExtraUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_chequevueltoextra')
    model = ChequeVueltoExtra
    template_name = "contabilidad/cheque/vuelto_extra.html"
    form_class = ChequeVueltoExtraForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.object.cheque.id})

    def get_form_kwargs(self):
        kwargs = super(ChequeVueltoExtraUpdateView, self).get_form_kwargs()
        cheque = ChequeVueltoExtra.objects.get(id = self.kwargs['pk'])
        kwargs['moneda_cheque'] = cheque.cheque.moneda
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ChequeVueltoExtraUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Vuelto Extra"
        return context


class ChequeVueltoExtraDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_chequevueltoextra')
    model = ChequeVueltoExtra
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.object.cheque.id})

    def get_context_data(self, **kwargs):
        context = super(ChequeVueltoExtraDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Vuelto Extra"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class ChequeSolicitarPdfView(View):
    permission_required = ('contabilidad.view_cheque')
    def get(self, request, *args, **kwargs):
        cheque = Cheque.objects.get(id = kwargs['pk'])
        movimientos = movimientos_cheque(cheque)

        titulo = 'Solicitud de Cheque - %s' % cheque.concepto
        fecha_hoy = _date(datetime.today(), "d \d\e F \d\e Y")
        vertical = True
        sociedad_MPL = Sociedad.objects.get(abreviatura='MPL')
        # sociedad_MCA = Sociedad.objects.get(abreviatura='MCA')
        color = COLOR_DEFAULT
        # logo = [sociedad_MPL.logo.url, sociedad_MCA.logo.url]
        logo = [sociedad_MPL.logo.url]
        pie_pagina = PIE_DE_PAGINA_DEFAULT
        buf = generarChequeSolicitarPdf(titulo, vertical, logo, pie_pagina, fecha_hoy, movimientos, cheque, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo
        
        return respuesta


class ChequeCerrarPdfView(View):
    permission_required = ('contabilidad.view_cheque')
    def get(self, request, *args, **kwargs):
        cheque = Cheque.objects.get(id = kwargs['pk'])
        movimientos = movimientos_cheque(cheque)
        
        titulo = 'Rendición de Cheque - %s' % cheque.concepto
        fecha_hoy = _date(datetime.today(), "d \d\e F \d\e Y")
        vertical = False
        sociedad_MPL = Sociedad.objects.get(abreviatura='MPL')
        # sociedad_MCA = Sociedad.objects.get(abreviatura='MCA')
        color = COLOR_DEFAULT
        # logo = [sociedad_MPL.logo.url, sociedad_MCA.logo.url]
        logo = [sociedad_MPL.logo.url]
        pie_pagina = PIE_DE_PAGINA_DEFAULT
        buf = generarChequeCerrarPdf(titulo, vertical, logo, pie_pagina, fecha_hoy, movimientos, cheque, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo
        
        return respuesta
        

#---------------------------------------------------------------------------------

class TelecreditoListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_telecredito')
    template_name = "contabilidad/telecredito/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(TelecreditoListView, self).get_context_data(**kwargs)
        telecredito = Telecredito.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(telecredito) > objectsxpage:
            paginator = Paginator(telecredito, objectsxpage)
            page_number = self.request.GET.get('page')
            telecredito = paginator.get_page(page_number)

        context['contexto_telecredito'] = telecredito
        context['contexto_pagina'] = telecredito
        context['contexto_filtro'] = '?'
        return context


def TelecreditoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/telecredito/inicio_tabla.html'
        context = {}
        telecredito = Telecredito.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(telecredito) > objectsxpage:
            paginator = Paginator(telecredito, objectsxpage)
            page_number = request.GET.get('page')
            telecredito = paginator.get_page(page_number)

        context['contexto_telecredito'] = telecredito
        context['contexto_pagina'] = telecredito
        context['contexto_filtro'] = '?'
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class TelecreditoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('contabilidad.add_telecredito')
    model = Telecredito
    template_name = "includes/formulario generico.html"
    form_class = TelecreditoForm
    success_url = reverse_lazy('contabilidad_app:telecredito_inicio')

    def get_context_data(self, **kwargs):
        context = super(TelecreditoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Telecrédito"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class TelecreditoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "contabilidad/telecredito/form.html"
    form_class = TelecreditoForm
    success_url = reverse_lazy('contabilidad_app:telecredito_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TelecreditoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Telecrédito"
        return context      


class TelecreditoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_telecredito')
    model = Telecredito
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('contabilidad_app:telecredito_inicio')

    def delete(self, request, *args, **kwargs):
        telecredito = self.get_object()
        for recibo in ReciboBoletaPago.objects.filter(content_type=ContentType.objects.get_for_model(telecredito), id_registro=telecredito.id):
            recibo.content_type = None
            recibo.id_registro = None
            recibo.save()
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TelecreditoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Telecredito"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class TelecreditoSolicitarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_SOLICITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoSolicitarView, self).get_context_data(**kwargs)
        context['accion'] = "Solicitar"
        context['titulo'] = "Telecredito"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    

class TelecreditoEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Telecredito"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class TelecreditoRegistrarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "includes/formulario generico.html"
    form_class = TelecreditoCobrarForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.instance.estado = 3
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoRegistrarView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Telecredito"
        return context
    

class TelecreditoRegistrarEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            self.object.fecha_cobro = None
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoRegistrarEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Telecredito"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class TelecreditoCerrarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        telecredito = self.get_object()
        error_cancelado = False
        for recibo in ReciboBoletaPago.objects.filter(content_type=ContentType.objects.get_for_model(telecredito), id_registro=telecredito.id):
            if recibo.estado != 2:
                error_cancelado = True
        
        if error_cancelado:
            context['texto'] = 'Hay comprobantes pendiente de cancelar'
            return render(request, 'includes/modal sin permiso.html', context)
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 4
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_POR_CERRAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoCerrarView, self).get_context_data(**kwargs)
        context['accion'] = "Cerrar"
        context['titulo'] = "Telecredito"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context
    

class TelecreditoCerradoEditarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.change_telecredito')
    model = Telecredito
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_EDITAR_CHEQUE)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoCerradoEditarView, self).get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['titulo'] = "Telecredito"
        context['dar_baja'] = "true"
        context['item'] = str(self.object.concepto) + ' | ' + str(self.object.usuario.username)
        return context


class TelecreditoRecibosListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_telecredito')
    template_name = "contabilidad/telecredito/detalle.html"
    
    def get_context_data(self, **kwargs):
        context = super(TelecreditoRecibosListView, self).get_context_data(**kwargs)
        telecredito_detalle = ReciboBoletaPago.objects.filter(
            content_type=ContentType.objects.get_for_model(Telecredito), 
            id_registro = self.kwargs['pk']
            )
        telecredito = Telecredito.objects.get(id=self.kwargs['pk'])
        context['contexto_telecredito_detalle'] = telecredito_detalle
        context['contexto_telecredito'] = telecredito
        return context


def TelecreditoRecibosTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/telecredito/detalle_tabla.html'
        context = {}
        telecredito_detalle = ReciboBoletaPago.objects.filter(
            content_type=ContentType.objects.get_for_model(Telecredito), 
            id_registro = pk
            )
        telecredito = Telecredito.objects.get(id=pk)
        context['contexto_telecredito_detalle'] = telecredito_detalle
        context['contexto_telecredito'] = telecredito
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class TelecreditoRecibosCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('contabilidad.add_telecredito')
    template_name = 'contabilidad/telecredito/form_recibos.html'
    form_class = TelecreditoReciboPagoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.kwargs['pk']})
    

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                recibo_boleta_pago = form.cleaned_data.get('recibo_boleta_pago')
                telecredito = Telecredito.objects.get(id=self.kwargs['pk'])
                recibo_boleta_pago.content_type = telecredito.content_type
                recibo_boleta_pago.id_registro = telecredito.id
                registro_guardar(recibo_boleta_pago, self.request)
                recibo_boleta_pago.save()

                recibos_boletas_pagos = ReciboBoletaPago.objects.filter(
                    content_type = telecredito.content_type, 
                    id_registro = telecredito.id,
                )
                monto_solicitado = 0
                if recibos_boletas_pagos:
                    for recibos_boletas in recibos_boletas_pagos:
                        monto_solicitado += recibos_boletas.monto
                    telecredito.monto = monto_solicitado
                    telecredito.save()
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(TelecreditoRecibosCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Añadir"
        context['titulo'] = "Recibo Pago"
        return context
    

class TelecreditoRecibosDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('contabilidad.delete_telecredito')
    model = ReciboBoletaPago
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():   
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.kwargs['telecredito_id']})
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            obj = self.get_object()
            obj.content_type = None
            obj.id_registro = None
            obj.monto_pagado = 0
            obj.fecha_pago = None
            obj.voucher = None
            obj.save()

            telecredito = Telecredito.objects.get(id = self.kwargs['telecredito_id'])
            recibos_boletas_pagos = ReciboBoletaPago.objects.filter(
                content_type = telecredito.content_type, 
                id_registro = telecredito.id,
            )
            monto_solicitado = 0
            monto_pagado = 0
            if recibos_boletas_pagos:
                for recibos_boletas in recibos_boletas_pagos:
                    monto_solicitado += recibos_boletas.monto
                    monto_pagado += recibos_boletas.monto_pagado
            telecredito.monto = monto_solicitado
            telecredito.monto_usado = monto_pagado
            telecredito.save()
            # return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TelecreditoRecibosDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Remover"
        context['titulo'] = "Recibo Boleta de Pago"
        context['item'] = str(self.object)
        return context


class TelecreditoRecibosUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('contabilidad.change_telecredito')
    model = ReciboBoletaPago
    template_name = 'includes/formulario generico.html'
    form_class = TelecreditoReciboPagoUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:telecredito_detalle', kwargs={'pk':self.kwargs['telecredito_id']})

    def get_context_data(self, **kwargs):
        context = super(TelecreditoRecibosUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Recibo de Boleta Pago"
        return context

    def form_valid(self, form):
        telecredito = Telecredito.objects.get(id=self.kwargs['telecredito_id'])
        recibos_boletas_pagos = ReciboBoletaPago.objects.filter(
            content_type = telecredito.content_type,
            id_registro = telecredito.id,
            ).filter(
                ~Q(id=form.instance.id)
                )
        monto_usado = 0
        if recibos_boletas_pagos:
            for recibo_pago in recibos_boletas_pagos:
                monto_usado += recibo_pago.monto_pagado
        telecredito.monto_usado = monto_usado + form.cleaned_data.get('monto_pagado')
        telecredito.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class TelecreditoSolicitarPdfView(View):
    permission_required = ('contabilidad.view_telecredito')
    def get(self, request, *args, **kwargs):
        telecredito = Telecredito.objects.get(id = kwargs['pk'])
        movimientos = movimientos_telecredito(telecredito)

        titulo = 'Solicitud de Telecredito - %s' % telecredito.concepto
        fecha_hoy = _date(datetime.today(), "d \d\e F \d\e Y")
        vertical = True
        sociedad_MPL = Sociedad.objects.get(abreviatura='MPL')
        # sociedad_MCA = Sociedad.objects.get(abreviatura='MCA')
        color = COLOR_DEFAULT
        # logo = [sociedad_MPL.logo.url, sociedad_MCA.logo.url]
        logo = [sociedad_MPL.logo.url]
        pie_pagina = PIE_DE_PAGINA_DEFAULT
        buf = generarTelecreditoSolicitarPdf(titulo, vertical, logo, pie_pagina, fecha_hoy, movimientos, telecredito, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo
        
        return respuesta


class TelecreditoCerrarPdfView(View):
    permission_required = ('contabilidad.view_telecredito')
    def get(self, request, *args, **kwargs):
        telecredito = Telecredito.objects.get(id = kwargs['pk'])
        movimientos = movimientos_telecredito(telecredito)
        
        titulo = 'Rendición de Telecredito - %s' % telecredito.concepto
        fecha_hoy = _date(datetime.today(), "d \d\e F \d\e Y")
        vertical = False
        sociedad_MPL = Sociedad.objects.get(abreviatura='MPL')
        # sociedad_MCA = Sociedad.objects.get(abreviatura='MCA')
        color = COLOR_DEFAULT
        # logo = [sociedad_MPL.logo.url, sociedad_MCA.logo.url]
        logo = [sociedad_MPL.logo.url]
        pie_pagina = PIE_DE_PAGINA_DEFAULT
        buf = generarTelecreditoCerrarPdf(titulo, vertical, logo, pie_pagina, fecha_hoy, movimientos, telecredito, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo
        
        return respuesta