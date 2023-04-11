from re import template
from django.db import models
from django.shortcuts import render
from django.core.paginator import Paginator
from applications.contabilidad.funciones import calcular_datos_boleta, calculo_montos
from applications.funciones import registrar_excepcion

from applications.importaciones import *
from applications.funciones import registrar_excepcion
from applications.caja_chica.models import ReciboCajaChica, Requerimiento

from .forms import(
    ChequeFisicoForm,
    ChequeForm,
    ChequeReciboBoletaPagoAgregarForm,
    ChequeReciboBoletaPagoUpdateForm,
    ChequeReciboServicioAgregarForm,
    ChequeReciboServicioUpdateForm,
    ComisionFondoPensionesForm,
    DatosPlanillaForm,
    DatosPlanillaDarBajaForm,
    EsSaludForm,
    BoletaPagoForm,
    BoletaPagoActualizarForm,
    ReciboBoletaPagoForm,
    ReciboBoletaPagoActualizarForm,
    ServicioForm,
    ReciboServicioForm,
    TelecreditoForm,
    TelecreditoReciboPagoForm,
    TelecreditoReciboPagoUpdateForm,
    TipoServicioForm,
    InstitucionForm,
    MedioPagoForm,
)

from .models import(
    Cheque,
    ChequeFisico,
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

class ComisionFondoPensionesListView(TemplateView):
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

class ComisionFondoPensionesCreateView(BSModalCreateView):
    model = ComisionFondoPensiones
    template_name = "includes/formulario generico.html"
    form_class = ComisionFondoPensionesForm
    success_url = reverse_lazy('contabilidad_app:comision_inicio')

    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Comision Fondo Pensiones"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ComisionFondoPensionesUpdateView(BSModalUpdateView):
    model = ComisionFondoPensiones
    template_name = "includes/formulario generico.html"
    form_class = ComisionFondoPensionesForm
    success_url = reverse_lazy('contabilidad_app:comision_inicio')

    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Comisiones"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ComisionFondoPensionesDeleteView(BSModalDeleteView):

    model = ComisionFondoPensiones
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('contabilidad_app:comision_inicio')

    def get_context_data(self, **kwargs):
        context = super(ComisionFondoPensionesDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Comisiones"
        return context

#---------------------------------------------------------------------------------

class DatosPlanillaListView(TemplateView):
    template_name = "contabilidad/datos_planilla/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaListView, self).get_context_data(**kwargs)
        datos_planilla = DatosPlanilla.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

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
        objectsxpage =  10 # Show 10 objects per page.

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

class DatosPlanillaCreateView(BSModalCreateView):
    model = DatosPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosPlanillaForm
    success_url = reverse_lazy('contabilidad_app:datos_planilla_inicio')

    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Datos Planilla"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class DatosPlanillaUpdateView(BSModalUpdateView):
    model = DatosPlanilla
    template_name = "contabilidad/datos_planilla/form.html"
    form_class = DatosPlanillaForm
    success_url = reverse_lazy('contabilidad_app:datos_planilla_inicio')
       
    def form_valid(self, form):
        form.instance.estado = 1
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosPlanillaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Datos Planilla'
        return context

class DatosPlanillaDarBajaView(BSModalUpdateView):
    model = DatosPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosPlanillaDarBajaForm
    success_url = reverse_lazy('contabilidad_app:datos_planilla_inicio')
    
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

class EsSaludListView(TemplateView):
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

class EsSaludCreateView(BSModalCreateView):
    model = EsSalud
    template_name = "includes/formulario generico.html"
    form_class = EsSaludForm
    success_url = reverse_lazy('contabilidad_app:essalud_inicio')

    def get_context_data(self, **kwargs):
        context = super(EsSaludCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Datos Planilla"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class EsSaludUpdateView(BSModalUpdateView):
    model = EsSalud
    template_name = "contabilidad/essalud/form.html"
    form_class = EsSaludForm
    success_url = reverse_lazy('contabilidad_app:essalud_inicio')
       
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

class BoletaPagoListView(TemplateView):
    template_name = "contabilidad/boleta_pago/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(BoletaPagoListView, self).get_context_data(**kwargs)
        boleta_pago = BoletaPago.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(boleta_pago) > objectsxpage:
            paginator = Paginator(boleta_pago, objectsxpage)
            page_number = self.request.GET.get('page')
            boleta_pago = paginator.get_page(page_number)

        context['contexto_boleta_pago'] = boleta_pago
        context['contexto_pagina'] = boleta_pago
        context['contexto_filtro'] = '?'
        return context

def BoletaPagoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/boleta_pago/inicio_tabla.html'
        context = {}
        boleta_pago = BoletaPago.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(boleta_pago) > objectsxpage:
            paginator = Paginator(boleta_pago, objectsxpage)
            page_number = request.GET.get('page')
            boleta_pago = paginator.get_page(page_number)

        context['contexto_boleta_pago'] = boleta_pago
        context['contexto_pagina'] = boleta_pago
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class BoletaPagoCreateView(BSModalCreateView):
    model = BoletaPago
    template_name = "includes/formulario generico.html"
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


class BoletaPagoUpdateView(BSModalUpdateView):
    model = BoletaPago
    template_name = "contabilidad/boleta_pago/form.html"
    form_class = BoletaPagoActualizarForm
    success_url = reverse_lazy('contabilidad_app:boleta_pago_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super(BoletaPagoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Boleta de Pago'
        return context

class BoletaPagoDeleteView(BSModalDeleteView):
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
#---------------------------------------------------------------------------------

class ReciboBoletaPagoListView(TemplateView):
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

class ReciboBoletaPagoCreateView(BSModalCreateView):
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

class ReciboBoletaPagoUpdateView(BSModalUpdateView):
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

class ReciboBoletaPagoDeleteView(BSModalDeleteView):
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

class ServicioListView(TemplateView):
    template_name = "contabilidad/servicio/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(ServicioListView, self).get_context_data(**kwargs)
        servicio = Servicio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(servicio) > objectsxpage:
            paginator = Paginator(servicio, objectsxpage)
            page_number = self.request.GET.get('page')
            servicio = paginator.get_page(page_number)

        context['contexto_servicio'] = servicio
        context['contexto_pagina'] = servicio
        context['contexto_filtro'] = '?'
        return context

def ServicioTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/servicio/inicio_tabla.html'
        context = {}
        servicio = Servicio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(servicio) > objectsxpage:
            paginator = Paginator(servicio, objectsxpage)
            page_number = request.GET.get('page')
            servicio = paginator.get_page(page_number)

        context['contexto_servicio'] = servicio
        context['contexto_pagina'] = servicio
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ServicioCreateView(BSModalCreateView):
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

class ServicioUpdateView(BSModalUpdateView):
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

#---------------------------------------------------------------------------------

class ReciboServicioListView(TemplateView):
    template_name = "contabilidad/recibo_servicio/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReciboServicioListView, self).get_context_data(**kwargs)
        recibo_servicio = ReciboServicio.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

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
        objectsxpage =  10 # Show 10 objects per page.

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

class ReciboServicioCreateView(BSModalCreateView):
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

class InstitucionListView(TemplateView):
    template_name = "contabilidad/institucion/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(InstitucionListView, self).get_context_data(**kwargs)
        institucion = Institucion.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(institucion) > objectsxpage:
            paginator = Paginator(institucion, objectsxpage)
            page_number = self.request.GET.get('page')
            institucion = paginator.get_page(page_number)

        context['contexto_institucion'] = institucion
        context['contexto_pagina'] = institucion
        context['contexto_filtro'] = '?'
        return context

def InstitucionTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/institucion/inicio_tabla.html'
        context = {}
        institucion = Institucion.objects.all()
        objectsxpage =  10 # Show 10 objects per page.

        if len(institucion) > objectsxpage:
            paginator = Paginator(institucion, objectsxpage)
            page_number = request.GET.get('page')
            institucion = paginator.get_page(page_number)

        context['contexto_institucion'] = institucion
        context['contexto_pagina'] = institucion
        context['contexto_filtro'] = '?'

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class InstitucionCreateView(BSModalCreateView):
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

#---------------------------------------------------------------------------------

class MedioPagoListView(TemplateView):
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

    def form_valid(self, form):
        form.instance.usuario = self.request.user
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

    def get_context_data(self, **kwargs):
        context = super(ChequeDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cheque"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
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
        # context['contexto_recibos_caja_chica'] = ReciboCajaChica.objects.filter(cheque = cheque)
        context['contexto_requerimientos'] = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_cheques_fisicos'] = ChequeFisico.objects.filter(cheque = cheque)
        context['total_boleta'] = context['contexto_recibos_boleta_pago'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        context['total_servicio'] = context['contexto_recibos_servicio'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        context['total_requerimiento'] = context['contexto_requerimientos'].aggregate(models.Sum('monto_usado'))['monto_usado__sum']

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
        # context['contexto_recibos_caja_chica'] = ReciboCajaChica.objects.filter(cheque = cheque)
        context['contexto_requerimientos'] = Requerimiento.objects.filter(content_type = ContentType.objects.get_for_model(cheque), id_registro = cheque.id)
        context['contexto_cheques_fisicos'] = ChequeFisico.objects.filter(cheque = cheque)
        context['total_boleta'] = context['contexto_recibos_boleta_pago'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        context['total_servicio'] = context['contexto_recibos_servicio'].aggregate(models.Sum('monto_pagado'))['monto_pagado__sum']
        context['total_requerimiento'] = context['contexto_requerimientos'].aggregate(models.Sum('monto_usado'))['monto_usado__sum']

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ChequeReciboBoletaPagoAgregarView(BSModalFormView):
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
        recibos = ReciboBoletaPago.objects.filter(content_type = None, id_registro = None)
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
    
    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                cheque = Cheque.objects.get(id=self.kwargs['cheque_id'])
                recibos_boletas_pagos = ReciboBoletaPago.objects.filter(
                    content_type = cheque.content_type,
                    id_registro = cheque.id,
                    ).filter(
                        ~Q(id=form.instance.id)
                        )
                monto_usado = 0
                if recibos_boletas_pagos:
                    for boleta_pago in recibos_boletas_pagos:
                        monto_usado += boleta_pago.monto_pagado
                cheque.monto_usado = monto_usado + form.cleaned_data.get('monto_pagado')
                cheque.save()
                registro_guardar(form.instance, self.request)
                self.request.session['primero'] = False
            return super().form_valid(form)
            
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
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
                cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
                recibos_boletas_pagos = ReciboBoletaPago.objects.filter(
                    content_type = cheque.content_type, 
                    id_registro = cheque.id,
                )
                monto_solicitado = 0
                monto_pagado = 0
                if recibos_boletas_pagos:
                    for recibos_boleta in recibos_boletas_pagos:
                        monto_solicitado += recibos_boleta.monto
                        monto_pagado += recibos_boleta.monto_pagado
                cheque.monto = monto_solicitado
                cheque.monto_usado = monto_pagado
                cheque.save()

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
        cheque = Cheque.objects.get(id=self.kwargs['cheque_id'])
        recibo_servicio = ReciboServicio.objects.filter(
            content_type = cheque.content_type,
            id_registro = cheque.id,
            ).filter(
                ~Q(id=form.instance.id)
                )
        monto_usado = 0
        if recibo_servicio:
            for boleta_pago in recibo_servicio:
                monto_usado += boleta_pago.monto_pagado
        cheque.monto_usado = monto_usado + form.cleaned_data.get('monto_pagado')
        cheque.save()
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
    

# class ChequeRequerimientoAgregarView(BSModalFormView):
#     template_name = 'includes/formulario generico.html'
#     form_class = ChequeRequerimientoAgregarForm

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk':self.kwargs['cheque_id']})

#     @transaction.atomic
#     def form_valid(self, form):
#         sid = transaction.savepoint()
#         try:
#             if self.request.session['primero']:
#                 cheque = Cheque.objects.get(id = self.kwargs['cheque_id'])
#                 requerimiento = form.cleaned_data.get('requerimiento')
#                 requerimiento.content_type = ContentType.objects.get_for_model(cheque)
#                 requerimiento.id_registro = cheque.id
#                 registro_guardar(requerimiento, self.request)
#                 requerimiento.save()
#                 self.request.session['primero'] = False
#             return super().form_valid(form)
#         except Exception as ex:
#             transaction.savepoint_rollback(sid)
#             registrar_excepcion(self, ex, __file__)
#         return HttpResponseRedirect(self.get_success_url())

#     def get_form_kwargs(self):
#         requerimientos = Requerimiento.objects.filter(content_type = None, id_registro = None)
#         kwargs = super().get_form_kwargs()
#         kwargs['requerimientos'] = requerimientos
#         return kwargs

#     def get_context_data(self, **kwargs):
#         self.request.session['primero'] = True
#         context = super(ChequeRequerimientoAgregarView, self).get_context_data(**kwargs)
#         context['accion'] = 'Agregar'
#         context['titulo'] = 'Requerimiento'
#         return context


# class ChequeRequerimientoRemoverView(PermissionRequiredMixin, BSModalDeleteView):
#     permission_required = ('contabilidad.delete_cheque')
#     model = Requerimiento
#     template_name = "includes/eliminar generico.html"

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('contabilidad_app:cheque_detalle', kwargs={'pk': self.kwargs['cheque_id']})

#     @transaction.atomic
#     def delete(self, request, *args, **kwargs):
#         sid = transaction.savepoint()
#         try:
#             requerimiento = self.get_object()
#             requerimiento.content_type = None
#             requerimiento.id_registro = None
#             registro_guardar(requerimiento, self.request)
#             requerimiento.save()
#             messages.success(request, MENSAJE_REMOVER_REQUERIMIENTO)
#         except Exception as ex:
#             transaction.savepoint_rollback(sid)
#             registrar_excepcion(self, ex, __file__)
#         return HttpResponseRedirect(self.get_success_url())

#     def get_context_data(self, **kwargs):
#         context = super(ChequeRequerimientoRemoverView, self).get_context_data(**kwargs)
#         context['accion'] = "Eliminar"
#         context['titulo'] = "Requerimiento"
#         context['item'] = self.get_object()
#         context['dar_baja'] = "true"
#         return context
    

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


class TelecreditoRecibosListView(PermissionRequiredMixin, TemplateView):
    permission_required = ('contabilidad.view_telecreditorecibo')
    template_name = "contabilidad/telecredito/detalle.html"
    
    def get_context_data(self, **kwargs):
        context = super(TelecreditoRecibosListView, self).get_context_data(**kwargs)
        telecredito_recibos = ReciboBoletaPago.objects.filter(
            content_type=ContentType.objects.get_for_model(Telecredito), 
            id_registro = self.kwargs['pk']
            )
        telecredito = Telecredito.objects.get(id=self.kwargs['pk'])
        context['contexto_telecredito_recibos'] = telecredito_recibos
        context['contexto_telecredito'] = telecredito
        return context


def TelecreditoRecibosTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'contabilidad/telecredito/detalle_tabla.html'
        context = {}
        telecredito_recibos = ReciboBoletaPago.objects.filter(
            content_type=ContentType.objects.get_for_model(Telecredito), 
            id_registro = pk
            )
        telecredito = Telecredito.objects.get(id=pk)
        context['contexto_telecredito_recibos'] = telecredito_recibos
        context['contexto_telecredito'] = telecredito
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class TelecreditoRecibosCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('contabilidad.add_telecreditorecibo')
    template_name = 'contabilidad/telecredito/form_recibos.html'
    form_class = TelecreditoReciboPagoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:telecredito_recibos_inicio', kwargs={'pk':self.kwargs['pk']})
    

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
    permission_required = ('contabilidad.delete_telecreditorecibo')
    model = ReciboBoletaPago
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():   
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:telecredito_recibos_inicio', kwargs={'pk':self.kwargs['telecredito_id']})
    
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
    permission_required = ('contabilidad.change_telecreditorecibo')
    model = ReciboBoletaPago
    template_name = 'includes/formulario generico.html'
    form_class = TelecreditoReciboPagoUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('contabilidad_app:telecredito_recibos_inicio', kwargs={'pk':self.kwargs['telecredito_id']})

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