from django.shortcuts import render
from decimal import Decimal
import json
from django import forms
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import SegmentoSunat, FamiliaSunat, ClaseSunat, ProductoSunat, Unidad
from applications.merchandising.funciones import stock, stock_disponible, stock_sede, stock_sede_disponible, stock_sede_tipo_stock, stock_tipo_stock
from applications.funciones import obtener_atributos, registrar_excepcion
from applications.importaciones import *
from applications.almacenes.models import Almacen
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from ..orden_compra.models import OrdenCompraDetalle

from .forms import (
    AjusteInventarioMerchandisingDetalleForm, AjusteInventarioMerchandisingForm, InventarioMerchandisingDetalleForm, InventarioMerchandisingForm, InventarioMerchandisingUpdateForm, MerchandisingBuscarForm, ModeloMerchandisingForm, MarcaMerchandisingForm, MerchandisingForm, ProductoSunatBuscarForm,
    RelacionMerchandisingComponenteForm, EspecificacionMerchandisingForm,
    DatasheetMerchandisingForm, DatosImportacionMerchandisingForm, ProductoSunatMerchandisingForm,
    ImagenMerchandisingForm,VideoMerchandisingForm,ProveedorMerchandisingForm,EquivalenciaUnidadMerchandisingForm,IdiomaMerchandisingForm,
    )

from .models import (
    AjusteInventarioMerchandising,
    AjusteInventarioMerchandisingDetalle,
    InventarioMerchandising,
    InventarioMerchandisingDetalle,
    ModeloMerchandising,
    MarcaMerchandising,
    Merchandising,
    RelacionMerchandisingComponente,
    EspecificacionMerchandising,
    DatasheetMerchandising,
    SubFamiliaMerchandising,
    ImagenMerchandising,
    VideoMerchandising,
    ProveedorMerchandising,
    EquivalenciaUnidadMerchandising,
    IdiomaMerchandising,
    )

class ModeloMerchandisingListView(PermissionRequiredMixin, ListView):
    permission_required = ('merchandising.view_modelo')
    model = ModeloMerchandising
    template_name = "merchandising/modelo/inicio.html"
    context_object_name = 'contexto_modelo_merchandising'

def ModeloMerchandisingTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/modelo/inicio_tabla.html'
        context = {}
        context['contexto_modelo_merchandising'] = ModeloMerchandising.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class ModeloMerchandisingCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('merchandising.add_modelo')
    model = ModeloMerchandising
    template_name = "includes/formulario generico.html"
    form_class = ModeloMerchandisingForm
    success_url = reverse_lazy('merchandising_app:modelo_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModeloMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Modelo Merchandising"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)
    

class ModeloMerchandisingUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('merchandising.change_modelo')
    model = ModeloMerchandising
    template_name = "includes/formulario generico.html"
    form_class = ModeloMerchandisingForm
    success_url = reverse_lazy('merchandising_app:modelo_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModeloMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Modelo Merchandising"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)
    

class MarcaMerchandisingListView(PermissionRequiredMixin, ListView):
    permission_required = ('merchandising.view_marca')
    model = MarcaMerchandising
    template_name = "merchandising/marca/inicio.html"
    context_object_name = 'contexto_marca_merchandising'

def MarcaMerchandisingTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/marca/inicio_tabla.html'
        context = {}
        context['contexto_marca_merchandising'] = MarcaMerchandising.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class MarcaMerchandisingCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('merchandising.add_marca')
    model = MarcaMerchandising
    template_name = "includes/formulario generico.html"
    form_class = MarcaMerchandisingForm
    success_url = reverse_lazy('merchandising_app:marca_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarcaMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Marca Merchandising"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class MarcaMerchandisingUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('merchandising.change_marca')
    model = MarcaMerchandising
    template_name = "includes/formulario generico.html"
    form_class = MarcaMerchandisingForm
    success_url = reverse_lazy('merchandising_app:marca_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarcaMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Marca Merchandising"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class MerchandisingListView(PermissionRequiredMixin, FormView):
    permission_required = ('merchandising.view_merchandising')
    template_name = "merchandising/merchandising/inicio.html"
    form_class = MerchandisingBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(MerchandisingListView, self).get_form_kwargs()
        kwargs['filtro'] = self.request.GET.get('buscar')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(MerchandisingListView,self).get_context_data(**kwargs)
        merchandising = Merchandising.objects.all().order_by('descripcion_venta','descripcion_corta','marca','modelo')
        filtro = self.request.GET.get('buscar')

        contexto_filtro = []

        if filtro:
            condicion = Q(descripcion_venta__unaccent__icontains = filtro.split(" ")[0]) | Q(descripcion_corta__unaccent__icontains = filtro.split(" ")[0]) | Q(marca__nombre__unaccent__icontains = filtro.split(" ")[0]) | Q(modelo__nombre__unaccent__icontains = filtro.split(" ")[0])
            for palabra in filtro.split(" ")[1:]:
                condicion &= Q(descripcion_venta__unaccent__icontains = palabra) | Q(descripcion_corta__unaccent__icontains = palabra) | Q(marca__nombre__unaccent__icontains = palabra) | Q(modelo__nombre__unaccent__icontains = palabra)
            merchandising = merchandising.filter(condicion)
            contexto_filtro.append("buscar=" + filtro)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        context['contexto_merchandising'] = merchandising
        return context


def MerchandisingTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/merchandising/inicio_tabla.html'
        context = {}
        merchandising = Merchandising.objects.all()
        filtro = request.GET.get('buscar')

        contexto_filtro = []

        if filtro:
            condicion = Q(descripcion_venta__unaccent__icontains = filtro.split(" ")[0]) | Q(descripcion_corta__unaccent__icontains = filtro.split(" ")[0]) | Q(marca__nombre__unaccent__icontains = filtro.split(" ")[0]) | Q(modelo__nombre__unaccent__icontains = filtro.split(" ")[0])
            for palabra in filtro.split(" ")[1:]:
                condicion &= Q(descripcion_venta__unaccent__icontains = palabra) | Q(descripcion_corta__unaccent__icontains = palabra) | Q(marca__nombre_unaccent__icontains = palabra) | Q(modelo__nombre__unaccent__icontains = palabra)
            merchandising = merchandising.filter(condicion)
            contexto_filtro.append("buscar=" + filtro)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        context['contexto_merchandising'] = merchandising

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class MerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_merchandising')
    model = Merchandising
    template_name = "merchandising/merchandising/form_merchandising.html"
    form_class = MerchandisingForm
    success_url = reverse_lazy('merchandising_app:merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Merchandising"
        return context


class MerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_merchandising')
    model = Merchandising
    template_name = "merchandising/merchandising/form_merchandising.html"
    form_class = MerchandisingForm
    success_url = reverse_lazy('merchandising_app:merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Merchandising"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class MerchandisingDarBajaView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_merchandising')
    model = Merchandising
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('merchandising_app:merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MerchandisingDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Merchandising"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_venta
        return context


class MerchandisingDarAltaView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_merchandising')
    model = Merchandising
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('merchandising_app:merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MerchandisingDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Merchandising"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_venta
        return context
    

class MerchandisingDetailView(PermissionRequiredMixin,DetailView):
    permission_required = ('merchandising.view_merchandising')
    model = Merchandising
    template_name = "merchandising/merchandising/detalle.html"
    context_object_name = 'contexto_merchandising'

    def get_context_data(self, **kwargs):
        merchandising = Merchandising.objects.get(id = self.kwargs['pk'])
        content_type = ContentType.objects.get_for_model(merchandising)

        context = super(MerchandisingDetailView, self).get_context_data(**kwargs)
        context['componentes'] = RelacionMerchandisingComponente.objects.filter(merchandising = merchandising)
        context['especificaciones'] = EspecificacionMerchandising.objects.filter(merchandising = merchandising)
        context['datasheets'] = DatasheetMerchandising.objects.filter(merchandising = merchandising)
        context['imagenes'] = ImagenMerchandising.objects.filter(merchandising = merchandising)
        context['videos'] = VideoMerchandising.objects.filter(merchandising = merchandising)
        context['proveedores'] = ProveedorMerchandising.objects.filter(content_type = content_type,id_registro=self.kwargs['pk'])
        context['equivalencias'] = EquivalenciaUnidadMerchandising.objects.filter(merchandising = merchandising)
        context['idiomas'] = IdiomaMerchandising.objects.filter(merchandising = merchandising)
        # context['precios'] = PrecioListaMerchandising.objects.filter(content_type_producto = content_type,id_registro_producto=self.kwargs['pk'])
        return context


def MerchandisingDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/merchandising/detalle_tabla.html'
        context = {}
        merchandising = Merchandising.objects.get(id = pk)
        content_type = ContentType.objects.get_for_model(merchandising)

        context['contexto_merchandising'] = merchandising
        context['componentes'] = RelacionMerchandisingComponente.objects.filter(merchandising = merchandising)
        context['especificaciones'] = EspecificacionMerchandising.objects.filter(merchandising = merchandising)
        context['datasheets'] = DatasheetMerchandising.objects.filter(merchandising = merchandising)
        context['imagenes'] = ImagenMerchandising.objects.filter(merchandising = merchandising)
        context['videos'] = VideoMerchandising.objects.filter(merchandising = merchandising)
        context['proveedores'] = ProveedorMerchandising.objects.filter(content_type = content_type,id_registro=pk)
        context['equivalencias'] = EquivalenciaUnidadMerchandising.objects.filter(merchandising = merchandising)
        context['idiomas'] = IdiomaMerchandising.objects.filter(merchandising = merchandising)
        # context['precios'] = PrecioListaMerchandising.objects.filter(content_type_producto = content_type,id_registro_producto=pk)


        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class ComponenteMerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_relacionmerchandisingcomponente')
    model = RelacionMerchandisingComponente
    template_name = "includes/formulario generico.html"
    form_class = RelacionMerchandisingComponenteForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        filtro = RelacionMerchandisingComponente.objects.filter(
            componentemerchandising = form.instance.componentemerchandising,
            merchandising = merchandising)
        if len(filtro)>0:
            form.add_error('componentemerchandising', 'El merchandising ya cuenta con el componente seleccionado.')
            return super().form_invalid(form)

        form.instance.merchandising = merchandising
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        kwargs = super(ComponenteMerchandisingCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['componentes'] = merchandising.subfamilia.componentes.all()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ComponenteMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Componente Merchandising"
        return context


class ComponenteMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_relacionmerchandisingcomponente')
    model = RelacionMerchandisingComponente
    template_name = "includes/formulario generico.html"
    form_class = RelacionMerchandisingComponenteForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ComponenteMerchandisingUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['componentes'] = self.object.merchandising.subfamilia.componentes.all()
        return kwargs

    def form_valid(self, form):
        filtro = RelacionMerchandisingComponente.objects.filter(
            componentemerchandising = form.instance.componentemerchandising,
            merchandising = self.object.merchandising).exclude(
                id = self.object.id
            )
        if len(filtro)>0:
            form.add_error('componentemerchandising', 'El merchandising ya cuenta con el componente seleccionado.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComponenteMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Componente Merchandising"
        return context


class ComponenteMerchandisingDeleteView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_relacionmerchandisingcomponente')
    model = RelacionMerchandisingComponente
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def get_context_data(self, **kwargs):
        context = super(ComponenteMerchandisingDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Componente Merchandising"
        return context
    

class EspecificacionMerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_especificacion')
    model = EspecificacionMerchandising
    template_name = "includes/formulario generico.html"
    form_class = EspecificacionMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        filtro = EspecificacionMerchandising.objects.filter(
            atributomerchandising = form.instance.atributomerchandising,
            merchandising = merchandising)
        if len(filtro)>0:
            form.add_error('atributomerchandising', 'El merchandising ya cuenta con el atributo seleccionado.')
            return super().form_invalid(form)

        form.instance.merchandising = merchandising
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        kwargs = super(EspecificacionMerchandisingCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['atributos'] = merchandising.subfamilia.familia.atributos.all()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EspecificacionMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Especificación"
        return context


class EspecificacionMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_especificacion')
    model = EspecificacionMerchandising
    template_name = "includes/formulario generico.html"
    form_class = EspecificacionMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EspecificacionMerchandisingUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['atributos'] = self.object.merchandising.subfamilia.familia.atributos.all()
        return kwargs

    def form_valid(self, form):
        filtro = EspecificacionMerchandising.objects.filter(
            atributomerchandising = form.instance.atributomerchandising,
            merchandising = self.object.merchandising).exclude(
                id = self.object.id
            )
        if len(filtro)>0:
            form.add_error('atributomerchandising', 'El merchandising ya cuenta con el atributo seleccionado.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EspecificacionMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Especificación"
        return context


class EspecificacionMerchandisingDeleteView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_especificacion')
    model = EspecificacionMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def get_context_data(self, **kwargs):
        context = super(EspecificacionMerchandisingDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Especificación"
        return context


class DatasheetMerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_datasheet')
    model = DatasheetMerchandising
    template_name = "includes/formulario generico.html"
    form_class = DatasheetMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        form.instance.merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatasheetMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Datasheet Merchandising"
        return context


class DatasheetMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_datasheet')
    model = DatasheetMerchandising
    template_name = "includes/formulario generico.html"
    form_class = DatasheetMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatasheetMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Datasheet Merchandising"
        return context


class DatasheetMerchandisingDeleteView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_datasheet')
    model = DatasheetMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def get_context_data(self, **kwargs):
        context = super(DatasheetMerchandisingDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Datasheet Merchandising"
        return context
    

class DatosImportacionMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_merchandising')
    model = Merchandising
    template_name = "includes/formulario generico.html"
    form_class = DatosImportacionMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatosImportacionMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Datos de Importación"
        return context


class ProductoSunatMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_merchandising')
    model = Merchandising
    template_name = "merchandising/merchandising/form_sunat.html"
    form_class = ProductoSunatMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoSunatMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Producto Sunat"
        return context


class ProductoSunatMerchandisingBuscarView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_merchandising')
    model = Merchandising
    template_name = "merchandising/merchandising/form_sunat_buscar.html"
    form_class = ProductoSunatBuscarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoSunatMerchandisingBuscarView, self).get_context_data(**kwargs)
        context['accion']="Buscar"
        context['titulo']="Producto Sunat"
        return context

def ProductoSunatJsonView(request):
    if request.is_ajax():
        term = request.GET.get('term')
        data = []
        if term:
            condicion = Q(descripcion__unaccent__icontains = term.split(" ")[0])
            for palabra in term.split(" ")[1:]:
                condicion &= Q(descripcion__unaccent__icontains = palabra)
            buscar = ProductoSunat.objects.filter(condicion)
        for producto_sunat in buscar:
            data.append({
                'id' : producto_sunat.codigo,
                'nombre' : producto_sunat.__str__(),
                })
        return JsonResponse(data, safe=False)


class FamiliaSunatForm(forms.Form):
    familia = forms.ModelChoiceField(queryset = FamiliaSunat.objects.all(), required=False)

def FamiliaSunatView(request, id_segmento):
    form = FamiliaSunatForm()
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


class ClaseSunatForm(forms.Form):
    clase = forms.ModelChoiceField(queryset = ClaseSunat.objects.all(), required=False)

def ClaseSunatView(request, id_familia):
    form = ClaseSunatForm()
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


class ProductoSunatForm(forms.Form):
    producto = forms.ModelChoiceField(queryset = ProductoSunat.objects.all(), required=False)

def ProductoSunatView(request, id_clase):
    form = ProductoSunatForm()
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


class SubfamiliaMerchandisingForm(forms.Form):
    subfamilia = forms.ModelChoiceField(queryset = SubFamiliaMerchandising.objects.all(), required=False)

def SubfamiliaMerchandisingView(request, id_familia):
    form = SubfamiliaMerchandisingForm()
    form.fields['subfamilia'].queryset = SubFamiliaMerchandising.objects.filter(familia = id_familia)
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


class UnidadForm(forms.Form):
    unidad = forms.ModelChoiceField(queryset = Unidad.objects.all(), required=False)

def UnidadView(request, id_subfamilia):
    form = UnidadForm()
    form.fields['unidad'].queryset = SubFamiliaMerchandising.objects.get(id = id_subfamilia).unidad.all()
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

def UnidadMerchandisingView(request, id_merchandising):
    form = UnidadForm()
    form.fields['unidad'].queryset = Merchandising.objects.get(id = id_merchandising).subfamilia.unidad.all()
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


class ModeloMerchandisingForm(forms.Form):
    modelo = forms.ModelChoiceField(queryset = ModeloMerchandising.objects.all(), required=False)

def ModeloMerchandisingView(request, id_marca):
    form = ModeloMerchandisingForm()
    if id_marca != "0":
        form.fields['modelo'].queryset = MarcaMerchandising.objects.get(id = id_marca).modelos.all()
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
    

class ImagenMerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_imagenmerchandising')
    model = ImagenMerchandising
    template_name = "includes/formulario generico.html"
    form_class = ImagenMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        filtro = ImagenMerchandising.objects.filter(
            descripcion = form.instance.descripcion,
            merchandising = merchandising)
        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de imagen ya registrada.')
            return super().form_invalid(form)

        form.instance.merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImagenMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Imagen Merchandising"
        return context

class ImagenMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.delete_imagenmerchandising')
    model = ImagenMerchandising
    template_name = "includes/formulario generico.html"
    form_class = ImagenMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def form_valid(self, form):
        filtro = ImagenMerchandising.objects.filter(
            descripcion = form.instance.descripcion,
            merchandising = self.object.merchandising).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de imagen ya registrada.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImagenMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Imagen"
        return context

class ImagenMerchandisingDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_imagenmerchandising')
    model = ImagenMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( ImagenMerchandisingDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Imagen"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context

class ImagenMerchandisingDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_imagenmerchandising')
    model = ImagenMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ImagenMerchandisingDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Imagen"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context
    

class VideoMerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_videomerchandising')
    model = VideoMerchandising
    template_name = "includes/formulario generico.html"
    form_class = VideoMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        filtro = VideoMerchandising.objects.filter(
            descripcion = form.instance.descripcion,
            merchandising = merchandising)
        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de video ya registrada.')
            return super().form_invalid(form)

        form.instance.merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VideoMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Video Merchandising"
        return context

class VideoMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_videomerchandising')
    model = VideoMerchandising
    template_name = "includes/formulario generico.html"
    form_class = VideoMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def form_valid(self, form):
        filtro = VideoMerchandising.objects.filter(
            descripcion = form.instance.descripcion,
            merchandising = self.object.merchandising).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de video ya registrada.')
            return super().form_invalid(form)
        else:
            pass
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VideoMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Video"
        return context


class VideoMerchandisingDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_videomerchandising')
    model = VideoMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( VideoMerchandisingDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Video"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context

class VideoMerchandisingDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_videomerchandising')
    model = VideoMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(VideoMerchandisingDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Video"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context
    

class ProveedorMerchandisingCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_proveedormerchandising')
    model = ProveedorMerchandising
    template_name = "includes/formulario generico.html"
    form_class = ProveedorMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        content_type = ContentType.objects.get_for_model(merchandising)
        id_registro = self.kwargs['merchandising_id']

        filtro = ProveedorMerchandising.objects.filter(
            proveedor = form.instance.proveedor,
            content_type = content_type,
            id_registro = id_registro)
            
        if len(filtro)>0:
            form.add_error('proveedor', 'Proveedor ya asignado al merchandising.')
            return super().form_invalid(form)

        form.instance.content_type = content_type
        form.instance.id_registro = id_registro
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProveedorMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Proveedor"
        return context

class ProveedorMerchandisingUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_proveedormerchandising')
    model = ProveedorMerchandising
    template_name = "includes/formulario generico.html"
    form_class = ProveedorMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.id_registro})

    def form_valid(self, form):
        filtro = ProveedorMerchandising.objects.filter(
            proveedor = form.instance.proveedor,
            content_type = self.object.content_type,
            id_registro = self.object.id_registro).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('proveedor', 'Proveedor ya asignado al merchandising.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProveedorMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Proveedor Merchandising"
        return context

class ProveedorMerchandisingDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_proveedormerchandising')
    model = ProveedorMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.id_registro})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( ProveedorMerchandisingDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Proveedor Merchandising"
        context['dar_baja'] = "true"
        context['item'] = self.object.proveedor
        return context

class ProveedorMerchandisingDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_proveedormerchandising')
    model = ProveedorMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.id_registro})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProveedorMerchandisingDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Proveedor Merchandising"
        context['dar_baja'] = "true"
        context['item'] = self.object.proveedor
        return context
    

class EquivalenciaUnidadCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('merchandising.add_equivalenciaunidad')
    model = EquivalenciaUnidadMerchandising
    template_name = "includes/formulario generico.html"
    form_class = EquivalenciaUnidadMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def get_form_kwargs(self, *args, **kwargs):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        kwargs = super(EquivalenciaUnidadCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['merchandising'] = merchandising
        return kwargs

    def form_valid(self, form):
        form.instance.merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquivalenciaUnidadCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Equivalencia Unidad"
        return context

class EquivalenciaUnidadUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('merchandising.change_equivalenciaunidad')
    model = EquivalenciaUnidadMerchandising
    template_name = "includes/formulario generico.html"
    form_class = EquivalenciaUnidadMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EquivalenciaUnidadUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['merchandising'] = self.object.merchandising
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquivalenciaUnidadUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Equivalencia Unidad"
        return context

class EquivalenciaUnidadDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_equivalenciaunidad')
    model = EquivalenciaUnidadMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( EquivalenciaUnidadDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Equivalencia Unidad"
        context['dar_baja'] = "true"
        return context

class EquivalenciaUnidadDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('merchandising.delete_equivalenciaunidad')
    model = EquivalenciaUnidadMerchandising
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_alta_baja = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EquivalenciaUnidadDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Equivalencia Unidad"
        context['dar_baja'] = "true"
        return context
    

class IdiomaMerchandisingCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('merchandising.add_idiomamerchandising')
    model = IdiomaMerchandising
    template_name = "includes/formulario generico.html"
    form_class = IdiomaMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

    def form_valid(self, form):
        merchandising = Merchandising.objects.get(id = self.kwargs['merchandising_id'])
        filtro = IdiomaMerchandising.objects.filter(
            idioma = form.instance.idioma,
            merchandising = merchandising)
        if len(filtro)>0:
            form.add_error('idioma', 'Idioma ya registrado.')
            return super().form_invalid(form)

        form.instance.merchandising = merchandising
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IdiomaMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Idioma Merchandising"
        return context

class IdiomaMerchandisingUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('merchandising.add_idiomamerchandising')
    model = IdiomaMerchandising
    template_name = "includes/formulario generico.html"
    form_class = IdiomaMerchandisingForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.object.merchandising.id})

    def form_valid(self, form):
        filtro = IdiomaMerchandising.objects.filter(
            idioma = form.instance.idioma,
            merchandising = self.object.merchandising).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('idioma', 'Idioma ya registrado.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IdiomaMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Idioma Merchandising"
        return context
    

# class PrecioListaMerchandisingCreateView(PermissionRequiredMixin, BSModalCreateView):
#     permission_required = ('cotizacion.add_preciolistamerchandising')
#     model = PrecioListaMerchandising
#     template_name = "merchandising/merchandising/form_precio.html"
#     form_class = PrecioListaMerchandisingForm

#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('merchandising_app:merchandising_detalle', kwargs={'pk':self.kwargs['merchandising_id']})

#     def form_valid(self, form):
#         if form.cleaned_data['comprobante']:
#             comprobante_id, comprobante_content_type_id, merchandising_id, merchandising_content_type_id = form.cleaned_data['comprobante'].split("|")
#         else:
#             comprobante_id, comprobante_content_type_id, merchandising_id, merchandising_content_type_id = [None, None, None, None]
#         form.instance.content_type_producto = ContentType.objects.get(id=self.kwargs['merchandising_content_type'])
#         form.instance.id_registro_producto = self.kwargs['merchandising_id']
#         if comprobante_content_type_id:
#             form.instance.content_type_documento = ContentType.objects.get(id=int(comprobante_content_type_id))
#         else:
#             form.instance.content_type_documento = None
#         if comprobante_id:
#             form.instance.id_registro_documento = int(comprobante_id)
#         else:
#             form.instance.id_registro_documento = comprobante_id
#         registro_guardar(form.instance, self.request)
#         return super().form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         precios = []
#         content_type = self.kwargs['merchandising_content_type']
#         id_registro = self.kwargs['merchandising_id']
#         orden_detalle = OrdenCompraDetalle.objects.filter(
#             content_type = content_type,
#             id_registro = id_registro,
#         )
        
#         for detalle in orden_detalle:
#             try:
#                 detalle.cantidad = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.cantidad
#                 detalle.precio = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.precio_final_con_igv
                
#                 comprobante_compra = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.comprobante_compra
#             except:
#                 continue
            
#             detalle.logistico = comprobante_compra.logistico
            
#             try:
#                 detalle.fecha_recepcion = comprobante_compra.fecha_recepcion
#                 detalle.numero_comprobante_compra = comprobante_compra.numero_comprobante_compra
#                 valor = "%s|%s|%s|%s" % (comprobante_compra.id, ContentType.objects.get_for_model(comprobante_compra).id, self.kwargs['merchandising_id'], self.kwargs['merchandising_content_type'])
#                 precios.append((valor, comprobante_compra.numero_comprobante_compra))
#             except:
#                 pass
#         self.kwargs['precios'] = orden_detalle
#         kwargs['precios'] = precios
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context = super(PrecioListaMerchandisingCreateView, self).get_context_data(**kwargs)
#         context['accion']="Registrar"
#         context['titulo']="Precio"
#         context['precios'] = self.kwargs['precios']
#         return context


def ComprobanteView(request, id_comprobante, comprobante_content_type, id_merchandising, merchandising_content_type):
    comprobante_content_type = ContentType.objects.get(id=comprobante_content_type)
    comprobante_compra = comprobante_content_type.get_object_for_this_type(id = id_comprobante)

    merchandising_content_type = ContentType.objects.get(id=merchandising_content_type)
    merchandising = merchandising_content_type.get_object_for_this_type(id = id_merchandising)    

    orden_detalle = OrdenCompraDetalle.objects.filter(
        content_type = merchandising_content_type,
        id_registro = id_merchandising,
    )

    precio = Decimal('0.00')
    moneda = None
    logistico = Decimal('0.00')
    
    for detalle in orden_detalle:
        try:
            comprobante_compra = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.comprobante_compra
            if comprobante_compra.id == id_comprobante and ContentType.objects.get_for_model(comprobante_compra) == comprobante_content_type:
                if detalle.id_registro == id_merchandising and detalle.content_type == merchandising_content_type:
                    precio = detalle.ComprobanteCompraPIDetalle_orden_compra_detalle.precio_final_con_igv
                    moneda = comprobante_compra.moneda
                    logistico = comprobante_compra.logistico
        except:
            continue

    
    return HttpResponse("%s|%s|%s" % (precio, moneda, logistico))
    # return HttpResponse("%s|%s" % (moneda, logistico))


def StockView(request, id_merchandising):
    if request.method == 'GET':
        try:
            return HttpResponse(Merchandising.objects.get(id=id_merchandising).stock)
        except:
            return HttpResponse("")


def StockSociedadView(request, id_merchandising, id_sociedad):
    if request.method == 'GET':
        try:
            return HttpResponse(stock(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad))
        except:
            return HttpResponse("")


def StockSociedadAlmacenView(request, id_merchandising, id_sociedad, id_almacen):
    if request.method == 'GET':
        try:
            return HttpResponse(stock(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad, id_almacen))
        except:
            return HttpResponse("")


def StockSedeView(request, id_merchandising, id_sociedad, id_sede):
    if request.method == 'GET':
        try:
            return HttpResponse(stock_sede(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad, id_sede))
        except:
            return HttpResponse("")


def StockSedeTipoStockView(request, id_merchandising, id_sociedad, id_sede, id_tipo_stock):
    if request.method == 'GET':
        try:
            return HttpResponse(stock_sede_tipo_stock(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad, id_sede, id_tipo_stock))
        except:
            return HttpResponse("")


def StockDisponibleView(request, id_merchandising):
    if request.method == 'GET':
        try:
            return HttpResponse(Merchandising.objects.get(id=id_merchandising).vendible)
        except:
            return HttpResponse("")


def StockDisponibleSociedadView(request, id_merchandising, id_sociedad):
    if request.method == 'GET':
        try:
            return HttpResponse(stock_disponible(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad))
        except:
            return HttpResponse("")


def StockDisponibleSociedadAlmacenView(request, id_merchandising, id_sociedad, id_almacen):
    if request.method == 'GET':
        try:
            return HttpResponse(stock_disponible(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad, id_almacen))
        except:
            return HttpResponse("")


def StockSedeDisponibleView(request, id_merchandising, id_sociedad, id_sede):
    if request.method == 'GET':
        try:
            return HttpResponse(stock_sede_disponible(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad, id_sede))
        except:
            return HttpResponse("")


def StockTipoStockView(request, id_merchandising, id_sociedad, id_almacen, id_tipo_stock):
    if request.method == 'GET':
        try:
            return HttpResponse(stock_tipo_stock(ContentType.objects.get_for_model(Merchandising), id_merchandising, id_sociedad, id_almacen, id_tipo_stock))
        except:
            return HttpResponse("")


def MerchandisingView(request, id_merchandising):
    if request.method == 'GET':
        try:
            merchandising = Merchandising.objects.get(id=id_merchandising)
            return HttpResponse(obtener_atributos(merchandising))
        except Exception as e:
            return HttpResponse("")


def ProveedorMerchandisingView(request, id_merchandising):
    if request.method == 'GET':
        try:
            merchandising = ProveedorMerchandising.objects.get(id=id_merchandising)
            atributos = json.loads(obtener_atributos(merchandising))
            atributos['producto-info'] = json.loads(obtener_atributos(merchandising.producto))
            return HttpResponse(json.dumps(atributos))
        except Exception as e:
            return HttpResponse("")

######################################################---INVENTARIO MERCHANDISING---######################################################

class InventarioMerchandisingListView(PermissionRequiredMixin, ListView):
    permission_required = ('merchandising.view_inventariomerchandising')
    model = InventarioMerchandising
    template_name = "merchandising/inventario_merchandising/inicio.html"
    context_object_name = 'contexto_inventario_merchandising'

def InventarioMerchandisingTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/inventario_merchandising/inicio_tabla.html'
        context = {}
        context['contexto_inventario_merchandising'] = InventarioMerchandising.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class InventarioMerchandisingCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('merchandising.view_inventariomerchandising')
    model = InventarioMerchandising
    template_name = "includes/formulario generico.html"
    form_class = InventarioMerchandisingForm
    success_url = reverse_lazy('merchandising_app:inventario_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InventarioMerchandisingCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Inventario Merchandising"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


class InventarioMerchandisingUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('merchandising.change_inventariomerchandising')
    model = InventarioMerchandising
    template_name = "includes/formulario generico.html"
    form_class = InventarioMerchandisingUpdateForm
    success_url = reverse_lazy('merchandising_app:inventario_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InventarioMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Inventario"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)


class InventarioMerchandisingConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('merchandising.change_inventariomerchandising')
    model = InventarioMerchandising
    template_name = "merchandising/inventario_merchandising/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('merchandising_app:ajuste_inventario_merchandising_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.request.session['primero'] = True
            self.object = self.get_object()
            detalles = self.object.InventarioMerchandisingDetalle_inventario_merchandising.all()

            ajuste_inventario_merchandising = AjusteInventarioMerchandising.objects.create(
                sociedad=self.object.sociedad,
                sede=self.object.sede,
                observacion='',
                estado='1',
                inventario_merchandising=self.object,
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            for detalle in detalles:
                ajuste_inventario_merchandising_detalle = AjusteInventarioMerchandisingDetalle.objects.create(
                    item=detalle.item,
                    merchandising=detalle.merchandising,
                    almacen=detalle.almacen,
                    tipo_stock=detalle.tipo_stock,
                    cantidad_stock=stock_tipo_stock(
                        content_type=detalle.merchandising.content_type,
                        id_registro=detalle.merchandising.id,
                        id_sociedad=self.object.sociedad.id,
                        id_almacen=detalle.almacen.id,
                        id_tipo_stock=detalle.tipo_stock.id),
                    cantidad_contada=detalle.cantidad,
                    ajuste_inventario_merchandising=ajuste_inventario_merchandising,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            self.kwargs['ajuste_inventario_merchandising'] = ajuste_inventario_merchandising
            self.request.session['primero'] = False
            registro_guardar(self.object, self.request)
            self.object.estado = 2
            self.object.save()
            messages.success(request, MENSAJE_GENERAR_DOCUMENTO_AJUSTE_INVENTARIO_MERCHANDISING)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(InventarioMerchandisingConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Inventario Merchandising"
        context['dar_baja'] = "true"
        return context


class InventarioMerchandisingDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('merchandising.view_inventariomerchandising')

    model = InventarioMerchandising
    template_name = "merchandising/inventario_merchandising/detalle.html"
    context_object_name = 'contexto_inventario_merchandising_detalle'

    def get_context_data(self, **kwargs):
        inventario_merchandising = InventarioMerchandising.objects.get(id = self.kwargs['pk'])
        context = super(InventarioMerchandisingDetailView, self).get_context_data(**kwargs)
        context['inventario_merchandising_detalle'] = InventarioMerchandisingDetalle.objects.filter(inventario_merchandising = inventario_merchandising)
        return context


def InventarioMerchandisingDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/inventario_merchandising/detalle_tabla.html'
        context = {}
        inventario_merchandising = InventarioMerchandising.objects.get(id = pk)
        context['contexto_inventario_merchandising_detalle'] = inventario_merchandising
        context['inventario_merchandising_detalle'] = InventarioMerchandisingDetalle.objects.filter(inventario_merchandising = inventario_merchandising)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class InventarioMerchandisingDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('merchandising.view_inventariomerchandisingdetalle')
    template_name = "merchandising/inventario_merchandising/form_merchandising.html"
    form_class = InventarioMerchandisingDetalleForm
    success_url = reverse_lazy('merchandising_app:inventario_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        registro = InventarioMerchandising.objects.get(id = self.kwargs['inventario_merchandising_id'])
        sede = registro.sede.id
        almacenes = Almacen.objects.filter(sede__id = sede)

        kwargs = super().get_form_kwargs()
        kwargs['almacenes'] = almacenes
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                inventario_merchandising = InventarioMerchandising.objects.get(id=self.kwargs['inventario_merchandising_id'])
                item = len(InventarioMerchandisingDetalle.objects.filter(inventario_merchandising = inventario_merchandising))

                merchandising = form.cleaned_data.get('merchandising')
                almacen = form.cleaned_data.get('almacen')
                tipo_stock = form.cleaned_data.get('tipo_stock')
                cantidad = form.cleaned_data.get('cantidad')

                obj, created = InventarioMerchandisingDetalle.objects.get_or_create(
                    merchandising = merchandising,
                    almacen = almacen,
                    tipo_stock = tipo_stock,
                    inventario_merchandising = inventario_merchandising,
                )
                
                if created:
                    obj.item = item + 1
                    obj.cantidad = cantidad

                else:
                    obj.cantidad = obj.cantidad + cantidad

                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(InventarioMerchandisingDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Merchandising"
        return context


class InventarioMerchandisingDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('merchandising.change_inventariomerchandisingdetalle')
    model = InventarioMerchandisingDetalle
    template_name = "merchandising/inventario_merchandising/form_merchandising.html"
    form_class = InventarioMerchandisingDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:inventario_merchandising_detalle', kwargs={'pk':self.get_object().inventario_merchandising_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        registro = InventarioMerchandising.objects.get(id = self.get_object().inventario_merchandising_id)
        sede = registro.sede.id
        almacenes = Almacen.objects.filter(sede__id = sede)

        kwargs = super().get_form_kwargs()
        kwargs['almacenes'] = almacenes
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(InventarioMerchandisingDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Merchandising"
        return context


class InventarioMerchandisingDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('merchandising.delete_inventariomerchandisingdetalle')
    model = InventarioMerchandisingDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:inventario_merchandising_detalle', kwargs={'pk': self.get_object().inventario_merchandising_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            merchandising = InventarioMerchandisingDetalle.objects.filter(inventario_merchandising=self.get_object().inventario_merchandising)
            contador = 1
            for merchandising in merchandising:
                if merchandising == self.get_object(): continue
                merchandising.item = contador
                merchandising.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(InventarioMerchandisingDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Merchandising"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class AjusteInventarioMerchandisingListView(PermissionRequiredMixin, ListView):
    permission_required = ('merchandising.view_ajusteinventariomerchandising')
    model = AjusteInventarioMerchandising
    template_name = "merchandising/ajuste_inventario_merchandising/inicio.html"
    context_object_name = 'contexto_ajuste_inventario_merchandising'

def AjusteInventarioMerchandisingTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/ajuste_inventario_merchandising/inicio_tabla.html'
        context = {}
        context['contexto_ajuste_inventario_merchandising'] = AjusteInventarioMerchandising.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AjusteInventarioMerchandisingUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('merchandising.change_ajusteinventariomerchandising')
    model = AjusteInventarioMerchandising
    template_name = "includes/formulario generico.html"
    form_class = AjusteInventarioMerchandisingForm
    success_url = reverse_lazy('merchandising_app:ajuste_inventario_merchandising_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AjusteInventarioMerchandisingUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Ajuste Inventario"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)


class AjusteInventarioMerchandisingConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('merchandising.change_ajusteinventariomerchandising')
    model = AjusteInventarioMerchandising
    template_name = "merchandising/ajuste_inventario_merchandising/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('merchandising_app:ajuste_inventario_merchandising_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.request.session['primero'] = True
            self.object = self.get_object()
            self.request.session['primero'] = False
            registro_guardar(self.object, self.request)
         
            tipo_stock_disponible = TipoStock.objects.get(codigo=3) # Disponible

            for detalle in self.object.AjusteInventarioMerchandisingDetalle_ajuste_inventario_merchandising.all():
                cantidad = detalle.cantidad_stock - detalle.cantidad_contada
                if cantidad > 0:
                    # AJUSTE POR INVENTARIO DISMINUIR STOCK
                    if detalle.merchandising.control_serie and tipo_stock_disponible == detalle.tipo_stock:
                        movimiento_final = TipoMovimiento.objects.get(codigo=154) # Correcion por Inventario, disminuir stock, c/Serie
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=153) # Correcion por Inventario, disminuir stock, s/Serie
                    tipo_stock_inicial = detalle.tipo_stock
                    tipo_stock_final = movimiento_final.tipo_stock_final
                else:
                    # AJUSTE POR INVENTARIO AUMENTAR STOCK
                    if detalle.merchandising.control_serie and tipo_stock_disponible == detalle.tipo_stock:
                        movimiento_final = TipoMovimiento.objects.get(codigo=157) # Correccion Inventario con Series, aumentar stock
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=156) #	Correcion por Inventario, aumentar stock, s/Serie
                    tipo_stock_inicial = movimiento_final.tipo_stock_final
                    tipo_stock_final = detalle.tipo_stock

                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.merchandising.content_type,
                    id_registro_producto = detalle.merchandising.id,
                    cantidad = cantidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = detalle.ajuste_inventario_merchandising.content_type,
                    id_registro_documento_proceso = detalle.ajuste_inventario_merchandising.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.ajuste_inventario_merchandising.sociedad,
                    movimiento_anterior = None,
                    created_by = request.user,
                    updated_by = request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.merchandising.content_type,
                    id_registro_producto = detalle.merchandising.id,
                    cantidad = cantidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = detalle.ajuste_inventario_merchandising.content_type,
                    id_registro_documento_proceso = detalle.ajuste_inventario_merchandising.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.ajuste_inventario_merchandising.sociedad,
                    movimiento_anterior = movimiento_uno,
                    created_by = request.user,
                    updated_by = request.user,
                )            

            self.object.estado = 2  # Concluir
            self.object.save()
            messages.success(request, MENSAJE_AJUSTE_INVENTARIO_MERCHANDISING)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(AjusteInventarioMerchandisingConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Ajuste Inventario Merchandising"
        context['dar_baja'] = "true"
        return context


class AjusteInventarioMerchandisingDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('merchandising.view_ajusteinventariomerchandising')

    model = AjusteInventarioMerchandising
    template_name = "merchandising/ajuste_inventario_merchandising/detalle.html"
    context_object_name = 'contexto_ajuste_inventario_merchandising_detalle'

    def get_context_data(self, **kwargs):
        ajuste_inventario_merchandising = AjusteInventarioMerchandising.objects.get(id = self.kwargs['pk'])
        context = super(AjusteInventarioMerchandisingDetailView, self).get_context_data(**kwargs)
        context['ajuste_inventario_merchandising_detalle'] = AjusteInventarioMerchandisingDetalle.objects.filter(ajuste_inventario_merchandising = ajuste_inventario_merchandising)
        return context


def AjusteInventarioMerchandisingDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'merchandising/ajuste_inventario_merchandising/detalle_tabla.html'
        context = {}
        ajuste_inventario_merchandising = AjusteInventarioMerchandising.objects.get(id = pk)
        context['contexto_ajuste_inventario_merchandising_detalle'] = ajuste_inventario_merchandising
        context['ajuste_inventario_merchandising_detalle'] = AjusteInventarioMerchandisingDetalle.objects.filter(ajuste_inventario_merchandising = ajuste_inventario_merchandising)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AjusteInventarioMerchandisingDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('merchandising.add_ajusteinventariomerchandisingdetalle')
    template_name = "includes/formulario generico.html"
    form_class = AjusteInventarioMerchandisingDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:ajuste_inventario_merchandising_detalle', kwargs={'pk': self.kwargs['ajuste_inventario_merchandising_id']})

    def get_form_kwargs(self):
        ajuste_inventario_merchandising = AjusteInventarioMerchandising.objects.get(id=self.kwargs['ajuste_inventario_merchandising_id'])
        inventario_merchandising = ajuste_inventario_merchandising.inventario_merchandising.id
        merchandising = ajuste_inventario_merchandising.AjusteInventarioMerchandisingDetalle_ajuste_inventario_merchandising.all()
        lista_merchandising = InventarioMerchandisingDetalle.objects.filter(inventario_merchandising__id=inventario_merchandising)
        for merchandising in merchandising:
            lista_merchandising = lista_merchandising.exclude(merchandising_id=merchandising.merchandising.id)
        kwargs = super().get_form_kwargs()
        kwargs['merchandising'] = lista_merchandising
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                ajuste_inventario_merchandising = AjusteInventarioMerchandising.objects.get(id=self.kwargs['ajuste_inventario_merchandising_id'])
                item = len(ajuste_inventario_merchandising.AjusteInventarioMerchandisingDetalle_ajuste_inventario_merchandising.all())
                merchandising = form.cleaned_data.get('producto')
                sociedad = ajuste_inventario_merchandising.sociedad

                ajuste_inventario_merchandising_detalle = AjusteInventarioMerchandisingDetalle.objects.create(
                    ajuste_inventario_merchandising=ajuste_inventario_merchandising,
                    merchandising = merchandising.merchandising,
                    almacen = ajuste_inventario_merchandising.inventario_merchandising.InventarioMerchandisingDetalle_inventario_merchandising.get(merchandising=merchandising.merchandising).almacen,
                    tipo_stock = ajuste_inventario_merchandising.inventario_merchandising.InventarioMerchandisingDetalle_inventario_merchandising.get(merchandising=merchandising.merchandising).tipo_stock,
                    cantidad_stock = stock_tipo_stock(
                        merchandising.merchandising.content_type, 
                        merchandising.merchandising.id, 
                        sociedad.id,
                        ajuste_inventario_merchandising.inventario_merchandising.InventarioMerchandisingDetalle_inventario_merchandising.get(merchandising=merchandising.merchandising).almacen.id, 
                        ajuste_inventario_merchandising.inventario_merchandising.InventarioMerchandisingDetalle_inventario_merchandising.get(merchandising=merchandising.merchandising).tipo_stock.id),
                    cantidad_contada = ajuste_inventario_merchandising.inventario_merchandising.InventarioMerchandisingDetalle_inventario_merchandising.get(merchandising=merchandising.merchandising).cantidad,
                    item=item + 1,
                    created_by=self.request.user,
                    updated_by=self.request.user, 
                )

                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(AjusteInventarioMerchandisingDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Merchandising"
        return context


class AjusteInventarioMerchandisingDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('merchandising.delete_ajusteinventariomerchandisingdetalle')
    model = AjusteInventarioMerchandisingDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('merchandising_app:ajuste_inventario_merchandising_detalle', kwargs={'pk': self.get_object().ajuste_inventario_merchandising_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            merchandising = AjusteInventarioMerchandisingDetalle.objects.filter(ajuste_inventario_merchandising=self.get_object().ajuste_inventario_merchandising)
            contador = 1
            for merchandising in merchandising:
                if merchandising == self.get_object(): continue
                merchandising.item = contador
                merchandising.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AjusteInventarioMerchandisingDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Merchandising"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context