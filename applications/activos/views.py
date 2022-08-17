from django.shortcuts import render
from applications.activos.models import Activo, ActivoBase, ActivoUbicacion, ActivoSociedad, ActivoUbicacion, ArchivoComprobanteCompraActivo, ComprobanteCompraActivo, ComprobanteCompraActivoDetalle, MarcaActivo, ModeloActivo
from applications.importaciones import *

from bootstrap_modal_forms.generic import BSModalCreateView
from .forms import ActivoBaseForm, ActivoForm, ActivoSociedadForm, ActivoUbicacionForm, ComprobanteCompraActivoDetalleForm, ComprobanteCompraActivoForm, MarcaActivoForm, ModeloActivoForm


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

class ModeloActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_modeloactivo')

    model = ModeloActivo
    template_name = "activos/modelo_activo/inicio.html"
    context_object_name = 'contexto_modelo_activo'

def ModeloActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/modelo_activo/inicio_tabla.html'
        context = {}
        context['contexto_modelo_activo'] = ModeloActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ModeloActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_modeloactivo')
    model = ModeloActivo
    template_name = "includes/formulario generico.html"
    form_class = ModeloActivoForm
    success_url = reverse_lazy('activos_app:modelo_activo_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModeloActivoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Modelo Activo"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class ModeloActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_modeloactivo')
    model = ModeloActivo
    template_name = "includes/formulario generico.html"
    form_class = ModeloActivoForm
    success_url = reverse_lazy('activos_app:modelo_activo_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModeloActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Modelo Activo"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class MarcaActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_marcaactivo')

    model = MarcaActivo
    template_name = "activos/marca_activo/inicio.html"
    context_object_name = 'contexto_marca_activo'

def MarcaActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/marca_activo/inicio_tabla.html'
        context = {}
        context['contexto_marca_activo'] = MarcaActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class MarcaActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_marcaactivo')
    model = MarcaActivo
    template_name = "includes/formulario generico.html"
    form_class = MarcaActivoForm
    success_url = reverse_lazy('activos_app:marca_activo_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarcaActivoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Marca Activo"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class MarcaActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_marcaactivo')
    model = MarcaActivo
    template_name = "includes/formulario generico.html"
    form_class = MarcaActivoForm
    success_url = reverse_lazy('activos_app:marca_activo_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarcaActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Marca Activo"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class ActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_activo')
    model = Activo
    template_name = "activos/activo/inicio.html"
    context_object_name = 'contexto_activo'

def ActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/activo/inicio_tabla.html'
        context = {}
        context['contexto_activo'] = Activo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)  

class ActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_activo')
    model = Activo
    template_name = "includes/formulario generico.html"
    form_class = ActivoForm
    success_url = reverse_lazy('activos_app:activo_inicio')

    def get_context_data(self, **kwargs):
            context = super(ActivoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Activo"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_activo')

    model = Activo
    template_name = "includes/formulario generico.html"
    form_class = ActivoForm
    success_url = reverse_lazy('activos_app:activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(ActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Activo"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_activo')
    model = Activo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(ActivoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Activo"
        return context

class ActivoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('activos.view_activo')

    model = Activo
    template_name = "activos/activo/detalle.html"
    context_object_name = 'contexto_activo_detalle'

    def get_context_data(self, **kwargs):
        activo = Activo.objects.get(id = self.kwargs['pk'])
        context = super(ActivoDetailView, self).get_context_data(**kwargs)
        context['activo_sociedad'] = ActivoSociedad.objects.filter(activo = activo)
        context['activo_ubicacion'] = ActivoUbicacion.objects.filter(activo = activo )
        return context

def ActivoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'activos/activo/detalle_tabla.html'
        context = {}
        activo = Activo.objects.get(id = pk)
        context['contexto_activo_detalle'] = activo
        context['activo_sociedad'] = ActivoSociedad.objects.filter(activo = activo)
        context['activo_ubicacion'] = ActivoUbicacion.objects.filter(activo = activo )
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ActivoSociedadCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('activos.add_activosociedad')
    model = ActivoSociedad
    template_name = "includes/formulario generico.html"
    form_class = ActivoSociedadForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:activo_detalle', kwargs={'pk':self.kwargs['activo_id']})

    def form_valid(self, form):
        form.instance.activo = Activo.objects.get(id = self.kwargs['activo_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivoSociedadCreateView, self).get_context_data(**kwargs)
        context['accion']="Relacionar"
        context['titulo']="Sociedad"
        return context

class ActivoSociedadUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('activos.change_activosociedad')
    model = ActivoSociedad
    template_name = "includes/formulario generico.html"
    form_class = ActivoSociedadForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:activo_detalle', kwargs={'pk':self.object.activo.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivoSociedadUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Relación Sociedad"
        return context

class ActivoUbicacionCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('activos.add_activoubicacion')
    model = ActivoUbicacion
    template_name = "includes/formulario generico.html"
    form_class = ActivoUbicacionForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:activo_detalle', kwargs={'pk':self.kwargs['activo_id']})

    def form_valid(self, form):
        form.instance.activo = Activo.objects.get(id = self.kwargs['activo_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivoUbicacionCreateView, self).get_context_data(**kwargs)
        context['accion']="Relacionar"
        context['titulo']="Ubicacion"
        return context

class ActivoUbicacionUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('activos.change_activoubicacion')
    model = ActivoUbicacion
    template_name = "includes/formulario generico.html"
    form_class = ActivoUbicacionForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:activo_detalle', kwargs={'pk':self.object.activo.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivoUbicacionUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Relación Ubicacion"
        return context

class ComprobanteCompraActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_comprobantecompraactivo')
    model = ComprobanteCompraActivo
    template_name = "activos/comprobante_compra_activo/inicio.html"
    context_object_name = 'contexto_comprobante_compra_activo'

def ComprobanteCompraActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/comprobante_compra_activo/inicio_tabla.html'
        context = {}
        context['contexto_comprobante_compra_activo'] = ComprobanteCompraActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ComprobanteCompraActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_comprobantecompraactivo')
    model = ComprobanteCompraActivo
    template_name = "includes/formulario generico.html"
    form_class = ComprobanteCompraActivoForm
    success_url = reverse_lazy('activos_app:comprobante_compra_activo_inicio')

    def get_context_data(self, **kwargs):
            context = super(ComprobanteCompraActivoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Activo"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ComprobanteCompraActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_comprobantecompraactivo')

    model = ComprobanteCompraActivo
    template_name = "includes/formulario generico.html"
    form_class = ComprobanteCompraActivoForm
    success_url = reverse_lazy('activos_app:comprobante_compra_activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Comprobante de Compra"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ComprobanteCompraActivoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('activos.view_comprobantecompraactivo')

    model = ComprobanteCompraActivo
    template_name = "activos/comprobante_compra_activo/detalle.html"
    context_object_name = 'contexto_comprobante_compra_activo_detalle'

    def get_context_data(self, **kwargs):
        comprobante_compra_activo = ComprobanteCompraActivo.objects.get(id = self.kwargs['pk'])
        context = super(ComprobanteCompraActivoDetailView, self).get_context_data(**kwargs)
        context['activos'] = ComprobanteCompraActivoDetalle.objects.filter(comprobante_compra_activo = comprobante_compra_activo)
        context['archivos'] = ArchivoComprobanteCompraActivo.objects.filter(comprobante_compra_activo = comprobante_compra_activo)
        return context

def ComprobanteCompraActivoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'activos/comprobante_compra_activo/detalle_tabla.html'
        context = {}
        comprobante_compra_activo = ComprobanteCompraActivo.objects.get(id = pk)
        context['contexto_comprobante_compra_activo_detalle'] = comprobante_compra_activo
        context['activos'] = ComprobanteCompraActivoDetalle.objects.filter(comprobante_compra_activo = comprobante_compra_activo)
        context['archivos'] = ArchivoComprobanteCompraActivo.objects.filter(comprobante_compra_activo = comprobante_compra_activo)
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ComprobanteCompraActivoDetalleCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('activos.add_comprobantecompraactivodetalle')
    model = ComprobanteCompraActivoDetalle
    template_name = "activos/comprobante_compra_activo/registrar.html"
    form_class = ComprobanteCompraActivoDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:comprobante_compra_activo_detalle', kwargs={'pk':self.kwargs['comprobante_compra_activo_id']})

    def form_valid(self, form):
        form.instance.comprobante_compra_activo = ComprobanteCompraActivo.objects.get(id = self.kwargs['comprobante_compra_activo_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraActivoDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Activo"
        return context