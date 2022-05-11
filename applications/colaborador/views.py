from requests import request
from applications.importaciones import *

from datetime import datetime, time
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

from .forms import (
    DatosContratoPlanillaForm,
    DatosContratoActualizarPlanillaForm,
    DatosContratoPlanillaDarBajaForm,
    DatosContratoHonorariosForm,
    DatosContratoActualizarHonorariosForm,
    DatosContratoHonorariosDarBajaForm,
    )

from .models import (
    DatosContratoPlanilla,
    DatosContratoHonorarios,
    )

class DatosContratoPlanillaListView(ListView):
    model = DatosContratoPlanilla
    template_name = "colaborador/datos_contrato/planilla/inicio.html"
    context_object_name = 'contexto_datoscontratoplanilla'

    def get_queryset(self):
        queryset = super(DatosContratoPlanillaListView, self).get_queryset()
        return queryset

def DatosContratoPlanillaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'colaborador/datos_contrato/planilla/inicio_tabla.html'
        context = {}
        datoscontratoplanilla = DatosContratoPlanilla.objects.all()
        context['contexto_datoscontratoplanilla'] = datoscontratoplanilla

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class DatosContratoPlanillaCreateView(BSModalCreateView):
    model = DatosContratoPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoPlanillaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')

    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="datos del contrato de planilla"
        return context

    def form_valid(self, form):
        usuario_honorario = DatosContratoHonorarios.objects.filter(usuario = form.instance.usuario)
        print(form.instance.usuario)

        if len(usuario_honorario)>0:
            form.add_error('usuario', 'El usuario tiene contrato por honorarios.')
            return super().form_invalid(form)

        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class DatosContratoPlanillaUpdateView(BSModalUpdateView):
    model = DatosContratoPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoActualizarPlanillaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')

    def form_valid(self, form):
        form.instance.estado_alta_baja = 1
        form.instance.usuario.is_active = False
        form.instance.usuario.save()
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Contrato por Planilla'
        return context

class DatosContratoPlanillaDarBajaView(BSModalUpdateView):
    model = DatosContratoPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoPlanillaDarBajaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')

    def form_valid(self, form):
        form.instance.estado_alta_baja = 2
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'al contrato planilla'
        return context
    


class DatosContratoHonorariosListView(ListView):
    model = DatosContratoHonorarios
    template_name = "colaborador/datos_contrato/honorarios/inicio.html"
    context_object_name = 'contexto_datoscontratohonorarios'

    def get_queryset(self):
        queryset = super(DatosContratoHonorariosListView, self).get_queryset()
        return queryset

def DatosContratoHonorariosTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'colaborador/datos_contrato/honorarios/inicio_tabla.html'
        context = {}
        datoscontratohonorarios = DatosContratoHonorarios.objects.all()
        context['contexto_datoscontratohonorarios'] = datoscontratohonorarios

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class DatosContratoHonorariosCreateView(BSModalCreateView):
    model = DatosContratoHonorarios
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoHonorariosForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_honorarios_inicio')

    def get_context_data(self, **kwargs):
        context = super(DatosContratoHonorariosCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="datos del contrato por honorarios"
        return context

    def form_valid(self, form):
        usuario_planilla =  DatosContratoPlanilla.objects.filter(usuario = form.instance.usuario)
        print(form.instance.usuario)

        if len(usuario_planilla)>0:
            form.add_error('usuario', 'El usuario tiene contrato por planilla.')
            return super().form_invalid(form)



        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class DatosContratoHonorariosUpdateView(BSModalUpdateView):
    model = DatosContratoHonorarios
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoActualizarHonorariosForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_honorarios_inicio')

    def form_valid(self, form):
        form.instance.estado_alta_baja = 1
        form.instance.usuario.is_active = False
        form.instance.usuario.save()
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoHonorariosUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Contrato por Honorarios'
        return context

class DatosContratoHonorariosDarBajaView(BSModalUpdateView):
    model = DatosContratoHonorarios
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoHonorariosDarBajaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_honorarios_inicio')

    def form_valid(self, form):
        form.instance.estado_alta_baja = 2
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoHonorariosDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'al contrato por honorarios'
        return context
