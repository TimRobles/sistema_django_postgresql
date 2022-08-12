from django.shortcuts import render
from applications.activos.models import ActivoBase
from applications.importaciones import *

from bootstrap_modal_forms.generic import BSModalCreateView
from .forms import ActivoBaseForm


class ActivoBaseListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_activo_base')
    model = ActivoBase
    template_name = "activos/activo_base/inicio.html"
    context_object_name = 'contexto_activo_base'


def ActivoBaseTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/activo_base/inicio_tabla.html'
        context = {}
        context['contexto_activo_base'] = ActivoBase.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)  


class ActivoBaseCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_activo_base')
    model = ActivoBase
    template_name = "activos/activo_base/registro.html"
    form_class = ActivoBaseForm
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def get_context_data(self, **kwargs):
            context = super(ActivoBaseCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Activo Base"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class ActivoBaseUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_activo_base')

    model = ActivoBase
    template_name = "activos/activo_base/registro.html"
    form_class = ActivoBaseForm
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def get_context_data(self, **kwargs):
        context = super(ActivoBaseUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Activo Base"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ActivoBaseDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_activo_base')

    model = ActivoBase
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ActivoBaseDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Activo Base"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_corta
        return context

class ActivoBaseDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_activo_base')

    model = ActivoBase
    template_name = "includes/dar_alta_generico.html"
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ActivoBaseDarAltaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Alta"
        context['titulo'] = "Activo Base"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_corta
        return context