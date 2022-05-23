from requests import request
from applications.importaciones import *

from datetime import datetime, time
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.shortcuts import render


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

class DatosContratoPlanillaListView(PermissionRequiredMixin,ListView):
    permission_required = ('colaborador.view_datoscontratoplanilla')
    
    model = DatosContratoPlanilla
    template_name = "colaborador/datos_contrato/planilla/inicio.html"
    context_object_name = 'contexto_datoscontratoplanilla'

    def get_queryset(self):
        queryset = super(DatosContratoPlanillaListView, self).get_queryset()
        queryset = DatosContratoPlanilla.objects.exclude(estado_alta_baja=2)
        return queryset

def DatosContratoPlanillaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'colaborador/datos_contrato/planilla/inicio_tabla.html'
        context = {}
        datoscontratoplanilla = DatosContratoPlanilla.objects.exclude(estado_alta_baja = 2)
        context['contexto_datoscontratoplanilla'] = datoscontratoplanilla

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class DatosContratoPlanillaCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('colaborador.add_datoscontratoplanilla')
    model = DatosContratoPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoPlanillaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="datos del contrato de planilla"
        return context

    def form_valid(self, form):
        usuario_honorario = DatosContratoHonorarios.objects.filter(usuario = form.instance.usuario)
        if len(usuario_honorario)>0:
            form.add_error('usuario', 'El usuario tiene contrato por honorarios.')
            return super().form_invalid(form)

        usuario_planilla = DatosContratoPlanilla.objects.filter(
                usuario = form.instance.usuario,
                estado_alta_baja = 1)
        if usuario_planilla:
            form.add_error('usuario', 'El usuario tiene un contrato activo por planilla.')
            return super().form_invalid(form)

        ultima_fecha_baja = DatosContratoPlanilla.objects.filter(usuario = form.instance.usuario).exclude(fecha_baja=None)        
        if ultima_fecha_baja:
            if ultima_fecha_baja.latest('fecha_baja').fecha_baja > form.instance.fecha_alta:
                form.add_error('fecha_alta','La fecha de alta tiene que ser mayor a la ultima fecha de baja (%s)' % ultima_fecha_baja.latest('fecha_baja').fecha_baja.strftime("%d/%m/%Y"))
                return super().form_invalid(form)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class DatosContratoPlanillaUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('colaborador.change_datoscontratoplanilla')
    model = DatosContratoPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoActualizarPlanillaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        form.instance.estado_alta_baja = 1
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Contrato por Planilla'
        return context

class DatosContratoPlanillaDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('colaborador.change_datoscontratoplanilla')
    model = DatosContratoPlanilla
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoPlanillaDarBajaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_planilla_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        form.instance.estado_alta_baja = 2
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoPlanillaDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'al contrato planilla'
        return context


class DatosContratoHonorariosListView(PermissionRequiredMixin, ListView):
    permission_required = ('colaborador.view_datoscontratohonorarios')
    model = DatosContratoHonorarios
    template_name = "colaborador/datos_contrato/honorarios/inicio.html"
    context_object_name = 'contexto_datoscontratohonorarios'

    def get_queryset(self):
        queryset = super(DatosContratoHonorariosListView, self).get_queryset()
        queryset = DatosContratoHonorarios.objects.exclude(estado_alta_baja=2)
        return queryset

def DatosContratoHonorariosTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'colaborador/datos_contrato/honorarios/inicio_tabla.html'
        context = {}
        datoscontratohonorarios = DatosContratoHonorarios.objects.exclude(estado_alta_baja = 2)
        context['contexto_datoscontratohonorarios'] = datoscontratohonorarios

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class DatosContratoHonorariosCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('colaborador.add_datoscontratohonorarios')
    model = DatosContratoHonorarios
    template_name = "colaborador/datos_contrato/honorarios/form.html"
    form_class = DatosContratoHonorariosForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_honorarios_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super(DatosContratoHonorariosCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="datos del contrato por honorarios"
        return context

    def form_valid(self, form):
        usuario_planilla =  DatosContratoPlanilla.objects.filter(usuario = form.instance.usuario)
        if len(usuario_planilla)>0:
            form.add_error('usuario', 'El usuario tiene contrato por planilla.')
            return super().form_invalid(form)
        
        usuario_planilla = DatosContratoHonorarios.objects.filter(
        usuario = form.instance.usuario,
        estado_alta_baja = 1)
        if usuario_planilla:
            form.add_error('usuario', 'El usuario tiene un contrato activo por recibo por honorarios.')
            return super().form_invalid(form)

        ultima_fecha_baja = DatosContratoHonorarios.objects.filter(usuario = form.instance.usuario).exclude(fecha_baja=None)        
        if ultima_fecha_baja:
            if ultima_fecha_baja.latest('fecha_baja').fecha_baja > form.instance.fecha_alta:
                form.add_error('fecha_alta','La fecha de alta tiene que ser mayor a la ultima fecha de baja (%s)' % ultima_fecha_baja.latest('fecha_baja').fecha_baja.strftime("%d/%m/%Y"))
                return super().form_invalid(form)

        if not form.instance.suspension_cuarta:
            form.instance.archivo_suspension_cuarta = None

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class DatosContratoHonorariosUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('colaborador.change_datoscontratohonorarios')
    model = DatosContratoHonorarios
    template_name = "colaborador/datos_contrato/honorarios/form.html"
    form_class = DatosContratoActualizarHonorariosForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_honorarios_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        if not form.instance.suspension_cuarta:
            form.instance.archivo_suspension_cuarta = None
        form.instance.estado_alta_baja = 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoHonorariosUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Contrato por Honorarios'
        return context

class DatosContratoHonorariosDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('colaborador.change_datoscontratohonorarios')
    model = DatosContratoHonorarios
    template_name = "includes/formulario generico.html"
    form_class = DatosContratoHonorariosDarBajaForm
    success_url = reverse_lazy('colaborador_app:datos_contrato_honorarios_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        form.instance.estado_alta_baja = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DatosContratoHonorariosDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = 'Dar de Baja'
        context['titulo'] = 'al contrato por honorarios'
        return context
