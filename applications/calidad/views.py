from urllib import request
from django.shortcuts import render
from applications.importaciones import*
from applications.material.models import SubFamilia
from applications.calidad.forms import( 
    FallaMaterialForm, 
    NotaControlCalidadStockAnularForm, 
    NotaControlCalidadStockDetalleAgregarForm, 
    NotaControlCalidadStockDetalleUpdateForm, 
    NotaControlCalidadStockForm,
    SerieActualizarBuenoForm,
    SerieActualizarMaloForm,
    # SerieActualizarBuenoForm,
    SerieAgregarBuenoForm,
    SerieAgregarMaloForm,
)
from applications.nota_ingreso.models import NotaIngresoDetalle
from .models import(
    EstadoSerie,
    NotaControlCalidadStock,
    NotaControlCalidadStockDetalle,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
)
from applications.funciones import numeroXn

class FallaMaterialTemplateView(TemplateView):
    template_name = "calidad/falla_material/inicio.html"

    def get_context_data(self, **kwargs):
        sub_familias = SubFamilia.objects.all
        context = super(FallaMaterialTemplateView, self).get_context_data(**kwargs)
        context['contexto_subfamilias'] = sub_familias

        return context

class FallaMaterialDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_fallamaterial')
    model = SubFamilia
    template_name = "calidad/falla_material/detalle.html"
    context_object_name = 'contexto_subfamilia'

    def get_context_data(self, **kwargs):
        sub_familia = SubFamilia.objects.get(id=self.kwargs['pk'])
        context = super(FallaMaterialDetailView, self).get_context_data(**kwargs)
        context['fallas'] = FallaMaterial.objects.filter(sub_familia = sub_familia)
        return context

def FallaMaterialDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/falla_material/detalle_tabla.html'
        context = {}
        sub_familia = SubFamilia.objects.get(id = pk)
        context['contexto_subfamilia'] = sub_familia
        context['fallas'] = FallaMaterial.objects.filter(sub_familia = sub_familia)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class FallaMaterialCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_fallamaterial')
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle', kwargs={'pk':self.kwargs['subfamilia_id']})
    
    def form_valid(self, form):
        form.instance.sub_familia = SubFamilia.objects.get(id = self.kwargs['subfamilia_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Falla"
        return context

class FallaMaterialUpdateView(BSModalUpdateView):
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle_tabla', kwargs={'pk':self.object.sub_familia.id})

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Falla"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class FallaMaterialDeleteView(BSModalDeleteView):
    model = FallaMaterial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:falla_material')

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle', kwargs={'pk':self.object.sub_familia.id})

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Falla"
        context['item'] = self.object.titulo
        return context

class NotaControlCalidadStockListView(PermissionRequiredMixin, ListView):
    permission_required = ('calidad.view_notacontrolcalidadstock')
    model = NotaControlCalidadStock 
    template_name = 'calidad/nota_control_calidad_stock/inicio.html'
    context_object_name = 'contexto_nota_control_calidad_stock'

def NotaControlCalidadStockTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/nota_control_calidad_stock/inicio_tabla.html'
        context = {}
        context['contexto_nota_control_calidad_stock'] = NotaControlCalidadStock.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)  

class NotaControlCalidadStockCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_notacontrolcalidadstock')
    model = NotaControlCalidadStock 
    template_name = "includes/formulario generico.html"
    form_class = NotaControlCalidadStockForm
    success_url = reverse_lazy('calidad_app:nota_control_calidad_stock_inicio')

    def get_context_data(self, **kwargs):
            context = super(NotaControlCalidadStockCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Nota Control Calidad Stock"
            return context

    def form_valid(self, form):
        nro_nota_control_calidad = len(NotaControlCalidadStock.objects.all()) + 1
        form.instance.nro_nota_calidad = numeroXn(nro_nota_control_calidad, 6)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class NotaControlCalidadStockDeleteView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.delete_notacontrolcalidadstock')
    model = NotaControlCalidadStock
    form_class = NotaControlCalidadStockAnularForm    
    template_name = "includes/formulario generico.html"
    success_url = reverse_lazy('calidad_app:nota_control_calidad_stock_inicio')

    def form_valid(self, form):
        form.instance.estado = 3
        registro_guardar(form.instance, self.request)
                
        messages.success(self.request, MENSAJE_ANULAR_NOTA_CONTROL_CALIDAD_STOCK)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Nota Control Calidad Stock'
        return context

class NotaControlCalidadStockDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_notacontrolcalidadstockdetalle')

    model = NotaControlCalidadStock 
    template_name = "calidad/nota_control_calidad_stock/detalle.html"
    context_object_name = 'contexto_nota_control_calidad_stock_detalle'

    def get_context_data(self, **kwargs):
        nota_control_calidad_stock = NotaControlCalidadStock.objects.get(id = self.kwargs['pk'])
        context = super(NotaControlCalidadStockDetailView, self).get_context_data(**kwargs)
        context['nota_control_calidad_detalle'] = NotaControlCalidadStockDetalle.objects.filter(nota_control_calidad_stock = nota_control_calidad_stock)
        return context

def NotaControlCalidadStockDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/nota_control_calidad_stock/detalle_tabla.html'
        context = {}
        nota_control_calidad_stock = NotaControlCalidadStock.objects.get(id = pk)
        context['contexto_nota_control_calidad_stock_detalle'] = nota_control_calidad_stock
        context['nota_control_calidad_detalle'] = NotaControlCalidadStockDetalle.objects.filter(nota_control_calidad_stock = nota_control_calidad_stock)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class NotaControlCalidadStockDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_notacontrolcalidadstockdetalle')
    template_name = "includes/formulario generico.html"
    form_class = NotaControlCalidadStockDetalleAgregarForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_id']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = NotaControlCalidadStock.objects.get(id = self.kwargs['nota_control_calidad_stock_id'])
            item = len(registro.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all())
            material = form.cleaned_data.get('material')
            cantidad_calidad = form.cleaned_data.get('cantidad_calidad')
            inspeccion = form.cleaned_data.get('inspeccion')

            obj, created = NotaControlCalidadStockDetalle.objects.get_or_create(
                nota_ingreso_detalle = material,
                nota_control_calidad_stock = registro,
            )
            if created:
                obj.item = item + 1
                obj.cantidad_calidad = cantidad_calidad
                obj.inspeccion = inspeccion

            else:
                obj.cantidad_calidad = obj.cantidad_calidad + cantidad_calidad

            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        registro = NotaControlCalidadStock.objects.get(id = self.kwargs['nota_control_calidad_stock_id'])
        nota_ingreso = registro.nota_ingreso.id
        materiales = NotaIngresoDetalle.objects.filter(nota_ingreso = nota_ingreso)

        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = materiales
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaControlCalidadStockDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Material'
        return context

class NotaControlCalidadStockDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_notacontrolcalidadstockdetalle')
    model = NotaControlCalidadStockDetalle
    template_name = "includes/formulario generico.html"
    form_class = NotaControlCalidadStockDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Item"
        return context

class NotaControlCalidadStockDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_notacontrolcalidadstockdetalle')
    model = NotaControlCalidadStockDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_id})

    def delete(self, request, *args, **kwargs):
        materiales = NotaControlCalidadStockDetalle.objects.filter(nota_control_calidad_stock=self.get_object().nota_control_calidad_stock)
        contador = 1
        for material in materiales:
            if material == self.get_object():continue
            material.item = contador
            material.save()
            contador += 1

        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Registro"
        return context

class SeriesDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_serie')
    model = NotaControlCalidadStockDetalle
    template_name = "calidad/series/detalle.html"
    context_object_name = 'contexto_series'

    def get_context_data(self, **kwargs):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['pk'])
        # material = nota_control_calidad_stock_detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
        # content_type = material.content_type
        # id_registro = material.id_registro
        context = super(SeriesDetailView, self).get_context_data(**kwargs)
        context['contexto_nota_control_calidad_stock_detalle'] = nota_control_calidad_stock_detalle
        context['contexto_series'] = Serie.objects.filter(nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle)
        # context['contexto_series'] = Serie.objects.filter(content_type = content_type, id_registro = id_registro)

        return context

def SeriesDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/series/detalle_tabla.html'
        context = {}
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = pk)
        # material = nota_control_calidad_stock_detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
        # content_type = material.content_type
        # id_registro = material.id_registro
        context['contexto_nota_control_calidad_stock_detalle'] = nota_control_calidad_stock_detalle
        context['contexto_series'] = Serie.objects.filter(nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle)
        # context['contexto_series'] = Serie.objects.filter(content_type = content_type, id_registro = id_registro)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class SeriesDetalleBuenoCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_series')
    template_name = "includes/formulario generico.html"
    form_class = SerieAgregarBuenoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
            material = registro.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
            content_type = material.content_type
            id_registro = material.id_registro
            serie_base = form.cleaned_data.get('serie_base')
            observacion = form.cleaned_data.get('observacion')
            sociedad_id = registro.nota_ingreso_detalle.nota_ingreso.sociedad
            estado_serie_id = EstadoSerie.objects.get(numero_estado = 1)

            serie = Serie.objects.create(
                serie_base = serie_base,
                content_type = content_type,
                id_registro = id_registro,
                sociedad = sociedad_id,
                nota_control_calidad_stock_detalle = registro,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
            historia_estado_serie = HistorialEstadoSerie.objects.create(
                serie = serie,
                estado_serie = estado_serie_id,
                falla_material = None,
                observacion = observacion,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SeriesDetalleBuenoCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class SeriesDetalleMaloCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_series')
    template_name = "includes/formulario generico.html"
    form_class = SerieAgregarMaloForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
            material = registro.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
            content_type = material.content_type
            id_registro = material.id_registro
            serie_base = form.cleaned_data.get('serie_base')
            falla_material = form.cleaned_data.get('falla_material')
            observacion = form.cleaned_data.get('observacion')
            sociedad_id = registro.nota_ingreso_detalle.nota_ingreso.sociedad
            estado_serie_id = EstadoSerie.objects.get(numero_estado = 1)

            serie = Serie.objects.create(
                serie_base = serie_base,
                content_type = content_type,
                id_registro = id_registro,
                sociedad = sociedad_id,
                nota_control_calidad_stock_detalle = registro,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
            historia_estado_serie = HistorialEstadoSerie.objects.create(
                serie = serie,
                estado_serie = estado_serie_id,
                falla_material = falla_material,
                observacion = observacion,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SeriesDetalleMaloCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class SeriesDetalleBuenoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_serie')
    model = Serie
    template_name = "includes/formulario generico.html"
    form_class = SerieActualizarBuenoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.object.nota_control_calidad_stock_detalle.id})

    def form_valid(self, form):
        historial_estado_serie = HistorialEstadoSerie.objects.get(
                serie = form.instance,
                estado_serie = 1,
            )

        historial_estado_serie.observacion = form.cleaned_data['observacion']
        historial_estado_serie.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SeriesDetalleBuenoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Serie"
        return context

class SeriesDetalleMaloUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_serie')
    model = Serie
    template_name = "includes/formulario generico.html"
    form_class = SerieActualizarMaloForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.object.nota_control_calidad_stock_detalle.id})

    def form_valid(self, form):
        historial_estado_serie = HistorialEstadoSerie.objects.get(
                serie = form.instance,
                estado_serie = 1,
            )

        historial_estado_serie.falla_material = form.cleaned_data['falla_material']
        historial_estado_serie.observacion = form.cleaned_data['observacion']
        historial_estado_serie.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SeriesDetalleMaloUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Serie"
        return context

class SeriesDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_serie')
    model = Serie
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_detalle.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SeriesDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Serie"
        return context