from django.shortcuts import render
from applications.importaciones import *
from applications.oferta_proveedor.models import ArchivoOfertaProveedor, OfertaProveedor, OfertaProveedorDetalle
from applications.oferta_proveedor.forms import AgregarMaterialOfertaProveedorForm, ArchivoOfertaProveedorForm, CrearMaterialOfertaProveedorForm, OfertaProveedorDetalleUpdateForm, OfertaProveedorForm
from applications.funciones import obtener_totales
from applications.funciones import slug_aleatorio
from applications.requerimiento_de_materiales.models import ListaRequerimientoMaterialDetalle, RequerimientoMaterialProveedor, RequerimientoMaterialProveedorDetalle
from applications.material.models import ProveedorMaterial

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

class OfertaProveedorFinalizarView(PermissionRequiredMixin, BSModalUpdateView):
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
        context = super(OfertaProveedorFinalizarView, self).get_context_data(**kwargs)
        context['accion']="Finalizar"
        context['titulo']="Oferta Proveedor"
        return context

class OfertaProveedorRechazarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('oferta_proveedor.delete_ofertaproveedor')
    model = OfertaProveedor
    template_name = "includes/eliminar generico.html"

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.has_permission():
    #         return render(request, 'includes/modal sin permiso.html')
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_RECHAZAR_OFERTA_PROVEEDOR)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorRechazarView, self).get_context_data(**kwargs)
        context['accion'] = "Rechazar"
        context['titulo'] = "Oferta Proveedor"
        context['dar_baja'] = "true"
        context['item'] = self.object.requerimiento_material
        return context

class OfertaProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('oferta_proveedor.view_archivoofertaproveedor')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/detalle.html"
    context_object_name = 'contexto_oferta_proveedor'

    def get_context_data(self, **kwargs):
        oferta_proveedor = OfertaProveedor.objects.get(slug = self.kwargs['slug'])
        context = super(OfertaProveedorDetailView, self).get_context_data(**kwargs)
        context['materiales'] = OfertaProveedorDetalle.objects.ver_detalle(oferta_proveedor)
        context['archivos'] = ArchivoOfertaProveedor.objects.filter(oferta_proveedor = oferta_proveedor)
        context['totales'] = obtener_totales(OfertaProveedor.objects.get(slug=self.kwargs['slug']))
        return context

def OfertaProveedorDetailTabla(request, slug):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/detalle_tabla.html'
        context = {}
        oferta_proveedor = OfertaProveedor.objects.get(slug = slug)
        context['contexto_oferta_proveedor'] = oferta_proveedor
        context['materiales'] = OfertaProveedorDetalle.objects.ver_detalle(oferta_proveedor)
        context['archivos'] = ArchivoOfertaProveedor.objects.filter(oferta_proveedor = oferta_proveedor)
        context['totales'] = obtener_totales(OfertaProveedor.objects.get(slug=slug))

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
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'slug':self.get_object().oferta_proveedor.slug})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Precios"
        context['material'] = self.object.proveedor_material
        return context

class OfertaProveedorDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('oferta_proveedor.delete_ofertaproveedordetalle')
    model = OfertaProveedorDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'slug':self.get_object().oferta_proveedor.slug})

    def delete(self, request, *args, **kwargs):
        materiales = OfertaProveedorDetalle.objects.filter(oferta_proveedor=self.get_object().oferta_proveedor)
        contador = 1
        for material in materiales:
            if material == self.get_object():continue
            material.item = contador
            material.save()
            contador += 1

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material."
        context['item'] = self.get_object().item
        context['dar_baja'] = "true"
        return context

class MaterialOfertaProveedorAgregarView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('oferta_proveedor.add_Materialofertaproveedor')
    template_name = "oferta_proveedor/oferta_proveedor/form_material.html"
    form_class = AgregarMaterialOfertaProveedorForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'slug':self.kwargs['oferta_proveedor_slug']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = OfertaProveedor.objects.get(slug = self.kwargs['oferta_proveedor_slug'])
            item = len(registro.OfertaProveedorDetalle_oferta_proveedor.all())
            material = form.cleaned_data.get('material')
            cantidad = form.cleaned_data.get('cantidad')

            obj, created = OfertaProveedorDetalle.objects.get_or_create(
                proveedor_material = material,
                oferta_proveedor = registro,
            )
            if created:
                obj.item = item + 1
                obj.cantidad = cantidad

            else:
                obj.cantidad = obj.cantidad + cantidad

            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        registro = OfertaProveedor.objects.get(slug = self.kwargs['oferta_proveedor_slug'])
        proveedor = registro.requerimiento_material.proveedor.id
        materiales = ProveedorMaterial.objects.filter(proveedor__id = proveedor)

        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = materiales
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(MaterialOfertaProveedorAgregarView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Material '
        return context

class MaterialOfertaProveedorCrearView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('oferta_proveedor.add_Materialofertaproveedor')
    template_name = "includes/formulario generico.html"
    form_class = CrearMaterialOfertaProveedorForm
    
    def get_success_url(self, **kwargs):
            return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'slug':self.kwargs['oferta_proveedor_slug']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = OfertaProveedor.objects.get(slug = self.kwargs['oferta_proveedor_slug'])
            proveedor = registro.requerimiento_material.proveedor
            item = len(registro.OfertaProveedorDetalle_oferta_proveedor.all())
            name = form.cleaned_data.get('name')
            brand = form.cleaned_data.get('brand')
            description = form.cleaned_data.get('description')
            
            proveedor_material, created = ProveedorMaterial.objects.get_or_create(
                proveedor = proveedor,
                name = name.upper(),
                brand = brand.upper(),
                description = description.upper(),
            )
            if created:
                proveedor_material.created_by = self.request.user
                proveedor_material.updated_by = self.request.user
                proveedor_material.save()

            oferta_proveedor_detalle, created = OfertaProveedorDetalle.objects.get_or_create(
                proveedor_material = proveedor_material,
                oferta_proveedor = registro,
            )
            if created:
                oferta_proveedor_detalle.item = item + 1
                oferta_proveedor_detalle.created_by = self.request.user
                oferta_proveedor_detalle.updated_by = self.request.user
                oferta_proveedor_detalle.save()

            self.request.session['primero'] = False
        return super().form_valid(form)

    # def get_form_kwargs(self):
        # registro = OfertaProveedorDetalle.objects.get(slug = self.kwargs['oferta_proveedor_slug'])
        # materiales = registro.proveedor_material.all()


        # # print('****************************')
        # # print(oferta_proveedor)
        # # print('****************************')
        # # materiales = OfertaProveedorDetalle.objects.ver_detalle(oferta_proveedor)
        # print('****************************')
        # print(materiales)
        # print('****************************')
        # kwargs = super().get_form_kwargs()
        # kwargs['materiales'] = materiales
        # return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(MaterialOfertaProveedorCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Crear'
        context['titulo'] = 'Material '
        return context

class ArchivoOfertaProveedorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('oferta_proveedor.add_archivoofertaproveedor')
    model = ArchivoOfertaProveedor
    template_name = "includes/formulario generico.html"
    form_class = ArchivoOfertaProveedorForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'slug':self.kwargs['oferta_proveedor_slug']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.oferta_proveedor = OfertaProveedor.objects.get(slug = self.kwargs['oferta_proveedor_slug'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoOfertaProveedorCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar"
        context['titulo']="Documento"
        return context

class ArchivoOfertaProveedorDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('oferta_proveedor.delete_archivoofertaproveedor')
    model =ArchivoOfertaProveedor
    template_name = "includes/eliminar generico.html" 

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'slug':self.object.oferta_proveedor.slug})

    def get_context_data(self, **kwargs):
        context = super(ArchivoOfertaProveedorDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Documento"
        return context

class OfertaProveedorGenerarNuevoRequerimientoView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('requerimiento_de_materiales.change_ofertaproveedordetalle')

    model = OfertaProveedor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.session['primero']:
            self.object = self.get_object()
            oferta = self.get_object()
            requerimiento = RequerimientoMaterialProveedor.objects.create(
                titulo = oferta.requerimiento_material.titulo,
                proveedor = oferta.requerimiento_material.proveedor,
                interlocutor_proveedor = oferta.requerimiento_material.interlocutor_proveedor,
                lista_requerimiento = oferta.requerimiento_material.lista_requerimiento,
                requerimiento_material_anterior = oferta.requerimiento_material.requerimiento_material_anterior,
                comentario = oferta.requerimiento_material.comentario,
                version = oferta.requerimiento_material.version + 1,
                slug = slug_aleatorio(RequerimientoMaterialProveedor),
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            oferta_detalle = oferta.OfertaProveedorDetalle_oferta_proveedor.all()
            for detalle in oferta_detalle:

                id_lista_requerimiento, created = ListaRequerimientoMaterialDetalle.objects.get_or_create(
                    content_type = detalle.proveedor_material.content_type,
                    id_registro = detalle.proveedor_material.id_registro,
                    lista_requerimiento_material = oferta.requerimiento_material.lista_requerimiento,
                )
                if created:
                    id_lista_requerimiento.item = len(detalle.requerimiento_material.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all())
                registro_guardar(id_lista_requerimiento, self.request)
                id_lista_requerimiento.save()
                
                oferta_detalle = RequerimientoMaterialProveedorDetalle.objects.create(
                    
                    item = detalle.item,
                    id_requerimiento_material_detalle = id_lista_requerimiento,
                    cantidad = detalle.cantidad,
                    requerimiento_material = requerimiento,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                    )
            self.request.session['primero'] = False
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_GENERAR_REQUERIMIENTO_PROVEEDOR)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(OfertaProveedorGenerarNuevoRequerimientoView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Requerimiento Proveedor"
        context['dar_baja'] = "true"
        return context

# ProveedorMaterial.objects.filter(proveedor__id = proveedor_id)

# ProveedorMaterial.objects.create(
#     content_type=
# )