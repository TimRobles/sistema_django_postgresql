from django.shortcuts import render
from applications.importaciones import *
from applications.oferta_proveedor.models import ArchivoOfertaProveedor, OfertaProveedor, OfertaProveedorDetalle
from applications.oferta_proveedor.forms import ArchivoOfertaProveedorForm, OfertaProveedorDetalleUpdateForm, OfertaProveedorForm
from applications.funciones import obtener_totales
from applications.funciones import slug_aleatorio

class OfertaProveedorListView(PermissionRequiredMixin, ListView):
    permission_required = ('oferta_proveedor.view_ofertaproveedor')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/inicio.html"
    context_object_name = 'contexto_oferta_proveedor'

def OfertaProveedorTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/inicio_tabla.html'
        context = {}
        context['contexto_oferta_proveedor'] = OfertaProveedor.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class OfertaProveedorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedor')
    model = OfertaProveedor
    template_name = "includes/formulario generico.html"
    form_class = OfertaProveedorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')

    def form_valid(self, form):
        totales = obtener_totales(OfertaProveedor.objects.get(id=form.instance.id))
        form.instance.estado = 2
        form.instance.descuento_global = totales['descuento_global']
        form.instance.total_descuento = totales['total_descuento']
        form.instance.total_anticipo = totales['total_anticipo']
        form.instance.total_gravada = totales['total_gravada']
        form.instance.total_inafecta = totales['total_inafecta']
        form.instance.total_exonerada = totales['total_exonerada']
        form.instance.total_igv = totales['total_igv']
        form.instance.total_gratuita = totales['total_gratuita']
        form.instance.total_otros_cargos = totales['total_otros_cargos']
        form.instance.total_icbper = totales['total_icbper']
        form.instance.total = totales['total']
        form.instance.slug = slug_aleatorio(OfertaProveedor)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Finalizar"
        context['titulo']="Oferta Proveedor"
        return context

class OfertaProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('oferta_proveedor.view_OfertaProveedordetalle')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/detalle.html"
    context_object_name = 'contexto_oferta_proveedor'

    def get_context_data(self, **kwargs):
        oferta_proveedor = OfertaProveedor.objects.get(id = self.kwargs['pk'])
        context = super(OfertaProveedorDetailView, self).get_context_data(**kwargs)
        context['materiales'] = OfertaProveedorDetalle.objects.ver_detalle(oferta_proveedor)
        context['archivos'] = ArchivoOfertaProveedor.objects.filter(oferta_proveedor = oferta_proveedor)
        context['totales'] = obtener_totales(OfertaProveedor.objects.get(id=self.kwargs['pk']))
        return context

def OfertaProveedorDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/detalle_tabla.html'
        context = {}
        oferta_proveedor = OfertaProveedor.objects.get(id = pk)
        context['contexto_oferta_proveedor'] = oferta_proveedor
        context['materiales'] = OfertaProveedorDetalle.objects.ver_detalle(oferta_proveedor)
        context['archivos'] = ArchivoOfertaProveedor.objects.filter(oferta_proveedor = oferta_proveedor)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class OfertaProveedorDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedordetalle')

    model = OfertaProveedorDetalle
    template_name = "oferta_proveedor/oferta_proveedor/actualizar.html"
    form_class = OfertaProveedorDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'pk':self.get_object().oferta_proveedor.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = self.object.proveedor_material
        return context




# class MaterialOfertaProveedorDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
#     permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedordetalle')
#     template_name = "requerimiento_material/lista_requerimiento_material/form_material.html"
#     form_class = RequerimientoMaterialProveedorDetalleForm
#     success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

#     def form_valid(self, form):
#         if self.request.session['primero']:
#             registro = RequerimientoMaterialProveedor.objects.get(id = self.kwargs['requerimiento_id'])
#             item = len(registro.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all())
#             material = form.cleaned_data.get('material')
#             cantidad = form.cleaned_data.get('cantidad')
#             # comentario = form.cleaned_data.get('comentario')
#             print('////////////////////////////////////////////')
#             print(registro)
#             print(item)
#             print(material)
#             print(material.id)
#             print('////////////////////////////////////////////')

#             obj, created = RequerimientoMaterialProveedorDetalle.objects.get_or_create(
#                 # content_type = ContentType.objects.get_for_model(material),
#                 id_registro = material.id,
#                 lista_requerimiento_material = registro,
#             )
#             if created:
#                 obj.item = item + 1
#                 obj.cantidad = cantidad
#                 # obj.comentario = comentario
#             else:
#                 obj.cantidad = obj.cantidad + cantidad
#                 # if obj.comentario[-len(' | ' + comentario):] != ' | ' + comentario:
#                 #     obj.comentario = obj.comentario + ' | ' + comentario


#             registro_guardar(obj, self.request)
#             obj.save()
#             self.request.session['primero'] = False
#         return super().form_valid(form)
        

#     def get_form_kwargs(self):
#         registro = RequerimientoMaterialProveedor.objects.get(id = self.kwargs['requerimiento_id'])
#         materiales = registro.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all()
#         kwargs = super().get_form_kwargs()
#         kwargs['materiales'] = materiales
#         return kwargs

#     def get_context_data(self, **kwargs):
#         self.request.session['primero'] = True
#         context = super(RequerimientoMaterialProveedorDetalleCreateView, self).get_context_data(**kwargs)
#         context['accion'] = 'Agregar'
#         context['titulo'] = 'Material '
#         return context




class ArchivoOfertaProveedorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('oferta_proveedor.add_ofertaproveedordetalle')
    model = ArchivoOfertaProveedor
    template_name = "includes/formulario generico.html"
    form_class = ArchivoOfertaProveedorForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'pk':self.kwargs['oferta_proveedor_id']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.oferta_proveedor = OfertaProveedor.objects.get(id = self.kwargs['oferta_proveedor_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoOfertaProveedorCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar"
        context['titulo']="Documento"
        return context

class ArchivoOfertaProveedorDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('oferta_proveedor.delete_documento')
    model =ArchivoOfertaProveedor
    template_name = "includes/eliminar generico.html" 

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'pk':self.object.oferta_proveedor_id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoOfertaProveedorDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Documento"
        return context


