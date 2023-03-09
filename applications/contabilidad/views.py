from django.shortcuts import render
from django.core.paginator import Paginator

from applications.importaciones import *

from .forms import(
    ComisionFondoPensionesForm,
    DatosPlanillaForm,
    DatosPlanillaDarBajaForm,
    EsSaludForm,
    BoletaPagoForm,
)

from .models import(
    FondoPensiones,
    ComisionFondoPensiones,
    DatosPlanilla,
    EsSalud,
    BoletaPago,
    ReciboBoletaPago,
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
        form.instance.usuario = self.request.user
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
    form_class = BoletaPagoForm
    success_url = reverse_lazy('contabilidad_app:boleta_pago_inicio')
       
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(BoletaPagoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Boleta de Pago'
        return context