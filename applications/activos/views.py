from django.shortcuts import render
from applications.activos.models import (
    ActivoBase,
    ArchivoAsignacionActivo,
    ArchivoDevolucionActivo,
    AsignacionActivo,
    AsignacionDetalleActivo,
    DevolucionActivo,
    DevolucionDetalleActivo,
    InventarioActivo,
    InventarioActivoDetalle,
    SubFamiliaActivo,
    Activo,
    ActivoUbicacion,
    ActivoSociedad,
    ArchivoComprobanteCompraActivo,
    ComprobanteCompraActivo,
    ComprobanteCompraActivoDetalle,
    MarcaActivo,
    ModeloActivo,
    )
from applications.activos.pdf import generarAsignacionActivos
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat
from applications.importaciones import *
from django import forms
from bootstrap_modal_forms.generic import BSModalCreateView
from applications.funciones import obtener_totales

from .forms import (
    ActivoBaseForm,
    ActivoForm,
    ActivoSociedadForm,
    ActivoUbicacionForm,
    ArchivoDevolucionActivoForm,
    ComprobanteCompraActivoDetalleForm,
    ComprobanteCompraActivoForm,
    DevolucionActivoForm,
    DevolucionDetalleActivoForm,
    ArchivoComprobanteCompraActivoDetalleForm,
    ComprobanteCompraActivoDetalleForm,
    ComprobanteCompraActivoForm,
    InventarioActivoForm,
    MarcaActivoForm,
    ModeloActivoForm,
    ArchivoAsignacionActivoForm,
    AsignacionActivoForm,
    AsignacionDetalleActivoForm,
    ProductoSunatActivoForm,
    )

class SubFamiliaActivoForm(forms.Form):
    sub_familia = forms.ModelChoiceField(queryset = SubFamiliaActivo.objects.all(), required=False)


def SubFamiliaActivoView(request, id_familia):
    form = SubFamiliaActivoForm()
    form.fields['sub_familia'].queryset = SubFamiliaActivo.objects.filter(familia = id_familia)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)


class ProductoSunatActivoUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_material')
    model = ActivoBase
    template_name = "material/material/form_sunat.html"
    form_class = ProductoSunatActivoForm
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('activos_app:activo_base_inicio')
        # return reverse_lazy('activos_app:activo_base_inicio', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoSunatActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Producto Sunat"
        return context


class FamiliaSunatActivoForm(forms.Form):
    familia = forms.ModelChoiceField(queryset = FamiliaSunat.objects.all(), required=False)

def FamiliaSunatActivoView(request, id_segmento):
    form = FamiliaSunatActivoForm()
    form.fields['familia'].queryset = FamiliaSunat.objects.filter(segmento = id_segmento)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)


class ClaseSunatActivoForm(forms.Form):
    clase = forms.ModelChoiceField(queryset = ClaseSunat.objects.all(), required=False)

def ClaseSunatActivoView(request, id_familia):
    form = ClaseSunatActivoForm()
    form.fields['clase'].queryset = ClaseSunat.objects.filter(familia = id_familia)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)


class ProductoSunatActivoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset = ProductoSunat.objects.all(), required=False)

def ProductoSunatActivoView(request, id_clase):
    form = ProductoSunatActivoForm()
    form.fields['producto'].queryset = ProductoSunat.objects.filter(clase = id_clase)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)


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
    template_name = "activos/activo_base/form_activo_base.html"
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
    # template_name = "activos/activo_base/registro.html"
    template_name = "activos/activo_base/form_activo_base.html"
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


class AsignacionActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_asignacion_activo')
    model = AsignacionActivo
    template_name = "activos/asignacion_activo/inicio.html"
    context_object_name = 'contexto_asignacion_activo'


def AsignacionActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/asignacion_activo/inicio_tabla.html'
        context = {}
        context['contexto_asignacion_activo'] = AsignacionActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

    
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


class AsignacionActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_asignacion_activo')
    model = AsignacionActivo
    # template_name = "activos/asignacion_activo/form_asignacion_activo.html"
    template_name = "includes/formulario generico.html"
    form_class = AsignacionActivoForm
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def get_context_data(self, **kwargs):
            context = super(AsignacionActivoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Asignación Activo"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class AsignacionActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/formulario generico.html"
    form_class = AsignacionActivoForm
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Asignación de Activos"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class AsignacionActivoEntregarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()

        asignacion_activo_id = self.object.id
        asignaciones = AsignacionDetalleActivo.objects.filter(asignacion=asignacion_activo_id)
        list_activos_id = []
        for asignacion in asignaciones:
            list_activos_id.append(asignacion.activo.id)
        if list_activos_id != []:
            Activo.objects.filter(id__in=list_activos_id).update(estado=3)

        messages.success(request, MENSAJE_ACTUALIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoEntregarView, self).get_context_data(**kwargs)
        context['accion'] = "Entregar"
        context['titulo'] = "Asignación de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_asignacion)
        return context


class AsignacionActivoDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 4
        registro_guardar(self.object, self.request)
        self.object.save()
        asignacion_activo_id = self.object.id
        asignaciones = AsignacionDetalleActivo.objects.filter(asignacion=asignacion_activo_id)
        list_activos_id = []
        for asignacion in asignaciones:
            list_activos_id.append(asignacion.activo.id)
        if list_activos_id != []:
            Activo.objects.filter(id__in=list_activos_id).update(estado=1)
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Asignación de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_asignacion)
        return context


class AsignacionActivoConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        asignacion_activo_id = self.object.id
        asignaciones = AsignacionDetalleActivo.objects.filter(asignacion=asignacion_activo_id)
        list_activos_id = []
        for asignacion in asignaciones:
            list_activos_id.append(asignacion.activo.id)
        if list_activos_id != []:
            Activo.objects.filter(id__in=list_activos_id).update(estado=1)
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir sin Asignar"
        context['titulo'] = "Asignación de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_asignacion)
        return context


class AsignacionActivoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('activos.view_asignacion_activo_detalle')
    model = AsignacionActivo
    template_name = "activos/asignacion_activo/inicio_detalle.html"
    context_object_name = 'contexto_asignacion_activo'

    def get_context_data(self, **kwargs):
        asignacion = AsignacionActivo.objects.get(id = self.kwargs['pk'])
        context = super(AsignacionActivoDetailView, self).get_context_data(**kwargs)
        context['contexto_asignacion_activo_detalle'] = AsignacionDetalleActivo.objects.filter(asignacion = asignacion)
        context['contexto_asignacion_activo_archivo'] = ArchivoAsignacionActivo.objects.filter(asignacion = asignacion)
        return context


def AsignacionActivoDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'activos/asignacion_activo/inicio_tabla_detalle.html'
        context = {}
        asignacion = AsignacionActivo.objects.get(id = pk)
        context['contexto_asignacion_activo'] = asignacion
        context['contexto_asignacion_activo_detalle'] = AsignacionDetalleActivo.objects.filter(asignacion = asignacion)
        context['contexto_asignacion_activo_archivo'] = ArchivoAsignacionActivo.objects.filter(asignacion = asignacion)
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


# Lo hizo Tim, referencia

# class AsignacionActivoDetailView(PermissionRequiredMixin, DetailView):
#     permission_required = ('activos.view_asignacion_activo_detalle')
#     model = AsignacionActivo
#     template_name = "activos/asignacion_activo/inicio_detalle.html"
#     context_object_name = 'contexto_asignacion_activo'

#     def get_context_data(self, **kwargs):
#         context = super(AsignacionActivoDetailView, self).get_context_data(**kwargs)
#         context['contexto_asignacion_activo_detalle'] = self.object.AsignacionDetalleActivo_asignacion.all()
#         return context


# def AsignacionActivoDetalleTabla(request, pk):
#     data = dict()
#     if request.method == 'GET':
#         template = 'activos/asignacion_activo/inicio_tabla_detalle.html'
#         context = {}
#         detalle_asignacion = AsignacionDetalleActivo.objects.get(id = pk)
#         context['contexto_asignacion_activo_detalle'] = detalle_asignacion

#         data['table'] = render_to_string(
#             template,
#             context,
#             request=request
#         )
#         return JsonResponse(data)  


class AsignacionDetalleActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_asignacion_activo_detalle')
    model = AsignacionDetalleActivo
    template_name = "includes/formulario generico.html"
    form_class = AsignacionDetalleActivoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk': self.kwargs['asignacion_id']})

    def form_valid(self, form):
        form.instance.asignacion = AsignacionActivo.objects.get(id = self.kwargs['asignacion_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(AsignacionDetalleActivoCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar Item"
        context['titulo']="Asignación de Activo"
        return context

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


class AsignacionDetalleActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.add_asignacion_activo_detalle')
    model = AsignacionDetalleActivo
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_asignacion_detalle_activo_eliminar' 

    def get_success_url(self, **kwargs):
        print(15*'*', 'DELETE')
        print('id:', self.object.activo.id)
        print('descripcion:', self.object.activo.descripcion)
        Activo.objects.filter(id=self.object.activo.id).update(estado=1)
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk':self.object.asignacion.id})

    def get_context_data(self, **kwargs):
        context = super(AsignacionDetalleActivoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Item de Asignación"
        context['dar_baja'] = "True"
        context['item'] = self.object.activo.descripcion
        return context


class ArchivoAsignacionActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_archivo_asignacion_activo')
    model = ArchivoAsignacionActivo
    template_name = "includes/formulario generico.html"
    form_class = ArchivoAsignacionActivoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk': self.kwargs['asignacion_id']})
    
    def form_valid(self, form):
        form.instance.asignacion = AsignacionActivo.objects.get(id = self.kwargs['asignacion_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoAsignacionActivoCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Documento"
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



class ArchivoAsignacionActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_archivo_asignacion_activo')
    model = ArchivoAsignacionActivo
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_asignacion_activo_archivo' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk':self.object.asignacion.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoAsignacionActivoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Archivo de Asignación"
        context['dar_baja'] = "True"
        context['item'] = self.object.archivo
        return context


class AsignacionActivoPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Asignación de Activos'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = AsignacionActivo.objects.get(id=self.kwargs['pk'])

        fecha = datetime.strftime(obj.fecha_asignacion,'%d - %m - %Y')

        texto_1 = obj.titulo + '\n' +str(obj.colaborador) + '\n' + str(fecha) + '\n'
        texto_2 = ''' En la Ciudad de Lima, con fecha, %s , se recibe de parte del Ing. BASILIO ALVAREZ ZAPATA, identificado con DNI° 19924516, Representante Legal de la Empresa MULTICABLE PERU SAC, con domicilio fiscal en Av. Petit Thouars N°3629 Urb. Fundo Chacarilla - San Isidro, con RUC N°20522137465, el/los equipo(s) que se especifica(n) a continuación:''' %(str(fecha))
        texto_3 = ''' Al momento de recibir el/los equipo(s) especificados se realizaron pruebas, encontrándose en buen estado físico y de funcionamiento.\n
            De acuerdo a lo anterior se hace constar que el/los equipo(s) se encuentran en las condiciones adecuadas para recibirlo(s). '''
        
        Texto = []
        Texto.extend([texto_1, texto_2, texto_3])
        
        TablaEncabezado = [
            'NRO', 
            'REFERENCIA',
            'DESCRIPCIÓN', 
            'MARCA', 
            'NRO. SERIE', 
            'COLOR', 
            ]

        detalle = obj.AsignacionDetalleActivo_asignacion
        activos = detalle.all()

        TablaDatos = []
        count = 1
        for activo in activos:
            # material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(
            #     id = material.id_requerimiento_material_detalle.id_registro
            #     )
            # proveedor_material = ProveedorMaterial.objects.get(
            #     content_type = ContentType.objects.get_for_model(material.material),
            #     id_registro = material.material.id,
            #     proveedor = obj.proveedor,
            #     estado_alta_baja = 1,
            #     )
            fila = []
            fila.append(str(count))
            fila.append(activo.activo.activo_base.descripcion_corta)
            fila.append(activo.activo.descripcion)
            if activo.activo.marca:
                fila.append(activo.activo.marca.nombre)
            else:
                fila.append('-')
            fila.append(activo.activo.numero_serie)
            if activo.activo.color:
                fila.append(activo.activo.color)
            else:
                fila.append('-')
            TablaDatos.append(fila)
            count += 1


        tabla_firmas = [
            ['', '------------------------', '', '------------------------', ''],
            ['', 'Recibe el/los equipo(s)', '', 'Entrega el/los equipo(s)', ''],
            ['', str(obj.colaborador), '', 'ING. BASILIO ÁLVAREZ ZAPATA', '']
            ]
        

        buf = generarAsignacionActivos(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color, tabla_firmas)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        # obj.estado = 2
        # obj.save()

        return respuesta

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
        context['totales'] = obtener_totales(ComprobanteCompraActivo.objects.get(id = self.kwargs['pk']))
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
        context['totales'] = obtener_totales(ComprobanteCompraActivo.objects.get(id = pk))
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
        item = len(ComprobanteCompraActivoDetalle.objects.filter(comprobante_compra_activo = form.instance.comprobante_compra_activo))
        form.instance.item = item + 1
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraActivoDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Activo"
        return context


class DevolucionActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_devolucion_activo')
    model = DevolucionActivo
    template_name = "activos/devolucion_activo/inicio.html"
    context_object_name = 'contexto_devolucion_activo'


def DevolucionActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/devolucion_activo/inicio_tabla.html'
        context = {}
        context['contexto_devolucion_activo'] = DevolucionActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DevolucionActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_devolucion_activo')
    model = DevolucionActivo
    template_name = "includes/formulario generico.html"
    form_class = DevolucionActivoForm
    success_url = reverse_lazy('activos_app:devolucion_activo_inicio')

    def get_context_data(self, **kwargs):
            context = super(DevolucionActivoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Devolución Activo"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class DevolucionActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_devolucion_activo')
    model = DevolucionActivo
    template_name = "includes/formulario generico.html"
    form_class = DevolucionActivoForm
    success_url = reverse_lazy('activos_app:devolucion_activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(DevolucionActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Devolución de Activos"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class DevolucionActivoDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_devolucion_activo')
    model = DevolucionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:devolucion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        devolucion_activo_id = self.object.id
        devoluciones = DevolucionDetalleActivo.objects.filter(devolucion=devolucion_activo_id)
        list_activos_id = []
        for devolucion in devoluciones:
            list_activos_id.append(devolucion.activo.id)
        if list_activos_id != []:
            Activo.objects.filter(id__in=list_activos_id).update(estado=3)
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DevolucionActivoDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Devolución de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_devolucion)
        return context


class DevolucionActivoRecepcionarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_devolucion_activo')
    model = DevolucionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:devolucion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()

        devolucion_activo_id = self.object.id
        devoluciones = DevolucionDetalleActivo.objects.filter(devolucion=devolucion_activo_id)
        list_activos_id = []
        for devolucion in devoluciones:
            list_activos_id.append(devolucion.activo.id)
        if list_activos_id != []:
            Activo.objects.filter(id__in=list_activos_id).update(estado=1)

        messages.success(request, MENSAJE_ACTUALIZACION)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DevolucionActivoRecepcionarView, self).get_context_data(**kwargs)
        context['accion'] = "Recepcionar"
        context['titulo'] = "Devolución de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_devolucion)
        return context


class DevolucionActivoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('activos.view_devolucion_activo_detalle')
    model = DevolucionActivo
    template_name = "activos/devolucion_activo/inicio_detalle.html"
    context_object_name = 'contexto_devolucion_activo'

    def get_context_data(self, **kwargs):
        devolucion = DevolucionActivo.objects.get(id = self.kwargs['pk'])
        context = super(DevolucionActivoDetailView, self).get_context_data(**kwargs)
        context['contexto_devolucion_activo_detalle'] = DevolucionDetalleActivo.objects.filter(devolucion = devolucion)
        context['contexto_devolucion_activo_archivo'] = ArchivoDevolucionActivo.objects.filter(devolucion = devolucion)
        return context


def DevolucionActivoDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'activos/devolucion_activo/inicio_tabla_detalle.html'
        context = {}
        devolucion = DevolucionActivo.objects.get(id = pk)
        context['contexto_devolucion_activo'] = devolucion
        context['contexto_devolucion_activo_detalle'] = DevolucionDetalleActivo.objects.filter(devolucion = devolucion)
        context['contexto_devolucion_activo_archivo'] = ArchivoDevolucionActivo.objects.filter(devolucion = devolucion)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ComprobanteCompraActivoDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_comprobantecompraactivodetalle')

    model = ComprobanteCompraActivoDetalle
    template_name = "activos/comprobante_compra_activo/registrar.html"
    form_class = ComprobanteCompraActivoDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:comprobante_compra_activo_detalle', kwargs={'pk':self.get_object().comprobante_compra_activo_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraActivoDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        return context

class ComprobanteCompraActivoDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_comprobantecompraactivodetalle')
    model = ComprobanteCompraActivoDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:comprobante_compra_activo_detalle', kwargs={'pk':self.object.comprobante_compra_activo.id})

    def delete(self, request, *args, **kwargs):
        activos = ComprobanteCompraActivoDetalle.objects.filter(comprobante_compra_activo=self.get_object().comprobante_compra_activo)
        contador = 1
        for activo in activos:
            if activo == self.get_object():continue
            activo.item = contador
            activo.save()
            contador += 1

        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComprobanteCompraActivoDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Registro"
        return context

class ArchivoComprobanteCompraActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_archivocomprobantecompraactivo')
    model = ArchivoComprobanteCompraActivo
    template_name = "includes/formulario generico.html"
    form_class = ArchivoComprobanteCompraActivoDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:comprobante_compra_activo_detalle', kwargs={'pk':self.kwargs['comprobante_compra_activo_id']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.comprobante_compra_activo = ComprobanteCompraActivo.objects.get(id = self.kwargs['comprobante_compra_activo_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoComprobanteCompraActivoCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar"
        context['titulo']="Documento"
        return context

class ArchivoComprobanteCompraActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_archivocomprobantecompraactivo')
    model =ArchivoComprobanteCompraActivo
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:comprobante_compra_activo_detalle', kwargs={'pk':self.object.comprobante_compra_activo.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoComprobanteCompraActivoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Documento"
        return context

class InventarioActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_inventarioactivo')
    model = InventarioActivo
    template_name = "activos/inventario_activo/inicio.html"
    context_object_name = 'contexto_inventario_activo'

def InventarioActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/inventario_activo/inicio_tabla.html'
        context = {}
        context['contexto_inventario_activo'] = InventarioActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DevolucionDetalleActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_devolucion_activo_detalle')
    model = DevolucionDetalleActivo
    template_name = "includes/formulario generico.html"
    form_class = DevolucionDetalleActivoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:devolucion_activo_detalle_inicio', kwargs={'pk': self.kwargs['devolucion_id']})

    def form_valid(self, form):
        form.instance.devolucion = DevolucionActivo.objects.get(id = self.kwargs['devolucion_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(DevolucionDetalleActivoCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar Item"
        context['titulo']="Devolución de Activo"
        return context


class DevolucionDetalleActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.add_devolucion_activo_detalle')
    model = DevolucionDetalleActivo
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_devolucion_detalle_activo_eliminar' 

    def get_success_url(self, **kwargs):
        Activo.objects.filter(id=self.object.activo.id).update(estado=3)
        return reverse_lazy('activos_app:devolucion_activo_detalle_inicio', kwargs={'pk':self.object.devolucion.id})

    def get_context_data(self, **kwargs):
        context = super(DevolucionDetalleActivoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Item de Devolución"
        context['dar_baja'] = "True"
        context['item'] = self.object.activo.descripcion
        return context


class DevolucionActivoPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Devolución de Activos'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = DevolucionActivo.objects.get(id=self.kwargs['pk'])

        fecha = datetime.strftime(obj.fecha_devolucion,'%d - %m - %Y')

        texto_1 = obj.titulo + '\n' +str(obj.colaborador) + '\n' + str(fecha) + '\n'
        texto_2 = ''' En la Ciudad de Lima, con fecha, %s , se recibe a nombre del Ing. BASILIO ALVAREZ ZAPATA, identificado con DNI° 19924516, Representante Legal de la Empresa MULTICABLE PERU SAC, con domicilio fiscal en Av. Petit Thouars N°3629 Urb. Fundo Chacarilla - San Isidro, con RUC N°20522137465, el/los equipo(s) que se especifica(n) a continuación:''' %(str(fecha))
        texto_3 = ''' Al momento de recibir el/los equipo(s) especificados se realizaron pruebas, encontrándose en buen estado físico y de funcionamiento.\n
            De acuerdo a lo anterior se hace constar que el/los equipo(s) se encuentran en las condiciones adecuadas para recepcionarlo(s). '''
        
        Texto = []
        Texto.extend([texto_1, texto_2, texto_3])
        
        TablaEncabezado = [
            'NRO', 
            'REFERENCIA',
            'DESCRIPCIÓN', 
            'MARCA', 
            'NRO. SERIE', 
            'COLOR', 
            ]

        detalle = obj.DevolucionDetalleActivo_devolucion
        activos = detalle.all()

        TablaDatos = []
        count = 1
        for activo in activos:
            fila = []
            fila.append(str(count))
            fila.append(activo.activo.activo_base.descripcion_corta)
            fila.append(activo.activo.descripcion)
            if activo.activo.marca:
                fila.append(activo.activo.marca.nombre)
            else:
                fila.append('-')
            fila.append(activo.activo.numero_serie)
            if activo.activo.color:
                fila.append(activo.activo.color)
            else:
                fila.append('-')
            TablaDatos.append(fila)
            count += 1


        tabla_firmas = [
            ['', '------------------------', '', '------------------------', ''],
            ['', 'Entrega el/los equipo(s)', '', 'Recibe el/los equipo(s)', ''],
            ['', str(obj.colaborador), '', 'ING. BASILIO ÁLVAREZ ZAPATA', '']
            ]
        

        buf = generarAsignacionActivos(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color, tabla_firmas)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta


class ArchivoDevolucionActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_archivo_devolucion_activo')
    model = ArchivoDevolucionActivo
    template_name = "includes/formulario generico.html"
    form_class = ArchivoDevolucionActivoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:devolucion_activo_detalle_inicio', kwargs={'pk': self.kwargs['devolucion_id']})
    
    def form_valid(self, form):
        form.instance.devolucion = DevolucionActivo.objects.get(id = self.kwargs['devolucion_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoDevolucionActivoCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Documento"
        return context


class ArchivoDevolucionActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_archivo_devolucion_activo')
    model = ArchivoDevolucionActivo
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_devolucion_activo_archivo' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:devolucion_activo_detalle_inicio', kwargs={'pk':self.object.devolucion.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoDevolucionActivoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Archivo de Devolución"
        context['dar_baja'] = "True"
        context['item'] = self.object.archivo
        return context
    
class InventarioActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_inventarioactivo')
    model = InventarioActivo
    template_name = "includes/formulario generico.html"
    form_class = InventarioActivoForm
    success_url = reverse_lazy('activos_app:inventario_activo_inicio')

    def get_context_data(self, **kwargs):
            context = super(InventarioActivoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Inventario Activo"
            return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class InventarioActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_inventarioactivo')

    model = InventarioActivo
    template_name = "includes/formulario generico.html"
    form_class = InventarioActivoForm
    success_url = reverse_lazy('activos_app:inventario_activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(InventarioActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Inventario Activo"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class InventarioActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_inventarioactivo')
    model = InventarioActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:inventario_activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(InventarioActivoDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Inventario Activo"
        return context

class InventarioActivoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('activos.view_inventarioactivo')
    model = InventarioActivo
    template_name = "activos/inventario_activo/detalle.html"
    context_object_name = 'contexto_inventario_activo_detalle'

    def get_context_data(self, **kwargs):
        inventario_activo = InventarioActivo.objects.get(id = self.kwargs['pk'])
        context = super(InventarioActivoDetailView, self).get_context_data(**kwargs)
        context['registro_activos'] = Activo.objects.all()
        return context

def InventarioActivoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'activos/inventario_activo/detalle_tabla.html'
        context = {}
        inventario_activo = InventarioActivo.objects.get(id = pk)
        context['contexto_inventario_activo_detalle'] = inventario_activo
        context['registro_activos'] = Activo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
