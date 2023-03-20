from django.shortcuts import render
from django.core.paginator import Paginator

from applications.importaciones import *

from .forms import(
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
    TipoServicioForm,
    InstitucionForm,
    MedioPagoForm,
)

from .models import(
    FondoPensiones,
    ComisionFondoPensiones,
    DatosPlanilla,
    EsSalud,
    BoletaPago,
    ReciboBoletaPago,
    Servicio,
    ReciboServicio,
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
        form.instance.usuario = self.request.user
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

