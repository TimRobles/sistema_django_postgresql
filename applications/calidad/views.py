from decimal import Decimal
from urllib import request
from django.core.paginator import Paginator
from django.shortcuts import render
from applications.importaciones import*
from applications.logistica.pdf import generarSeries
from applications.material.funciones import stock_tipo_stock
from applications.material.models import SubFamilia
from applications.datos_globales.models import Unidad
from applications.calidad.forms import(
    EntradaTransformacionProductosForm,
    EntradaTransformacionProductosSeriesForm,
    FallaMaterialForm,
    NotaControlCalidadStockAnularForm,
    NotaControlCalidadStockBuscarForm,
    NotaControlCalidadStockDetalleAgregarForm,
    NotaControlCalidadStockDetalleUpdateForm,
    NotaControlCalidadStockForm,
    NotaControlCalidadStockBuenoUpdateForm,
    NotaControlCalidadStockMaloUpdateForm,
    NotaControlCalidadStockMaloSinSerieUpdateForm,
    # NotaControlCalidadStockBuenoUpdateForm,
    NotaControlCalidadStockBuenoCreateForm,
    NotaControlCalidadStockAgregarMaloCreateForm,
    NotaControlCalidadStockActualizarFallasCreateForm,
    NotaControlCalidadStockAgregarMaloSinFallaCreateForm,
    NotaControlCalidadStockAgregarMaloSinSerieCreateForm,
    NotaControlCalidadStockTransformacionProductosForm,
    ReparacionMaterialDetalleSeriesActualizarForm,
    ReparacionMaterialDetalleSeriesForm,
    SalidaTransformacionProductosForm,
    SalidaTransformacionProductosSeriesForm,
    SerieBuscarForm,
    SolicitudConsumoInternoForm,
    SolicitudConsumoInternoDetalleForm,
    AprobacionConsumoInternoForm,
    SolicitudConsumoInternoRechazarForm,
    SolicitudConsumoInternoDetalleSeriesForm,
    ReparacionMaterialForm,
    ReparacionMaterialDetalleForm,
    SolucionMaterialForm,
    SolucionMaterialGeneralForm,
    TransformacionProductosForm,
    TransformacionProductosUpdateForm,
)
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from applications.muestra.models import NotaIngresoMuestra
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from .models import(
    EntradaTransformacionProductos,
    EstadoSerie,
    NotaControlCalidadStock,
    NotaControlCalidadStockDetalle,
    ReparacionMaterial,
    ReparacionMaterialDetalle,
    SalidaTransformacionProductos,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
    SerieCalidad,
    SolicitudConsumoInterno,
    SolicitudConsumoInternoDetalle,
    AprobacionConsumoInterno,
    AprobacionConsumoInternoDetalle,
    Almacen,
    Sede,
    Material,
    SolucionMaterial,
    ValidarSerieReparacionMaterialDetalle,
    TransformacionProductos,
    ValidarSerieEntradaTransformacionProductos,
    ValidarSerieSalidaTransformacionProductos,
    ValidarSerieSolicitudConsumoInternoDetalle,
)
from applications.funciones import numeroXn, registrar_excepcion
from django import forms

class FallaMaterialTemplateView(PermissionRequiredMixin, TemplateView):
    permission_required = ('calidad.view_fallamaterial')
    template_name = "calidad/falla_material/inicio.html"

    def get_context_data(self, **kwargs):
        sub_familias = SubFamilia.objects.all().order_by('familia__nombre', 'nombre')
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


class FallaMaterialModalDetailView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('calidad.view_fallamaterial')
    model = SubFamilia
    template_name = "calidad/falla_material/detalle_modal.html"
    context_object_name = 'contexto_subfamilia'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        sub_familia = SubFamilia.objects.get(id=self.kwargs['pk'])
        context = super(FallaMaterialModalDetailView, self).get_context_data(**kwargs)
        context['fallas'] = FallaMaterial.objects.filter(sub_familia = sub_familia)
        context['titulo'] = 'Fallas Material'
        return context


class FallaMaterialCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_fallamaterial')
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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


class FallaMaterialUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.view_fallamaterial')
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle_tabla', kwargs={'pk':self.object.sub_familia.id})

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Falla"
        return context


class FallaMaterialDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_fallamaterial')
    model = FallaMaterial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:falla_material')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle', kwargs={'pk':self.object.sub_familia.id})

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Falla"
        context['item'] = self.object.titulo
        return context

class NotaControlCalidadStockListView(PermissionRequiredMixin, FormView):
    permission_required = ('calidad.view_notacontrolcalidadstock')
    form_class = NotaControlCalidadStockBuscarForm
    template_name = 'calidad/nota_control_calidad_stock/inicio.html'

    def get_form_kwargs(self):
        kwargs = super(NotaControlCalidadStockListView, self).get_form_kwargs()
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_usuario'] = self.request.GET.get('usuario')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockListView,self).get_context_data(**kwargs)
        nota_control_calidad_stock = NotaControlCalidadStock.objects.all()

        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_estado = self.request.GET.get('estado')
        filtro_usuario = self.request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_sociedad:
            condicion = Q(nota_ingreso__sociedad = filtro_sociedad)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(nota_control_calidad_stock) > objectsxpage:
            paginator = Paginator(nota_control_calidad_stock, objectsxpage)
            page_number = self.request.GET.get('page')
            nota_control_calidad_stock = paginator.get_page(page_number)
   
        context['contexto_nota_control_calidad_stock'] = nota_control_calidad_stock
        context['contexto_pagina'] = nota_control_calidad_stock
        return context

def NotaControlCalidadStockTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/nota_control_calidad_stock/inicio_tabla.html'
        context = {}
        nota_control_calidad_stock = NotaControlCalidadStock.objects.all()

        filtro_sociedad = request.GET.get('sociedad')
        filtro_estado = request.GET.get('estado')
        filtro_usuario = request.GET.get('usuario')
        
        contexto_filtro = []

        if filtro_sociedad:
            condicion = Q(nota_ingreso__sociedad = filtro_sociedad)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"sociedad={filtro_sociedad}")

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"estado={filtro_estado}")

        if filtro_usuario:
            condicion = Q(created_by = filtro_usuario)
            nota_control_calidad_stock = nota_control_calidad_stock.filter(condicion)
            contexto_filtro.append(f"usuario={filtro_usuario}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage = 10 # Show 10 objects per page.

        if len(nota_control_calidad_stock) > objectsxpage:
            paginator = Paginator(nota_control_calidad_stock, objectsxpage)
            page_number = request.GET.get('page')
            nota_control_calidad_stock = paginator.get_page(page_number)
   
        context['contexto_nota_control_calidad_stock'] = nota_control_calidad_stock
        context['contexto_pagina'] = nota_control_calidad_stock

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class NotaControlCalidadStockCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_notacontrolcalidadstock')
    model = NotaControlCalidadStock
    template_name = "calidad/nota_control_calidad_stock/form.html"
    form_class = NotaControlCalidadStockForm
    success_url = reverse_lazy('calidad_app:nota_control_calidad_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Nota Control Calidad Stock"
        return context

    def form_valid(self, form):
        nro_nota_control_calidad = len(NotaControlCalidadStock.objects.all()) + 1
        form.instance.nro_nota_calidad = numeroXn(nro_nota_control_calidad, 6)
        nota_ingreso_temp = form.cleaned_data.get('nota_ingreso_temp')
        form.instance.content_type = ContentType.objects.get_for_model(nota_ingreso_temp)
        form.instance.id_registro = nota_ingreso_temp.id
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class NotaControlCalidadStockTransformacionProductosCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_notacontrolcalidadstock')
    model = NotaControlCalidadStock
    template_name = "calidad/nota_control_calidad_stock/form.html"
    form_class = NotaControlCalidadStockTransformacionProductosForm
    success_url = reverse_lazy('calidad_app:nota_control_calidad_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockTransformacionProductosCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Nota Control Calidad Stock de Transformación"
        return context

    def form_valid(self, form):
        nro_nota_control_calidad = len(NotaControlCalidadStock.objects.all()) + 1
        form.instance.nro_nota_calidad = numeroXn(nro_nota_control_calidad, 6)
        transformacion_productos_temp = form.cleaned_data.get('transformacion_productos_temp')
        form.instance.content_type = ContentType.objects.get_for_model(transformacion_productos_temp)
        form.instance.id_registro = transformacion_productos_temp.id
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class NotaControlCalidadStockDeleteView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.delete_notacontrolcalidadstock')
    model = NotaControlCalidadStock
    form_class = NotaControlCalidadStockAnularForm
    template_name = "includes/formulario generico.html"
    success_url = reverse_lazy('calidad_app:nota_control_calidad_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if form.instance.estado == 1:
                pass
            elif form.instance.estado == 2:
                detalles = form.instance.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all()
                for detalle in detalles:
                    if detalle.inspeccion == 2:
                        movimiento_final = TipoMovimiento.objects.get(codigo=105) #Inspección, material dañado
                    elif detalle.nota_ingreso_detalle.producto.control_serie:
                        if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                            movimiento_final = TipoMovimiento.objects.get(codigo=148) #Inspección, muestra buena, sin registrar serie
                        else:
                            movimiento_final = TipoMovimiento.objects.get(codigo=106) #Inspección, material bueno, sin registrar serie
                    else:
                        if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                            movimiento_final = TipoMovimiento.objects.get(codigo=149) #Inspección, muestra buena, no requiere serie
                        else:
                            movimiento_final = TipoMovimiento.objects.get(codigo=107) #Inspección, material bueno, no requiere serie

                    movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                        id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso = form.instance.id,
                        almacen = detalle.nota_ingreso_detalle.almacen,
                        sociedad = form.instance.nota_ingreso.sociedad,
                    )
                    movimiento_uno = movimiento_dos.movimiento_anterior
                    
                    movimiento_dos.delete()
                    movimiento_uno.delete()
            elif form.instance.estado == 3:
                detalles = form.instance.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all()
                for detalle in detalles:
                    if detalle.inspeccion == 2:
                        movimiento_final = TipoMovimiento.objects.get(codigo=141) #Registro de Serie, material dañado
                    elif detalle.nota_ingreso_detalle.producto.control_serie:
                        if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                            movimiento_final = TipoMovimiento.objects.get(codigo=150) #Registro de Serie de Muestra
                        else:
                            movimiento_final = TipoMovimiento.objects.get(codigo=108) #Registro de Serie

                    movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                        id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso = form.instance.id,
                        almacen = detalle.nota_ingreso_detalle.almacen,
                        sociedad = form.instance.nota_ingreso.sociedad,
                    )
                    movimiento_uno = movimiento_dos.movimiento_anterior
                    movimiento_anterior_dos = movimiento_uno.movimiento_anterior
                    movimiento_anterior_uno = movimiento_anterior_dos.movimiento_anterior
                    
                    movimiento_dos.delete()
                    movimiento_uno.delete()
                    movimiento_anterior_dos.delete()
                    movimiento_anterior_uno.delete()
            
            form.instance.estado = 4
            registro_guardar(form.instance, self.request)

            messages.success(self.request, MENSAJE_ANULAR_NOTA_CONTROL_CALIDAD_STOCK)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Anular'
        context['titulo'] = 'Nota Control Calidad Stock'
        return context

# CORREGIR
class NotaControlCalidadStockRegistrarSeriesView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_notacontrolcalidadstock')
    model = NotaControlCalidadStock
    template_name = "calidad/nota_control_calidad_stock/boton.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cantidad_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().NotaControlCalidadStockDetalle_nota_control_calidad_stock.all()
        for detalle in detalles:
            if detalle.control_serie and detalle.series_calidad != detalle.cantidad_calidad:
                error_cantidad_series = True
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_cantidad_series:
            context['texto'] = 'Hay Series sin registrar.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super(NotaControlCalidadStockRegistrarSeriesView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            detalles = self.object.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all()
            for detalle in detalles:
                if detalle.nota_ingreso_detalle.producto.control_calidad:
                    if detalle.inspeccion == 1:
                        if detalle.nota_ingreso_detalle.producto.control_serie:
                            if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                                movimiento_inicial = TipoMovimiento.objects.get(codigo=148) #Inspección, muestra buena, sin registrar serie
                                movimiento_final = TipoMovimiento.objects.get(codigo=150) #Registro de Serie de Muestra
                            else:
                                movimiento_inicial = TipoMovimiento.objects.get(codigo=106) #Inspección, material bueno, sin registrar serie
                                movimiento_final = TipoMovimiento.objects.get(codigo=108) #Registro de Serie

                            tipo_stock = movimiento_inicial.tipo_stock_final
                        # elif self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(TransformacionProductos):
                        #     movimiento_inicial = TipoMovimiento.objects.get(codigo=161) #Transformación de productos
                        #     tipo_stock = TipoStock.objects.get(codigo=5) #Bloq sin QA
                        else:
                            continue
                    else:
                        print("Producto malo")
                        movimiento_inicial = TipoMovimiento.objects.get(codigo=105) #Inspección, material dañado
                        movimiento_final = TipoMovimiento.objects.get(codigo=141) #Registro de Serie, material dañado

                    movimiento_anterior = MovimientosAlmacen.objects.get(
                        content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                        id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                        tipo_movimiento = movimiento_inicial,
                        tipo_stock = movimiento_inicial.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso = self.object.id,
                        almacen = detalle.nota_ingreso_detalle.almacen,
                        sociedad = self.object.nota_ingreso.sociedad,
                        movimiento_reversion = False,
                    )

                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                        id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador = -1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso = self.object.id,
                        almacen = movimiento_anterior.almacen,
                        sociedad = self.object.nota_ingreso.sociedad,
                        movimiento_anterior = movimiento_anterior,
                        movimiento_reversion = False,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                        id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso = self.object.id,
                        almacen = movimiento_anterior.almacen,
                        sociedad = self.object.nota_ingreso.sociedad,
                        movimiento_anterior = movimiento_uno,
                        movimiento_reversion = False,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )

                    for serie_calidad in detalle.SerieCalidad_nota_control_calidad_stock_detalle.all():
                        serie = Serie.objects.create(
                            serie_base = serie_calidad.serie.upper(),
                            content_type = serie_calidad.content_type,
                            id_registro = serie_calidad.id_registro,
                            sociedad = serie_calidad.nota_control_calidad_stock_detalle.nota_ingreso_detalle.sociedad,
                            nota_control_calidad_stock_detalle = serie_calidad.nota_control_calidad_stock_detalle,
                            created_by = self.request.user,
                            updated_by = self.request.user,
                        )
                        if serie_calidad.falla_material:
                            #Dañado
                            estado_serie = EstadoSerie.objects.get(numero_estado=2)
                        else:
                            #Bueno
                            estado_serie = EstadoSerie.objects.get(numero_estado=1)

                        HistorialEstadoSerie.objects.create(
                            serie=serie,
                            estado_serie=estado_serie,
                            falla_material=serie_calidad.falla_material,
                            observacion=serie_calidad.observacion,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                        serie.serie_movimiento_almacen.add(movimiento_anterior)
                        serie.serie_movimiento_almacen.add(movimiento_uno)
                        serie.serie_movimiento_almacen.add(movimiento_dos)

                        serie_calidad.delete()

            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONCLUIR_NOTA_CONTROL_CALIDAD_STOCK)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockRegistrarSeriesView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar Series"
        context['titulo'] = "Nota Control Calidad Stock"
        context['dar_baja'] = "true"
        context['item'] = self.object.nro_nota_calidad
        return context

# CORREGIR
class NotaControlCalidadStockConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_notacontrolcalidadstock')
    model = NotaControlCalidadStock
    template_name = "calidad/nota_control_calidad_stock/boton.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            detalles = self.object.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all()
            if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                movimiento_inicial = TipoMovimiento.objects.get(codigo=147) #Ingreso por Muestra, c/QA
            else:
                movimiento_inicial = TipoMovimiento.objects.get(codigo=104) #Ingreso por compra, c/QA

            tipo_stock = movimiento_inicial.tipo_stock_final

            if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(TransformacionProductos):
                movimiento_inicial = TipoMovimiento.objects.get(codigo=161) #Transformación de productos
                tipo_stock = TipoStock.objects.get(codigo=5) #Bloq sin QA
            
            finalizar = True
            for detalle in detalles:
                if detalle.inspeccion == 2:
                    movimiento_final = TipoMovimiento.objects.get(codigo=105) #Inspección, material dañado
                    finalizar &= False
                elif detalle.nota_ingreso_detalle.producto.control_serie:
                    if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                        movimiento_final = TipoMovimiento.objects.get(codigo=148) #Inspección, muestra buena, sin registrar serie
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=106) #Inspección, material bueno, sin registrar serie
                    finalizar &= False
                else:
                    if self.object.nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
                        movimiento_final = TipoMovimiento.objects.get(codigo=149) #Inspección, muestra buena, no requiere serie
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=107) #Inspección, material bueno, no requiere serie

                movimiento_anterior = MovimientosAlmacen.objects.get(
                    content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                    id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                    tipo_movimiento = movimiento_inicial,
                    tipo_stock = tipo_stock,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object.nota_ingreso),
                    id_registro_documento_proceso = self.object.nota_ingreso.id,
                    sociedad = self.object.nota_ingreso.sociedad,
                    almacen = detalle.nota_ingreso_detalle.almacen,
                    movimiento_reversion = False,
                )

                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                    id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                    cantidad = detalle.cantidad_calidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = movimiento_anterior.almacen,
                    sociedad = self.object.nota_ingreso.sociedad,
                    movimiento_anterior = movimiento_anterior,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = ContentType.objects.get_for_model(detalle.nota_ingreso_detalle.producto),
                    id_registro_producto = detalle.nota_ingreso_detalle.producto.id,
                    cantidad = detalle.cantidad_calidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = movimiento_anterior.almacen,
                    sociedad = self.object.nota_ingreso.sociedad,
                    movimiento_anterior = movimiento_uno,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

            if finalizar:
                self.object.estado = 3
            else:
                self.object.estado = 2
            
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONCLUIR_NOTA_CONTROL_CALIDAD_STOCK)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Nota Control Calidad Stock"
        context['dar_baja'] = "true"
        context['item'] = self.object.nro_nota_calidad
        return context


class NotaControlCalidadStockDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_notacontrolcalidadstockdetalle')
    model = NotaControlCalidadStock
    template_name = "calidad/nota_control_calidad_stock/detalle.html"
    context_object_name = 'contexto_nota_control_calidad_stock'

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
        context['contexto_nota_control_calidad_stock'] = nota_control_calidad_stock
        context['nota_control_calidad_detalle'] = NotaControlCalidadStockDetalle.objects.filter(nota_control_calidad_stock = nota_control_calidad_stock)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class NotaControlCalidadStockDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_notacontrolcalidadstockdetalle')
    template_name = "calidad/nota_control_calidad_stock/form_material.html"
    form_class = NotaControlCalidadStockDetalleAgregarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                nota_control_calidad_stock = NotaControlCalidadStock.objects.get(id = self.kwargs['nota_control_calidad_stock_id'])
                item = len(nota_control_calidad_stock.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all())
                nota_ingreso_detalle = form.cleaned_data.get('material')
                content_type = ContentType.objects.get_for_model(nota_ingreso_detalle)
                id_registro = nota_ingreso_detalle.id
                cantidad_calidad = form.cleaned_data.get('cantidad_calidad')
                inspeccion = form.cleaned_data.get('inspeccion')

                buscar = NotaControlCalidadStockDetalle.objects.filter(
                    content_type=content_type,
                    id_registro=id_registro,
                ).exclude(nota_control_calidad_stock__estado=4)
                
                if buscar:
                    contar = buscar.aggregate(Sum('cantidad_calidad'))['cantidad_calidad__sum']
                else:
                    contar = 0
                
                if nota_ingreso_detalle.cantidad < contar + cantidad_calidad:
                    form.add_error('cantidad_calidad', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (nota_ingreso_detalle.cantidad, contar + cantidad_calidad))
                    return super().form_invalid(form)

                obj, created = NotaControlCalidadStockDetalle.objects.get_or_create(
                    content_type = content_type,
                    id_registro = id_registro,
                    nota_control_calidad_stock = nota_control_calidad_stock,
                    inspeccion = inspeccion,
                )
                if created:
                    obj.item = item + 1
                    obj.cantidad_calidad = cantidad_calidad

                else:
                    obj.cantidad_calidad = obj.cantidad_calidad + cantidad_calidad
                    obj.inspeccion = inspeccion

                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero'] = False
                return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            print('*************')
            print(ex)
            print('*************')
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad = NotaControlCalidadStock.objects.get(id = self.kwargs['nota_control_calidad_stock_id'])
        nota_ingreso = nota_control_calidad.nota_ingreso
        
        materiales = nota_ingreso.detalles
        
        materiales_sin_calidad = []
        for material in materiales:
            if not material.producto.control_calidad:
                materiales_sin_calidad.append(material.id)
        materiales = materiales.exclude(id__in = materiales_sin_calidad)
        inspeccion = None
        if nota_ingreso.content_type == ContentType.objects.get_for_model(NotaIngresoMuestra):
            inspeccion = ESTADOS_INSPECCION = [(1, 'BUENO'),]

        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = materiales
        kwargs['inspeccion'] = inspeccion
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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_id})

    def form_valid(self, form):
        nota_ingreso_detalle = form.instance.nota_ingreso_detalle
        content_type = form.instance.content_type
        id_registro = form.instance.id_registro

        buscar = NotaControlCalidadStockDetalle.objects.filter(
            content_type=content_type,
            id_registro=id_registro,
            inspeccion=form.instance.inspeccion,
            nota_control_calidad_stock=form.instance.nota_control_calidad_stock,
        ).exclude(id=form.instance.id)

        if len(buscar) > 0:
            form.add_error('inspeccion', f'Ya existe un producto como {form.instance.get_inspeccion_display()}')
            return super().form_invalid(form)

        buscar = NotaControlCalidadStockDetalle.objects.filter(
            content_type=content_type,
            id_registro=id_registro,
        ).exclude(id=form.instance.id).exclude(nota_control_calidad_stock__estado=4)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_calidad'))['cantidad_calidad__sum']
        else:
            contar = 0

        if nota_ingreso_detalle.cantidad < contar + form.instance.cantidad_calidad:
            form.add_error('cantidad_calidad', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (nota_ingreso_detalle.cantidad, contar + form.instance.cantidad_calidad))
            return super().form_invalid(form)
            
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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = NotaControlCalidadStockDetalle.objects.filter(nota_control_calidad_stock=self.get_object().nota_control_calidad_stock)
            contador = 1
            for material in materiales:
                if material == self.get_object():continue
                material.item = contador
                material.save()
                contador += 1

            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Registro"
        return context

class NotaControlCalidadStockDetalleView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_seriecalidad')
    model = NotaControlCalidadStockDetalle
    template_name = "calidad/series/detalle.html"
    context_object_name = 'contexto_series'

    def get_context_data(self, **kwargs):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['pk'])
        context = super(NotaControlCalidadStockDetalleView, self).get_context_data(**kwargs)
        context['contexto_nota_control_calidad_stock_detalle'] = nota_control_calidad_stock_detalle
        context_series = nota_control_calidad_stock_detalle.SerieCalidad_nota_control_calidad_stock_detalle.all()
        context['contexto_series'] = context_series
        context['cantidad_inspeccionada'] = nota_control_calidad_stock_detalle.cantidad_calidad
        context['cantidad_registrada'] = len(context_series)

        return context

def NotaControlCalidadStockDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/series/detalle_tabla.html'
        context = {}
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = pk)
        context['contexto_nota_control_calidad_stock_detalle'] = nota_control_calidad_stock_detalle
        context_series = nota_control_calidad_stock_detalle.SerieCalidad_nota_control_calidad_stock_detalle.all()
        context['contexto_series'] = context_series
        context['cantidad_inspeccionada'] = nota_control_calidad_stock_detalle.cantidad_calidad
        context['cantidad_registrada'] = len(context_series)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class NotaControlCalidadStockBuenoCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_seriecalidad')
    template_name = "calidad/series/form_agregar.html"
    form_class = NotaControlCalidadStockBuenoCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    @transaction.atomic
    def form_valid(self, form):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                material = nota_control_calidad_stock_detalle.material
                content_type = material.content_type
                id_registro = material.id
                serie_base = form.cleaned_data.get('serie_base')
                observacion = form.cleaned_data.get('observacion')

                buscar = SerieCalidad.objects.filter(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )
                estado = 1
                if len(buscar) > 0:
                    estado = 2

                buscar2 = Serie.objects.filter(
                    serie_base = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )

                if len(buscar2) > 0:
                    estado = 2

                serie = SerieCalidad.objects.create(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                    observacion = observacion,
                    estado = estado,
                    nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaControlCalidadStockBuenoCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class NotaControlCalidadStockAgregarMaloCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_seriecalidad')
    template_name = "calidad/series/form_agregar.html"
    form_class = NotaControlCalidadStockAgregarMaloCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    @transaction.atomic
    def form_valid(self, form):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                material = nota_control_calidad_stock_detalle.material
                content_type = material.content_type
                id_registro = material.id
                serie_base = form.cleaned_data.get('serie_base')
                falla_material = form.cleaned_data.get('falla_material')
                observacion = form.cleaned_data.get('observacion')

                buscar = SerieCalidad.objects.filter(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )
                estado = 1
                if len(buscar) > 0:
                    estado = 2

                buscar2 = Serie.objects.filter(
                    serie_base = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )

                if len(buscar2) > 0:
                    estado = 2
                
                serie = SerieCalidad.objects.create(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                    observacion = observacion,
                    falla_material = falla_material,
                    estado = estado,
                    nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        material = nota_control_calidad_stock_detalle.material
        
        kwargs = super().get_form_kwargs()
        kwargs['falla_material'] = material.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaControlCalidadStockAgregarMaloCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class NotaControlCalidadStockAgregarMaloSinFallaCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_seriecalidad')
    template_name = "calidad/series/form_agregar.html"
    form_class = NotaControlCalidadStockAgregarMaloSinFallaCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    @transaction.atomic
    def form_valid(self, form):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                material = nota_control_calidad_stock_detalle.material
                content_type = material.content_type
                id_registro = material.id
                serie_base = form.cleaned_data.get('serie_base')
                
                buscar = SerieCalidad.objects.filter(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )
                estado = 1
                if len(buscar) > 0:
                    estado = 2

                buscar2 = Serie.objects.filter(
                    serie_base = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )

                if len(buscar2) > 0:
                    estado = 2
                
                serie = SerieCalidad.objects.create(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                    estado = estado,
                    nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaControlCalidadStockAgregarMaloSinFallaCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class NotaControlCalidadStockActualizarFallasCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_seriecalidad')
    template_name = "calidad/series/form_agregar.html"
    form_class = NotaControlCalidadStockActualizarFallasCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    @transaction.atomic
    def form_valid(self, form):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                material = nota_control_calidad_stock_detalle.material
                content_type = material.content_type
                id_registro = material.id
                falla_material = form.cleaned_data.get('falla_material')
                series = SerieCalidad.objects.filter(
                    content_type = content_type,
                    id_registro = id_registro,
                    nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle,
                )
                for serie in series:
                    serie.falla_material = falla_material
                    serie.save()

                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        material = nota_control_calidad_stock_detalle.material
        
        kwargs = super().get_form_kwargs()
        kwargs['falla_material'] = material.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs
    
    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaControlCalidadStockActualizarFallasCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class NotaControlCalidadStockAgregarMaloSinSerieCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_seriecalidad')
    template_name = "calidad/series/form_agregar.html"
    form_class = NotaControlCalidadStockAgregarMaloSinSerieCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.kwargs['nota_control_calidad_stock_detalle_id']})

    @transaction.atomic
    def form_valid(self, form):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                material = nota_control_calidad_stock_detalle.material
                content_type = material.content_type
                id_registro = material.id
                serie_base = form.cleaned_data.get('serie_base')
                falla_material = form.cleaned_data.get('falla_material')
                observacion = form.cleaned_data.get('observacion')

                buscar = SerieCalidad.objects.filter(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )
                estado = 1
                if len(buscar) > 0:
                    estado = 2

                buscar2 = Serie.objects.filter(
                    serie_base = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                )

                if len(buscar2) > 0:
                    estado = 2
                
                serie = SerieCalidad.objects.create(
                    serie = serie_base,
                    content_type = content_type,
                    id_registro = id_registro,
                    observacion = observacion,
                    falla_material = falla_material,
                    estado = estado,
                    nota_control_calidad_stock_detalle = nota_control_calidad_stock_detalle,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad_stock_detalle = NotaControlCalidadStockDetalle.objects.get(id = self.kwargs['nota_control_calidad_stock_detalle_id'])
        material = nota_control_calidad_stock_detalle.material
        
        kwargs = super().get_form_kwargs()
        kwargs['falla_material'] = material.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(NotaControlCalidadStockAgregarMaloSinSerieCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Serie'
        return context

class NotaControlCalidadStockBuenoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_seriecalidad')
    model = SerieCalidad
    template_name = "includes/formulario generico.html"
    form_class = NotaControlCalidadStockBuenoUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.object.nota_control_calidad_stock_detalle.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            buscar = SerieCalidad.objects.filter(
                serie = form.instance.serie,
                content_type = form.instance.content_type,
                id_registro = form.instance.id_registro,
            ).exclude(id=form.instance.id)
            estado = 1
            if len(buscar) > 0:
                estado = 2

            buscar2 = Serie.objects.filter(
                serie_base = form.instance.serie,
                content_type = form.instance.content_type,
                id_registro = form.instance.id_registro,
            ).exclude(id=form.instance.id)

            if len(buscar2) > 0:
                estado = 2
            
            form.instance.estado = estado
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockBuenoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Serie"
        return context

class NotaControlCalidadStockMaloUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_seriecalidad')
    model = SerieCalidad
    template_name = "includes/formulario generico.html"
    form_class = NotaControlCalidadStockMaloUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.object.nota_control_calidad_stock_detalle.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            buscar = SerieCalidad.objects.filter(
                serie = form.instance.serie,
                content_type = form.instance.content_type,
                id_registro = form.instance.id_registro,
            ).exclude(id=form.instance.id)
            estado = 1
            if len(buscar) > 0:
                estado = 2

            buscar2 = Serie.objects.filter(
                serie_base = form.instance.serie,
                content_type = form.instance.content_type,
                id_registro = form.instance.id_registro,
            ).exclude(id=form.instance.id)

            if len(buscar2) > 0:
                estado = 2
            
            form.instance.estado = estado
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad_stock_detalle = self.object.nota_control_calidad_stock_detalle
        material = nota_control_calidad_stock_detalle.material
        
        kwargs = super().get_form_kwargs()
        kwargs['falla_material'] = material.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockMaloUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Serie"
        return context

class NotaControlCalidadStockMaloSinSerieUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_seriecalidad')
    model = SerieCalidad
    template_name = "includes/formulario generico.html"
    form_class = NotaControlCalidadStockMaloSinSerieUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.object.nota_control_calidad_stock_detalle.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            buscar = SerieCalidad.objects.filter(
                serie = form.instance.serie,
                content_type = form.instance.content_type,
                id_registro = form.instance.id_registro,
            ).exclude(id=form.instance.id)
            estado = 1
            if len(buscar) > 0:
                estado = 2

            buscar2 = Serie.objects.filter(
                serie_base = form.instance.serie,
                content_type = form.instance.content_type,
                id_registro = form.instance.id_registro,
            ).exclude(id=form.instance.id)

            if len(buscar2) > 0:
                estado = 2
            
            form.instance.estado = estado
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad_stock_detalle = self.object.nota_control_calidad_stock_detalle
        material = nota_control_calidad_stock_detalle.material
        
        kwargs = super().get_form_kwargs()
        kwargs['falla_material'] = material.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockMaloSinSerieUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Serie"
        return context

class NotaControlCalidadStockSerieCalidadDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_seriecalidad')
    model = SerieCalidad
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:series_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(NotaControlCalidadStockSerieCalidadDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Serie"
        return context


class NotaControlCalidadStockSeriesPdf(View):
    def get(self, request, *args, **kwargs):
        obj = NotaControlCalidadStock.objects.get(id=self.kwargs['pk'])

        color = obj.sociedad.color
        titulo = 'REGISTRO DE SERIES DE EQUIPOS'
        vertical = True
        logo = [obj.sociedad.logo.url]
        pie_pagina = obj.sociedad.pie_pagina

        titulo = "%s - %s - %s" % (titulo, numeroXn(obj.nota_ingreso, 6), obj.proveedor)

        movimientos = MovimientosAlmacen.objects.buscar_movimiento(obj, ContentType.objects.get_for_model(NotaControlCalidadStock))
        series = Serie.objects.buscar_series(movimientos)
        series_unicas = []
        if series:
            series_unicas = series.order_by('id_registro', 'serie_base').distinct()
        
        tipo_documento = "INTERNACIONAL"
        if obj.proveedor:
            if obj.proveedor.ruc:
                tipo_documento = "RUC"

        texto_cabecera = 'La empresa MULTICABLE PERU SAC certifica la entrega a la empresa indicada en el presente documento de los equipos con sus respectivos números de serie enlistados a continuación:'
        
        series_final = {}
        for serie in series_unicas:
            if not serie.producto in series_final:
                series_final[serie.producto] = []
            series_final[serie.producto].append(serie.serie_base)

        TablaEncabezado = ['DOCUMENTOS',
                           'FECHA',
                           'RAZÓN SOCIAL',
                           tipo_documento,
                           ]

        TablaDatos = []
        TablaDatos.append("<br/>".join(obj.documentos))
        TablaDatos.append(obj.fecha.strftime('%d/%m/%Y'))
        if obj.proveedor:
            TablaDatos.append(obj.proveedor.nombre)
            if obj.proveedor.ruc:
                TablaDatos.append(obj.proveedor.ruc)
            else:
                TablaDatos.append("")
        else:
            TablaDatos.append("")
            TablaDatos.append("")

        buf = generarSeries(titulo, vertical, logo, pie_pagina, texto_cabecera, TablaEncabezado, TablaDatos, series_final, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition'] = 'inline; filename=%s.pdf' % titulo

        return respuesta


class SerieBuscarView(PermissionRequiredMixin, FormView):
    permission_required = ('calidad.view_serie')
    template_name = "calidad/series/buscar.html"
    form_class = SerieBuscarForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['serie'] = self.request.GET.get('serie')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SerieBuscarView, self).get_context_data(**kwargs)
        serie = self.request.GET.get('serie')
        if serie:
            buscar_serie = Serie.objects.filter(serie_base = serie.upper())
            context['buscar_serie'] = buscar_serie
        
        return context


class SerieDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_serie')
    model = Serie
    template_name = "calidad/series/ver.html"
    context_object_name = 'contexto_series'

    def get_context_data(self, **kwargs):
        context = super(SerieDetailView, self).get_context_data(**kwargs)
        context['form'] = SerieBuscarForm(serie=None)
        return context


class SolicitudConsumoInternoListView(ListView):
    model = SolicitudConsumoInterno
    template_name = "calidad/consumo/solicitud_consumo_interno/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoListView,self).get_context_data(**kwargs)
        solicitud_consumo_interno = SolicitudConsumoInterno.objects.all()
        context['contexto_solicitud_consumo'] = solicitud_consumo_interno
        return context


def SolicitudConsumoInternoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/consumo/solicitud_consumo_interno/inicio_tabla.html'
        context = {}
        solicitud_consumo_interno = SolicitudConsumoInterno.objects.all()
        context['contexto_solicitud_consumo'] = solicitud_consumo_interno
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SolicitudConsumoInternoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_solicitudconsumointerno')
    model = SolicitudConsumoInterno
    template_name = "includes/formulario generico.html"
    form_class = SolicitudConsumoInternoForm
    success_url = reverse_lazy('calidad_app:solicitud_consumo_interno_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
            context = super(SolicitudConsumoInternoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Solicitud de Consumo Interno"
            return context

    def form_valid(self, form):
        nro_solicitud_consumo_interno = len(SolicitudConsumoInterno.objects.all()) + 1
        form.instance.numero_solicitud = numeroXn(nro_solicitud_consumo_interno, 6)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class SolicitudConsumoInternoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_solicitudconsumointerno')
    model = SolicitudConsumoInterno
    # template_name = "calidad/consumo/solicitud_consumo_interno/form.html"
    template_name = "includes/formulario generico.html"
    form_class = SolicitudConsumoInternoForm
    success_url = reverse_lazy('calidad_app:solicitud_consumo_interno_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Solicitud de Consumo Interno"
        return context


class SolicitudConsumoInternoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.change_solicitudconsumointerno')

    model = SolicitudConsumoInterno
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:solicitud_consumo_interno_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Solicitud Consumo Interno"
        context['dar_baja'] = "true"
        context['item'] = 'Solicitud Nro ' + str(self.object.numero_solicitud) + ' / '+ str(self.object.fecha_solicitud) + ' / ' + str(self.object.solicitante)
        return context


class SolicitudConsumoInternoConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.change_solicitudconsumointerno')
    model = SolicitudConsumoInterno
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:solicitud_consumo_interno_inicio')

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().SolicitudConsumoInternoDetalle_solicitud_consumo.all()
        for detalle in detalles:
            if detalle.series_validar != detalle.cantidad and detalle.material.control_serie:
                error_series = True
        
        if error_series:
            context['texto'] = 'La cantidad de series no coincide.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def generar_aprobacion_consumo(self):
        solicitud_consumo = SolicitudConsumoInterno.objects.get(id=self.get_object().id)
        aprobacion_consumo = AprobacionConsumoInterno.objects.create(
                numero_aprobacion=len(AprobacionConsumoInterno.objects.all()) + 1,
                estado=1,
                solicitud_consumo=solicitud_consumo,
                created_by = self.request.user,
                updated_by = self.request.user,
            )
        query_solicitud_consumo = SolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo=solicitud_consumo)      
        list_aprobacion_detalle = []
        for fila_detalle in query_solicitud_consumo:
            list_aprobacion_detalle.append(
                AprobacionConsumoInternoDetalle(
                    item = fila_detalle.item,
                    material = fila_detalle.material,
                    cantidad = fila_detalle.cantidad,
                    sede = fila_detalle.sede,
                    almacen = fila_detalle.almacen,
                    aprobacion_consumo = aprobacion_consumo,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                    )    
                )
        AprobacionConsumoInternoDetalle.objects.bulk_create(list_aprobacion_detalle)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            self.generar_aprobacion_consumo()
            messages.success(request, MENSAJE_ACTUALIZACION)
            # return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Solicitud Consumo Interno"
        context['dar_baja'] = "true"
        context['item'] = 'Solicitud Nro ' + str(self.object.numero_solicitud) + ' / '+ str(self.object.fecha_solicitud) + ' / ' + str(self.object.solicitante)
        return context


class SolicitudConsumoInternoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_solicitudconsumointerno')
    model = SolicitudConsumoInterno
    template_name = "calidad/consumo/solicitud_consumo_interno/detalle.html"
    context_object_name = 'contexto_solicitud_consumo'

    def get_context_data(self, **kwargs):
        solicitud_consumo = SolicitudConsumoInterno.objects.get(id=self.kwargs['pk'])
        context = super(SolicitudConsumoInternoDetailView, self).get_context_data(**kwargs)
        context['contexto_solicitud_consumo'] = solicitud_consumo
        context['contexto_solicitud_consumo_detalle'] = SolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo = solicitud_consumo)
        return context


def SolicitudConsumoInternoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/consumo/solicitud_consumo_interno/detalle_tabla.html'
        context = {}
        solicitud_consumo = SolicitudConsumoInterno.objects.get(id = pk)
        context['contexto_solicitud_consumo'] = solicitud_consumo
        context['contexto_solicitud_consumo_detalle'] = SolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo = solicitud_consumo)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SolicitudConsumoInternoDetalleCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_solicitudconsumointernodetalle')
    model = SolicitudConsumoInternoDetalle
    template_name = "calidad/consumo/solicitud_consumo_interno/form.html"
    form_class = SolicitudConsumoInternoDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solicitud_consumo_interno_detalle', kwargs={'pk':self.kwargs['solicitud_consumo_id']})

    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Añadir"
        context['titulo']="Detalle Solicitud de Consumo Interno"
        solicitud_consumo = SolicitudConsumoInterno.objects.get(id=self.kwargs['solicitud_consumo_id'])
        context['id_sociedad'] = solicitud_consumo.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock_disponible', kwargs={'id_material':1})[:-2]
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SolicitudConsumoInternoDetalleCreateView, self).get_form_kwargs(*args, **kwargs)
        solicitud_consumo = SolicitudConsumoInterno.objects.get(id=self.kwargs['solicitud_consumo_id'])
        kwargs['id_sociedad'] = solicitud_consumo.sociedad.id
        return kwargs

    def form_valid(self, form):
        solicitud_consumo = SolicitudConsumoInterno.objects.get(id=self.kwargs['solicitud_consumo_id'])
        item = len(SolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo=solicitud_consumo)) + 1
        form.instance.item = numeroXn(item, 6)
        form.instance.solicitud_consumo = solicitud_consumo
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    # def get_form(self, *args, **kwargs):
    #     form = super(SolicitudConsumoInternoDetalleCreateView, self).get_form(*args, **kwargs)
    #     form.fields['almacen'].queryset = Almacen.filter(sede = self.kwargs['id_sede'])


class SolicitudConsumoInternoDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_solicitudconsumointernodetalle')

    model = SolicitudConsumoInternoDetalle
    template_name = "calidad/consumo/solicitud_consumo_interno/form.html"
    form_class = SolicitudConsumoInternoDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solicitud_consumo_interno_detalle', kwargs={'pk':self.get_object().solicitud_consumo.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SolicitudConsumoInternoDetalleUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['id_sociedad'] = self.object.solicitud_consumo.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Detalle Solicitud de Consumo"
        context['id_sociedad'] = self.object.solicitud_consumo.sociedad.id
        context['id_material'] = self.object.material.id
        context['url_stock'] = reverse_lazy('material_app:stock_disponible', kwargs={'id_material':1})[:-2]
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class SolicitudConsumoInternoDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_solicitudconsumointernodetalle')
    model = SolicitudConsumoInternoDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():   
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solicitud_consumo_interno_detalle', kwargs={'pk':self.get_object().solicitud_consumo.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            filas_detalle = SolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo=self.get_object().solicitud_consumo)
            contador = 1
            for fila in filas_detalle:
                if fila == self.get_object():continue
                fila.item = contador
                fila.save()
                contador += 1

            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(SolicitudConsumoInternoDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Item"
        context['item'] = str(self.object.item) + ' - ' + self.object.material.descripcion_corta
        return context


class MaterialUnidad(forms.Form):
    unidad = forms.ModelChoiceField(queryset=Unidad.objects.all(), required=False)

def MaterialUnidadView(request, pk):
    form = MaterialUnidad()
    materiales = Material.objects.filter(id=pk)
    print(20*'*.')
    print(type(materiales[0].unidad_base))
    print(20*'*.')
    form.fields['unidad'].queryset = Unidad.objects.filter(nombre=materiales[0].unidad_base.nombre)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form': form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)


class AprobacionConsumoInternoListView(ListView):
    model = AprobacionConsumoInterno
    template_name = "calidad/consumo/aprobacion_consumo_interno/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(AprobacionConsumoInternoListView,self).get_context_data(**kwargs)
        aprobacion_consumo_interno = AprobacionConsumoInterno.objects.all()
        context['contexto_aprobacion_consumo'] = aprobacion_consumo_interno
        return context


def AprobacionConsumoInternoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/consumo/aprobacion_consumo_interno/inicio_tabla.html'        
        context = {}
        aprobacion_consumo_interno = AprobacionConsumoInterno.objects.all()
        context['contexto_aprobacion_consumo'] = aprobacion_consumo_interno
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AprobacionConsumoInternoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_aprobacionconsumointerno')
    model = AprobacionConsumoInterno
    template_name = "includes/formulario generico.html"
    form_class = AprobacionConsumoInternoForm
    success_url = reverse_lazy('calidad_app:aprobacion_consumo_interno_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AprobacionConsumoInternoCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Registrar'
        context['titulo'] = 'Aprobación de Consumo Interno'
        return context

    def guardar_detalle_aprobacion_consumo(self, form, nro_aprobacion_consumo):
        solicitud_consumo = form.instance.solicitud_consumo
        query_solicitud_consumo = SolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo=solicitud_consumo)
        list_aprobacion_detalle = []
        for fila_detalle in query_solicitud_consumo:
            list_aprobacion_detalle.append(
                AprobacionConsumoInternoDetalle(
                    item = fila_detalle.item,
                    material = fila_detalle.material,
                    cantidad = fila_detalle.cantidad,
                    sede = fila_detalle.sede,
                    almacen = fila_detalle.almacen,
                    aprobacion_consumo = form.instance.id,
                    )    
                )
        AprobacionConsumoInternoDetalle.objects.bulk_create(list_aprobacion_detalle)

    def form_valid(self, form):
        nro_aprobacion_consumo = len(AprobacionConsumoInterno.objects.all()) + 1
        form.instance.numero_aprobacion = numeroXn(nro_aprobacion_consumo, 6)
        registro_guardar(form.instance, self.request)
        # self.guardar_detalle_aprobacion_consumo(form, nro_aprobacion_consumo)
        return super().form_valid(form)


class AprobacionConsumoInternoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad_app:change_aprobacionconsumointerno')
    model = AprobacionConsumoInterno
    template_name = "calidad/consumo/aprobacion_consumo_interno/actualizar.html"
    form_class = AprobacionConsumoInternoForm
    success_url = reverse_lazy('calidad_app:aprobacion_consumo_interno_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AprobacionConsumoInternoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Aprobación de Consumo Interno'
        return context
    

class AprobacionConsumoInternoDetailView(DetailView):
    model = AprobacionConsumoInterno
    template_name = "calidad/consumo/aprobacion_consumo_interno/detalle.html"
    context_object_name = 'contexto_aprobacion_consumo'

    def get_context_data(self, **kwargs):
        aprobacion_consumo = AprobacionConsumoInterno.objects.get(id=self.kwargs['pk'])
        context = super(AprobacionConsumoInternoDetailView, self).get_context_data(**kwargs)
        context['contexto_aprobacion_consumo'] = aprobacion_consumo
        context['contexto_aprobacion_consumo_detalle'] = AprobacionConsumoInternoDetalle.objects.filter(aprobacion_consumo = aprobacion_consumo)
        return context


def AprobacionConsumoInternoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/consumo/aprobacion_consumo_interno/detalle_tabla.html'
        context = {}
        aprobacion_consumo = AprobacionConsumoInterno.objects.get(id = pk)
        context['contexto_aprobacion_consumo'] = aprobacion_consumo
        context['contexto_aprobacion_consumo_detalle'] = AprobacionConsumoInternoDetalle.objects.filter(aprobacion_consumo = aprobacion_consumo)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class AprobacionConsumoInternoAprobarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.change_aprobacionconsumointerno')
    model = AprobacionConsumoInterno
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:aprobacion_consumo_interno_inicio')

    def actualizar_estado_solicitud(self):
        aprobacion_consumo = SolicitudConsumoInterno.objects.get(id = self.object.solicitud_consumo.id)
        aprobacion_consumo.estado = 6       # APROBAR SOLICITUD
        aprobacion_consumo.save()

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            tipo_movimiento = TipoMovimiento.objects.get(codigo=152) #Consumo de Material

            for detalle in self.object.AprobacionConsumoInternoDetalle_aprobacion_consumo.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = tipo_movimiento.tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = detalle.aprobacion_consumo.content_type,
                    id_registro_documento_proceso = detalle.aprobacion_consumo.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.sociedad,
                    movimiento_anterior = None,
                    created_by = request.user,
                    updated_by = request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = tipo_movimiento.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = detalle.aprobacion_consumo.content_type,
                    id_registro_documento_proceso = detalle.aprobacion_consumo.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.sociedad,
                    movimiento_anterior = movimiento_uno,
                    created_by = request.user,
                    updated_by = request.user,
                )

                for serie in detalle.aprobacion_consumo.solicitud_consumo.SolicitudConsumoInternoDetalle_solicitud_consumo.get(item=detalle.item).ValidarSerieSolicitudConsumoInternoDetalle_solicitud_consumo_detalle.all():
                    HistorialEstadoSerie.objects.create(
                        serie=serie.serie,
                        estado_serie=EstadoSerie.objects.get(numero_estado=10),
                        falla_material=None,
                        observacion=None,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    serie.serie.serie_movimiento_almacen.add(movimiento_uno)
                    serie.serie.serie_movimiento_almacen.add(movimiento_dos)

            self.object.estado = 2          # APROBADO
            self.actualizar_estado_solicitud()
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_ACTUALIZACION)

        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AprobacionConsumoInternoAprobarView, self).get_context_data(**kwargs)
        context['accion'] = "Aprobar"
        context['titulo'] = "Solicitud de Consumo Interno"
        context['dar_baja'] = "true"
        context['item'] = 'Solicitud Nro ' + str(self.object.solicitud_consumo.numero_solicitud) + ' / '+ str(self.object.solicitud_consumo.fecha_solicitud) + ' / ' + str(self.object.solicitud_consumo.solicitante)
        return context


class AprobacionConsumoInternoRechazarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_aprobacionconsumointerno')
    model = SolicitudConsumoInterno
    template_name = "includes/formulario generico.html"
    success_url = reverse_lazy('calidad_app:aprobacion_consumo_interno_inicio')
    form_class = SolicitudConsumoInternoRechazarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AprobacionConsumoInternoRechazarView, self).get_context_data(**kwargs)
        context['accion'] = "Rechazar"
        context['titulo'] = "Solicitud de Consumo Interno"
        context['dar_baja'] = "true"
        # context['item'] = 'Solicitud Nro ' + str(self.object.numero_solicitud) + ' / '+ str(self.object.fecha_solicitud) + ' / ' + str(self.object.solicitante)
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            aprobacion_consumo = AprobacionConsumoInterno.objects.get(solicitud_consumo = form.instance)
            aprobacion_consumo.estado = 3  # RECHAZADO
            aprobacion_consumo.save()
            form.instance.estado = 5       # RECHAZAR SOLICITUD
            registro_guardar(form.instance, self.request)
            messages.success(self.request, MENSAJE_ACTUALIZACION)
            return super().form_valid(form)

        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)



class ValidarSeriesSolicitudConsumoDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('calidad.view_solicitudconsumointernodetalle')
    template_name = "calidad/consumo/solicitud_consumo_interno/validar_serie/detalle.html"
    form_class = SolicitudConsumoInternoDetalleSeriesForm
    success_url = '.'

    def form_valid(self, form):
        # if self.request.session['primero']:
        serie = form.cleaned_data['serie']
        solicitud_consumo_detalle = SolicitudConsumoInternoDetalle.objects.get(id = self.kwargs['pk'])
        try:
            buscar = Serie.objects.get(
                serie_base=serie,
                content_type=ContentType.objects.get_for_model(solicitud_consumo_detalle.material),
                id_registro=solicitud_consumo_detalle.material.id,
            )
            buscar2 = ValidarSerieSolicitudConsumoInternoDetalle.objects.filter(serie = buscar)

            if len(buscar2) != 0:
                form.add_error('serie', "Serie ya ha sido registrada")
                return super().form_invalid(form)

            if buscar.estado != 'DISPONIBLE':
                form.add_error('serie', "Serie no disponible, su estado es: %s" % buscar.estado)
                return super().form_invalid(form)
        except:
            form.add_error('serie', "Serie no encontrada: %s" % serie)
            return super().form_invalid(form)

        obj, created = ValidarSerieSolicitudConsumoInternoDetalle.objects.get_or_create(
            solicitud_consumo_detalle=solicitud_consumo_detalle,
            serie=buscar,
        )
        if created:
            obj.estado = 1
        # self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        solicitud_consumo_detalle = SolicitudConsumoInternoDetalle.objects.get(id = self.kwargs['pk'])
        cantidad = solicitud_consumo_detalle.cantidad
        cantidad_ingresada = len(ValidarSerieSolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo_detalle=solicitud_consumo_detalle))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad'] = cantidad
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        # self.request.session['primero'] = True
        solicitud_consumo_detalle = SolicitudConsumoInternoDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesSolicitudConsumoDetailView, self).get_context_data(**kwargs)
        context['contexto_solicitud_consumo_detalle'] = solicitud_consumo_detalle
        context['contexto_series'] = ValidarSerieSolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo_detalle = solicitud_consumo_detalle)
        return context


def ValidarSeriesSolicitudConsumoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/consumo/solicitud_consumo_interno/validar_serie/detalle_tabla.html'
        context = {}
        solicitud_consumo_detalle = SolicitudConsumoInternoDetalle.objects.get(id = pk)
        context['contexto_solicitud_consumo_detalle'] = solicitud_consumo_detalle
        context['contexto_series'] = ValidarSerieSolicitudConsumoInternoDetalle.objects.filter(solicitud_consumo_detalle = solicitud_consumo_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesSolicitudConsumoDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_validarseriesolicitudconsumointernodetalle')
    model = ValidarSerieSolicitudConsumoInternoDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solicitud_consumo_validar_series_detalle', kwargs={'pk': self.get_object().solicitud_consumo_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesSolicitudConsumoDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context


class ReparacionMaterialListView(ListView):
    model = ReparacionMaterial
    template_name = "calidad/reparacion/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReparacionMaterialListView,self).get_context_data(**kwargs)
        reparacion_material = ReparacionMaterial.objects.all()
        context['contexto_reparacion_material'] = reparacion_material
        return context


def ReparacionMaterialTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/reparacion/inicio_tabla.html'
        context = {}
        reparacion_material = ReparacionMaterial.objects.all()
        context['contexto_reparacion_material'] = reparacion_material

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ReparacionMaterialCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_reparacionmaterial')
    model = ReparacionMaterial
    template_name = "includes/formulario generico.html"
    form_class = ReparacionMaterialForm
    success_url = reverse_lazy('calidad_app:reparacion_material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
            context = super(ReparacionMaterialCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Reparación de Materiales"
            return context

    def form_valid(self, form):
        horas = form.cleaned_data['horas']
        minutos = form.cleaned_data['minutos']
        tiempo_total = 60*horas + minutos
        form.instance.tiempo_estimado = tiempo_total
        nro_reparacion = len(ReparacionMaterial.objects.all()) + 1
        form.instance.numero_reparacion = numeroXn(nro_reparacion, 6)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class ReparacionMaterialUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.reparacionmaterial')
    model = ReparacionMaterial
    template_name = "includes/formulario generico.html"
    form_class = ReparacionMaterialForm
    success_url = reverse_lazy('calidad_app:reparacion_material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReparacionMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Reparación de Material"
        return context


class ReparacionMaterialDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_reparacionmaterial')
    model = ReparacionMaterial
    template_name = "calidad/reparacion/detalle.html"
    context_object_name = 'contexto_reparacion_material'

    def get_context_data(self, **kwargs):
        reparacion_material = ReparacionMaterial.objects.get(id=self.kwargs['pk'])
        context = super(ReparacionMaterialDetailView, self).get_context_data(**kwargs)
        context['contexto_reparacion_material'] = reparacion_material
        context['contexto_reparacion_material_detalle'] = ReparacionMaterialDetalle.objects.filter(reparacion = reparacion_material)
        return context


def ReparacionMaterialDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/reparacion/detalle_tabla.html'
        context = {}
        reparacion_material = ReparacionMaterial.objects.get(id = pk)
        context['contexto_reparacion_material'] = reparacion_material
        context['contexto_reparacion_material_detalle'] = ReparacionMaterialDetalle.objects.filter(reparacion = reparacion_material)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
        

class ReparacionMaterialDetalleCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_solicitudconsumointernodetalle')
    model = ReparacionMaterialDetalle
    template_name = "calidad/reparacion/form.html"
    form_class = ReparacionMaterialDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:reparacion_material_detalle', kwargs={'pk':self.kwargs['reparacion_id']})

    def get_context_data(self, **kwargs):
        context = super(ReparacionMaterialDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Añadir"
        context['titulo']="Detalle Reparación de Material"
        reparacion_material = ReparacionMaterial.objects.get(id=self.kwargs['reparacion_id'])
        context['id_sociedad'] = reparacion_material.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock_disponible', kwargs={'id_material':1})[:-2]
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReparacionMaterialDetalleCreateView, self).get_form_kwargs(*args, **kwargs)
        reparacion_material = ReparacionMaterial.objects.get(id=self.kwargs['reparacion_id'])
        kwargs['id_sociedad'] = reparacion_material.sociedad.id
        return kwargs

    def form_valid(self, form):
        reparacion_material = ReparacionMaterial.objects.get(id=self.kwargs['reparacion_id'])
        item = len(ReparacionMaterialDetalle.objects.filter(reparacion=reparacion_material)) + 1
        form.instance.item = numeroXn(item, 6)
        form.instance.reparacion = reparacion_material
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class ReparacionMaterialDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_reparacionmaterialdetalle')
    model = ReparacionMaterialDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():   
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:reparacion_material_detalle', kwargs={'pk':self.get_object().reparacion.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            filas_detalle = ReparacionMaterialDetalle.objects.filter(reparacion=self.get_object().reparacion)
            contador = 1
            for fila in filas_detalle:
                if fila == self.get_object():continue
                fila.item = contador
                fila.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(ReparacionMaterialDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Item"
        context['item'] = str(self.object.item) + ' - ' + self.object.material.descripcion_corta
        return context



class ReparacionMaterialDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_reparacionmaterialdetalle')

    model = ReparacionMaterialDetalle
    template_name = "calidad/reparacion/form.html"
    form_class = ReparacionMaterialDetalleForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:reparacion_material_detalle', kwargs={'pk':self.get_object().reparacion.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReparacionMaterialDetalleUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['id_sociedad'] = self.object.reparacion.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReparacionMaterialDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Detalle Reparación de Material"
        context['id_sociedad'] = self.object.reparacion.sociedad.id
        context['id_material'] = self.object.material.id
        context['url_stock'] = reverse_lazy('material_app:stock_disponible', kwargs={'id_material':1})[:-2]
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class ValidarSeriesReparacionMaterialDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('calidad.view_solicitudconsumointernodetalle')
    template_name = "calidad/reparacion/validar_serie/detalle.html"
    form_class = ReparacionMaterialDetalleSeriesForm
    success_url = '.'

    def form_valid(self, form):
        # if self.request.session['primero']:
        serie = form.cleaned_data['serie']
        reparacion_detalle = ReparacionMaterialDetalle.objects.get(id = self.kwargs['pk'])
        try:
            buscar = Serie.objects.get(
                serie_base=serie,
                content_type=ContentType.objects.get_for_model(reparacion_detalle.material),
                id_registro=reparacion_detalle.material.id,
            )
            buscar2 = ValidarSerieReparacionMaterialDetalle.objects.filter(serie = buscar)

            if len(buscar2) != 0:
                form.add_error('serie', "Serie ya ha sido registrada")
                return super().form_invalid(form)

            if buscar.numero_estado != 2: # CON PROBLEMAS
                form.add_error('serie', "Serie NO DAÑADA, su estado es: %s" % buscar.estado)
                return super().form_invalid(form)
        except:
            form.add_error('serie', "Serie no encontrada: %s" % serie)
            return super().form_invalid(form)

        obj, created = ValidarSerieReparacionMaterialDetalle.objects.get_or_create(
            reparacion_detalle=reparacion_detalle,
            serie=buscar,
        )
        if created:
            obj.estado = 1
        # self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        reparacion_detalle = ReparacionMaterialDetalle.objects.get(id = self.kwargs['pk'])
        cantidad = reparacion_detalle.cantidad
        cantidad_ingresada = len(ValidarSerieReparacionMaterialDetalle.objects.filter(reparacion_detalle=reparacion_detalle))        
        kwargs = super().get_form_kwargs()
        kwargs['cantidad'] = cantidad
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        # self.request.session['primero'] = True
        reparacion_detalle = ReparacionMaterialDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesReparacionMaterialDetailView, self).get_context_data(**kwargs)
        context['contexto_reparacion_material_detalle'] = reparacion_detalle
        context['contexto_series'] = ValidarSerieReparacionMaterialDetalle.objects.filter(reparacion_detalle = reparacion_detalle)
        return context


def ValidarSeriesReparacionMaterialDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/reparacion/validar_serie/detalle_tabla.html'
        context = {}
        reparacion_detalle = ReparacionMaterialDetalle.objects.get(id = pk)
        context['contexto_reparacion_material_detalle'] = reparacion_detalle
        context['contexto_series'] = ValidarSerieReparacionMaterialDetalle.objects.filter(reparacion_detalle = reparacion_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ValidarSeriesReparacionMaterialDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_reparacionmaterialdetalle')

    model = ValidarSerieReparacionMaterialDetalle
    template_name = "calidad/reparacion/validar_serie/form.html"
    form_class = ReparacionMaterialDetalleSeriesActualizarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:reparacion_material_validar_series_detalle', kwargs={'pk':self.get_object().reparacion_detalle.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ValidarSeriesReparacionMaterialDetalleUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['subfamilia'] = self.object.reparacion_detalle.material.subfamilia
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesReparacionMaterialDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Validar Serie Detalle Reparación de Material"
        return context

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class ValidarSeriesReparacionMaterialDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_validarseriesreparacionmaterialdetalle')
    model = ValidarSerieReparacionMaterialDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:reparacion_material_validar_series_detalle', kwargs={'pk': self.get_object().reparacion_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesReparacionMaterialDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context

class ReparacionMaterialConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.change_reparacionmaterial')
    model = ReparacionMaterial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:reparacion_material_inicio')

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().ReparacionMaterialDetalle_reparacion.all()
        for detalle in detalles:
            if detalle.series_validar != detalle.cantidad:
                error_series = True
        
        if error_series:
            context['texto'] = 'La cantidad de series no coincide.'
            return render(request, 'includes/modal sin permiso.html', context)

        if len(detalles) == 0:
            context['texto'] = 'Debe agregar al menos un item.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            tipo_movimiento = TipoMovimiento.objects.get(codigo=160) # Reparación, material reparado

            for detalle in self.object.ReparacionMaterialDetalle_reparacion.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = tipo_movimiento.tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = detalle.reparacion.content_type,
                    id_registro_documento_proceso = detalle.reparacion.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.reparacion.sociedad,
                    movimiento_anterior = None,
                    created_by = request.user,
                    updated_by = request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = tipo_movimiento.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = detalle.reparacion.content_type,
                    id_registro_documento_proceso = detalle.reparacion.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.reparacion.sociedad,
                    movimiento_anterior = movimiento_uno,
                    created_by = request.user,
                    updated_by = request.user,
                )

                for serie in detalle.ValidarSerieReparacionMaterialDetalle_reparacion_detalle.all():
                    HistorialEstadoSerie.objects.create(
                        serie=serie.serie,
                        estado_serie=EstadoSerie.objects.get(numero_estado=5), # REPARADO
                        falla_material=serie.solucion_material.falla_material,
                        solucion=serie.solucion_material,
                        observacion=serie.observacion,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    serie.serie.serie_movimiento_almacen.add(movimiento_uno)
                    serie.serie.serie_movimiento_almacen.add(movimiento_dos)            

            self.object.estado = 3          # CONCLUIDO
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_ACTUALIZACION)

        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ReparacionMaterialConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Reparación de Material"
        context['dar_baja'] = "true"
        context['item'] = 'Doc. Reparación Nro. ' + str(self.object)
        return context


class SolucionMaterialTemplateView(PermissionRequiredMixin, TemplateView):
    permission_required = ('calidad.view_solucionmaterial')
    template_name = "calidad/solucion_material/inicio.html"

    def get_context_data(self, **kwargs):
        sub_familias = SubFamilia.objects.all
        context = super(SolucionMaterialTemplateView, self).get_context_data(**kwargs)
        context['contexto_subfamilias'] = sub_familias

        return context


class SolucionMaterialDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_solucionmaterial')
    model = FallaMaterial
    template_name = "calidad/solucion_material/detalle.html"
    context_object_name = 'contexto_fallamaterial'

    def get_context_data(self, **kwargs):
        falla_material = FallaMaterial.objects.get(id=self.kwargs['pk'])
        context = super(SolucionMaterialDetailView, self).get_context_data(**kwargs)
        context['contexto_soluciones_material'] = SolucionMaterial.objects.filter(falla_material = falla_material)
        context['contexto_falla_material'] = falla_material
        return context


def SolucionMaterialDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/solucion_material/detalle_tabla.html'
        context = {}
        falla_material = FallaMaterial.objects.get(id=pk)
        context['contexto_soluciones_material'] = SolucionMaterial.objects.filter(falla_material = falla_material)
        context['contexto_falla_material'] = falla_material

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

        
class SolucionMaterialModalDetailView(PermissionRequiredMixin, BSModalReadView):
    permission_required = ('calidad.view_solucionmaterial')
    model = SubFamilia
    template_name = "calidad/solucion_material/detalle_modal.html"
    context_object_name = 'contexto_subfamilia'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        sub_familia = SubFamilia.objects.get(id=self.kwargs['pk'])
        context = super(SolucionMaterialModalDetailView, self).get_context_data(**kwargs)
        context['contexto_soluciones_material'] = SolucionMaterial.objects.filter(falla_material__sub_familia = sub_familia)
        context['titulo'] = 'Soluciones de Fallas de Material'
        return context


class SolucionMaterialCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_solucionmaterial')
    model = SolucionMaterial
    template_name = "includes/formulario generico.html"
    form_class = SolucionMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solucion_material_detalle', kwargs={'pk':self.kwargs['falla_material_id']})

    def form_valid(self, form):
        form.instance.falla_material = FallaMaterial.objects.get(id = self.kwargs['falla_material_id'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolucionMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Solución"
        return context

class SolucionMaterialGeneralCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.add_solucionmaterial')
    model = SolucionMaterial
    template_name = "includes/formulario generico.html"
    form_class = SolucionMaterialGeneralForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SolucionMaterialGeneralCreateView, self).get_form_kwargs(*args, **kwargs)
        subfamilia = SubFamilia.objects.get(id = self.kwargs['subfamilia_id'])
        kwargs['subfamilia'] = subfamilia
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SolucionMaterialGeneralCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Solución"
        return context


class SolucionMaterialUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.view_solucionmaterial')
    model = SolucionMaterial
    template_name = "includes/formulario generico.html"
    form_class = SolucionMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solucion_material_detalle_tabla', kwargs={'pk':self.object.falla_material.id})

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SolucionMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Solución"
        return context


class SolucionMaterialDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_solucionmaterial')
    model = SolucionMaterial
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:solucion_material_detalle', kwargs={'pk':self.object.falla_material.id})

    def get_context_data(self, **kwargs):
        context = super(SolucionMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Solución"
        context['item'] = self.object.titulo
        return context



class TransformacionProductosListView(PermissionRequiredMixin, ListView):
    permission_required = ('calidad.view_transformacionproductos')
    model = TransformacionProductos
    template_name = "calidad/transformacion_productos/inicio.html"
    context_object_name = 'contexto_transformacion_productos'

def TransformacionProductosTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/transformacion_productos/inicio_tabla.html'
        context = {}
        context['contexto_transformacion_productos'] = TransformacionProductos.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class TransformacionProductosCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('calidad.view_transformacionproductos')
    model = TransformacionProductos
    template_name = "includes/formulario generico.html"
    form_class = TransformacionProductosForm
    success_url = reverse_lazy('calidad_app:transformacion_productos_inicio')

    def get_context_data(self, **kwargs):
        context = super(TransformacionProductosCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Documento de Transformación"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        nro_transformacion = len(TransformacionProductos.objects.all()) + 1
        form.instance.numero_transformacion = numeroXn(nro_transformacion, 6)
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class TransformacionProductosUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_transformacionproductos')
    model = TransformacionProductos
    template_name = "includes/formulario generico.html"
    form_class = TransformacionProductosUpdateForm
    success_url = reverse_lazy('calidad_app:transformacion_productos_inicio')

    def get_context_data(self, **kwargs):
        context = super(TransformacionProductosUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Documento de Transformación"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class TransformacionProductosDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_transformacionproductos')
    model = TransformacionProductos
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:transformacion_productos_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransformacionProductosDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Documento"
        context['item'] = self.get_object().id
        context['dar_baja'] = "true"
        return context
    

class TransformacionProductosConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.change_transformacionproductos')
    model = TransformacionProductos
    template_name = "calidad/transformacion_productos/boton.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
            context = {}
            error_series_entrada = False
            error_series_salida = False
            context['titulo'] = 'Error de guardar'
            detalles_entrada = self.get_object().EntradaTransformacionProductos_transformacion_productos.all()
            for detalle in detalles_entrada:
                if detalle.material.control_serie and detalle.transformacion_productos.tipo_stock.serie_registrada:
                    if detalle.series_validar != detalle.cantidad:
                        error_series_entrada = True
            
            detalles_salida = self.get_object().SalidaTransformacionProductos_transformacion_productos.all()
            for detalle in detalles_salida:
                if detalle.material.control_serie and detalle.transformacion_productos.tipo_stock.serie_registrada:
                    if detalle.series_validar != detalle.cantidad:
                        error_series_salida = True

            if error_series_entrada: 
                context['texto'] = 'La cantidad de series de ENTRADA no coincide.'
                return render(request, 'includes/modal sin permiso.html', context)

            if error_series_salida:
                context['texto'] = 'La cantidad de series de SALIDA no coincide.'
                return render(request, 'includes/modal sin permiso.html', context)

            if len(detalles_entrada) == 0:
                context['texto'] = 'Debe agregar al menos un item en la tabla de ENTRADA.'
                return render(request, 'includes/modal sin permiso.html', context)
            
            if len(detalles_salida) == 0:
                context['texto'] = 'Debe agregar al menos un item en la tabla de SALIDA.'
                return render(request, 'includes/modal sin permiso.html', context)
            
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('calidad_app:transformacion_productos_inicio')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()

            tipo_movimiento = TipoMovimiento.objects.get(codigo=161) # Transformación, material transformado
            
            ## TRANSFORMACION - ENTRADA DE MATERIALES
            for detalle in self.object.EntradaTransformacionProductos_transformacion_productos.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = self.object.tipo_stock,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = detalle.transformacion_productos.content_type,
                    id_registro_documento_proceso = detalle.transformacion_productos.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.transformacion_productos.sociedad,
                    movimiento_anterior = None,
                    created_by = request.user,
                    updated_by = request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = tipo_movimiento.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = detalle.transformacion_productos.content_type,
                    id_registro_documento_proceso = detalle.transformacion_productos.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.transformacion_productos.sociedad,
                    movimiento_anterior = movimiento_uno,
                    created_by = request.user,
                    updated_by = request.user,
                )

                for serie in detalle.ValidarSerieEntradaTransformacionProductos_entrada_transformacion_productos.all():
                    HistorialEstadoSerie.objects.create(
                        serie=serie.serie,
                        estado_serie=EstadoSerie.objects.get(numero_estado=11), # Transformado
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    serie.serie.serie_movimiento_almacen.add(movimiento_uno)
                    serie.serie.serie_movimiento_almacen.add(movimiento_dos)        

            ## TRANSFORMACION - SALIDA DE MATERIALES
            if self.object.tipo_stock.codigo == 3: 
                numero_estado = 1 # Disponible
            elif self.object.tipo_stock.codigo == 6:
                numero_estado = 2 # Con problemas
            elif self.object.tipo_stock.codigo == 36:
                numero_estado = 5 # Reparado
            else:
                numero_estado = 11 # Transformado

            for detalle in self.object.SalidaTransformacionProductos_transformacion_productos.all():
                movimiento_tres = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.material.content_type,
                    id_registro_producto = detalle.material.id,
                    cantidad = detalle.cantidad,
                    tipo_movimiento = tipo_movimiento,
                    tipo_stock = self.object.tipo_stock,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = detalle.transformacion_productos.content_type,
                    id_registro_documento_proceso = detalle.transformacion_productos.id,
                    almacen = detalle.almacen,
                    sociedad = detalle.transformacion_productos.sociedad,
                    movimiento_anterior = None,
                    transformacion = True,
                    created_by = request.user,
                    updated_by = request.user,
                )

                for serie in detalle.ValidarSerieSalidaTransformacionProductos_salida_transformacion_productos.all():
                    HistorialEstadoSerie.objects.create(
                        serie=serie.serie,
                        estado_serie=EstadoSerie.objects.get(numero_estado=numero_estado), # Depende del tipo de stock del documento
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    serie.serie.serie_movimiento_almacen.add(movimiento_tres)                  

            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONCLUIR_TRANSFORMACION_PRODUCTOS)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TransformacionProductosConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Transformación Productos"
        context['dar_baja'] = "true"
        return context


class TransformacionProductosDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('calidad.view_transformacionproductos')

    model = TransformacionProductos
    template_name = "calidad/transformacion_productos/detalle.html"
    context_object_name = 'contexto_transformacion_productos_detalle'

    def get_context_data(self, **kwargs):
        transformacion_productos = TransformacionProductos.objects.get(id = self.kwargs['pk'])
        context = super(TransformacionProductosDetailView, self).get_context_data(**kwargs)
        context['entrada_transformacion_productos'] = EntradaTransformacionProductos.objects.filter(transformacion_productos = transformacion_productos)
        context['salida_transformacion_productos'] = SalidaTransformacionProductos.objects.filter(transformacion_productos = transformacion_productos)
        return context


def TransformacionProductosDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/transformacion_productos/detalle_tabla.html'
        context = {}
        transformacion_productos = TransformacionProductos.objects.get(id = pk)
        context['contexto_transformacion_productos_detalle'] = transformacion_productos
        context['entrada_transformacion_productos'] = EntradaTransformacionProductos.objects.filter(transformacion_productos = transformacion_productos)
        context['salida_transformacion_productos'] = SalidaTransformacionProductos.objects.filter(transformacion_productos = transformacion_productos)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class EntradaTransformacionProductosCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.view_entradatransformacionproductos')
    template_name = "calidad/transformacion_productos/form_material.html"
    form_class = EntradaTransformacionProductosForm
    success_url = reverse_lazy('calidad_app:transformacion_productos_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                transformacion_productos = TransformacionProductos.objects.get(id=self.kwargs['transformacion_productos_id'])
                item = len(EntradaTransformacionProductos.objects.filter(transformacion_productos = transformacion_productos))

                material = form.cleaned_data.get('material')
                sede = form.cleaned_data.get('sede')
                almacen = form.cleaned_data.get('almacen')
                tipo_stock = form.cleaned_data.get('tipo_stock')
                cantidad = form.cleaned_data.get('cantidad')

                mensaje = f"material: {material}"
                messages.info(self.request, mensaje)
                mensaje = f"sede: {sede}"
                messages.info(self.request, mensaje)
                mensaje = f"almacen: {almacen}"
                messages.info(self.request, mensaje)
                mensaje = f"tipo_stock: {tipo_stock}"
                messages.info(self.request, mensaje)
                mensaje = f"cantidad: {cantidad}"
                messages.info(self.request, mensaje)

                mensaje = f"{material} | {sede} | {almacen} | {tipo_stock} | {cantidad}"
                messages.info(self.request, mensaje)

                if Decimal(cantidad) > stock_tipo_stock(material.content_type, material.id, transformacion_productos.sociedad.id, almacen.id, tipo_stock.id):
                    form.add_error('cantidad', "Se excedió la cantidad del stock")
                    return super().form_invalid(form)

                obj, created = EntradaTransformacionProductos.objects.get_or_create(
                    material = material,
                    sede = sede,
                    almacen = almacen,
                    # tipo_stock = tipo_stock,
                    transformacion_productos = transformacion_productos,
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

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EntradaTransformacionProductosCreateView, self).get_form_kwargs(*args, **kwargs)
        transformacion_productos = TransformacionProductos.objects.get(id=self.kwargs['transformacion_productos_id'])
        kwargs['tipo_stock'] = transformacion_productos.tipo_stock
        kwargs['id_sociedad'] = transformacion_productos.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(EntradaTransformacionProductosCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        context['url_sede'] = reverse_lazy('logistica_app:almacen', kwargs={'id_sede':1})[:-2]
        transformacion_productos = TransformacionProductos.objects.get(id=self.kwargs['transformacion_productos_id'])
        context['sociedad'] = transformacion_productos.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        return context
    

class EntradaTransformacionProductosUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_transformacionproductosdetalle')
    model = EntradaTransformacionProductos
    template_name = "calidad/transformacion_productos/form_material.html"
    form_class = EntradaTransformacionProductosForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:transformacion_productos_detalle', kwargs={'pk':self.get_object().transformacion_productos_id})

    def form_valid(self, form):
        cantidad = form.cleaned_data.get('cantidad')
        material = form.cleaned_data.get('material')
        almacen = form.cleaned_data.get('almacen')
        tipo_stock = form.cleaned_data.get('tipo_stock')
        if Decimal(cantidad) > stock_tipo_stock(material.content_type, material.id, self.get_object().transformacion_productos.sociedad.id, almacen.id, tipo_stock.id):
            form.add_error('cantidad', "Se excedió la cantidad del stock")
            return super().form_invalid(form)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EntradaTransformacionProductosUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['tipo_stock'] = self.object.transformacion_productos.tipo_stock
        kwargs['id_sociedad'] = self.object.transformacion_productos.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EntradaTransformacionProductosUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        context['url_sede'] = reverse_lazy('logistica_app:almacen', kwargs={'id_sede':1})[:-2]
        transformacion_productos = TransformacionProductos.objects.get(id=self.get_object().transformacion_productos_id)
        context['sociedad'] = transformacion_productos.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        return context


class EntradaTransformacionProductosDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_transformacionproductosdetalle')
    model = EntradaTransformacionProductos
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:transformacion_productos_detalle', kwargs={'pk': self.get_object().transformacion_productos_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = EntradaTransformacionProductos.objects.filter(transformacion_productos=self.get_object().transformacion_productos)
            contador = 1
            for material in materiales:
                if material == self.get_object(): continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super(EntradaTransformacionProductosDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context


class ValidarSeriesEntradaTransformacionProductosDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('calidad.view_entradatransformacionproductos')
    template_name = "calidad/transformacion_productos/validar_serie_entrada/detalle.html"
    form_class = EntradaTransformacionProductosSeriesForm
    success_url = '.'

    def form_valid(self, form):
        # if self.request.session['primero']:
        serie = form.cleaned_data['serie']
        entrada_transformacion_productos = EntradaTransformacionProductos.objects.get(id = self.kwargs['pk'])
        try:
            buscar = Serie.objects.get(
                serie_base=serie,
                content_type=ContentType.objects.get_for_model(entrada_transformacion_productos.material),
                id_registro=entrada_transformacion_productos.material.id,
            )
            buscar2 = ValidarSerieEntradaTransformacionProductos.objects.filter(serie = buscar)

            if len(buscar2) != 0:
                form.add_error('serie', "Serie ya ha sido registrada")
                return super().form_invalid(form)

            if buscar.ultimo_movimiento.tipo_stock != entrada_transformacion_productos.transformacion_productos.tipo_stock:
                form.add_error('serie', "Serie INVÁLIDA, su estado es: %s" % buscar.estado)
                return super().form_invalid(form)
                
        except Exception as e:
            # print(e)
            form.add_error('serie', "Serie no encontrada: %s" % serie)
            return super().form_invalid(form)

        obj, created = ValidarSerieEntradaTransformacionProductos.objects.get_or_create(
            entrada_transformacion_productos=entrada_transformacion_productos,
            serie=buscar,
        )
        if created:
            obj.estado = 1
        # self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        entrada_transformacion_productos = EntradaTransformacionProductos.objects.get(id = self.kwargs['pk'])
        cantidad = entrada_transformacion_productos.cantidad
        cantidad_ingresada = len(ValidarSerieEntradaTransformacionProductos.objects.filter(entrada_transformacion_productos=entrada_transformacion_productos))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad'] = cantidad
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        # self.request.session['primero'] = True
        entrada_transformacion_productos = EntradaTransformacionProductos.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesEntradaTransformacionProductosDetailView, self).get_context_data(**kwargs)
        context['contexto_entrada_transformacion_productos'] = entrada_transformacion_productos
        context['contexto_series'] = ValidarSerieEntradaTransformacionProductos.objects.filter(entrada_transformacion_productos = entrada_transformacion_productos)
        return context


def ValidarSeriesEntradaTransformacionProductosDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/transformacion_productos/validar_serie_entrada/detalle_tabla.html'
        context = {}
        entrada_transformacion_productos = EntradaTransformacionProductos.objects.get(id = pk)
        context['contexto_entrada_transformacion_productos'] = entrada_transformacion_productos
        context['contexto_series'] = ValidarSerieEntradaTransformacionProductos.objects.filter(entrada_transformacion_productos = entrada_transformacion_productos)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesEntradaTransformacionProductosDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_validarserieentradatransformacionproductos')
    model = ValidarSerieEntradaTransformacionProductos
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:entrada_transformacion_productos_validar_series_detalle', kwargs={'pk': self.get_object().entrada_transformacion_productos.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesEntradaTransformacionProductosDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context
    

class SalidaTransformacionProductosCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.view_salidatransformacionproductos')
    template_name = "calidad/transformacion_productos/form_material.html"
    form_class = SalidaTransformacionProductosForm
    success_url = reverse_lazy('calidad_app:transformacion_productos_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                transformacion_productos = TransformacionProductos.objects.get(id=self.kwargs['transformacion_productos_id'])
                item = len(SalidaTransformacionProductos.objects.filter(transformacion_productos = transformacion_productos))

                material = form.cleaned_data.get('material')
                sede = form.cleaned_data.get('sede')
                almacen = form.cleaned_data.get('almacen')
                # tipo_stock = form.cleaned_data.get('tipo_stock')
                cantidad = form.cleaned_data.get('cantidad')

                obj, created = SalidaTransformacionProductos.objects.get_or_create(
                    material = material,
                    sede = sede,
                    almacen = almacen,
                    # tipo_stock = tipo_stock,
                    transformacion_productos = transformacion_productos,
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

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SalidaTransformacionProductosCreateView, self).get_form_kwargs(*args, **kwargs)
        transformacion_productos = TransformacionProductos.objects.get(id=self.kwargs['transformacion_productos_id'])
        kwargs['tipo_stock'] = transformacion_productos.tipo_stock
        kwargs['id_sociedad'] = transformacion_productos.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(SalidaTransformacionProductosCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        context['url_sede'] = reverse_lazy('logistica_app:almacen', kwargs={'id_sede':1})[:-2]
        transformacion_productos = TransformacionProductos.objects.get(id=self.kwargs['transformacion_productos_id'])
        context['sociedad'] = transformacion_productos.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        return context
    

class SalidaTransformacionProductosUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_transformacionproductosdetalle')
    model = SalidaTransformacionProductos
    template_name = "calidad/transformacion_productos/form_material.html"
    form_class = SalidaTransformacionProductosForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:transformacion_productos_detalle', kwargs={'pk':self.get_object().transformacion_productos_id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SalidaTransformacionProductosUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['tipo_stock'] = self.object.transformacion_productos.tipo_stock
        kwargs['id_sociedad'] = self.object.transformacion_productos.sociedad.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SalidaTransformacionProductosUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        context['url_sede'] = reverse_lazy('logistica_app:almacen', kwargs={'id_sede':1})[:-2]
        transformacion_productos = TransformacionProductos.objects.get(id=self.get_object().transformacion_productos_id)
        context['sociedad'] = transformacion_productos.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        return context


class SalidaTransformacionProductosDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_transformacionproductosdetalle')
    model = SalidaTransformacionProductos
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:transformacion_productos_detalle', kwargs={'pk': self.get_object().transformacion_productos_id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = SalidaTransformacionProductos.objects.filter(transformacion_productos=self.get_object().transformacion_productos)
            contador = 1
            for material in materiales:
                if material == self.get_object(): continue
                material.item = contador
                material.save()
                contador += 1
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SalidaTransformacionProductosDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        context['dar_baja'] = "true"
        return context
    

class ValidarSeriesSalidaTransformacionProductosDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('calidad.view_salidatransformacionproductos')
    template_name = "calidad/transformacion_productos/validar_serie_salida/detalle.html"
    form_class = SalidaTransformacionProductosSeriesForm
    success_url = '.'

    def form_valid(self, form):
        # if self.request.session['primero']:
        serie = form.cleaned_data['serie']
        salida_transformacion_productos = SalidaTransformacionProductos.objects.get(id = self.kwargs['pk'])
        try:
            buscar = Serie.objects.filter(
                serie_base=serie,
                content_type=ContentType.objects.get_for_model(salida_transformacion_productos.material),
                id_registro=salida_transformacion_productos.material.id,
            )

            if len(buscar) == 0:
                nueva_serie = Serie.objects.create(
                    serie_base=serie,
                    content_type=salida_transformacion_productos.material.content_type,
                    id_registro=salida_transformacion_productos.material.id,
                    sociedad=salida_transformacion_productos.transformacion_productos.sociedad,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )    
            else:
                buscar2 = ValidarSerieSalidaTransformacionProductos.objects.filter(serie = buscar[0])
                if len(buscar2) != 0:
                    form.add_error('serie', "Serie ya ha sido ingresada")
                    return super().form_invalid(form)
                
                form.add_error('serie', "Serie ya ha sido registrada")
                return super().form_invalid(form)

        except Exception as e:
            form.add_error('serie', "Ocurrió un problema con la serie: %s, %s" % (serie, e) )
            return super().form_invalid(form)

        obj, created = ValidarSerieSalidaTransformacionProductos.objects.get_or_create(
            salida_transformacion_productos=salida_transformacion_productos,
            serie=nueva_serie,
        )
        if created:
            obj.estado = 1
        # self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        salida_transformacion_productos = SalidaTransformacionProductos.objects.get(id = self.kwargs['pk'])
        cantidad = salida_transformacion_productos.cantidad
        cantidad_ingresada = len(ValidarSerieSalidaTransformacionProductos.objects.filter(salida_transformacion_productos=salida_transformacion_productos))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad'] = cantidad
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        # self.request.session['primero'] = True
        salida_transformacion_productos = SalidaTransformacionProductos.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesSalidaTransformacionProductosDetailView, self).get_context_data(**kwargs)
        context['contexto_salida_transformacion_productos'] = salida_transformacion_productos
        context['contexto_series'] = ValidarSerieSalidaTransformacionProductos.objects.filter(salida_transformacion_productos = salida_transformacion_productos)
        return context


def ValidarSeriesSalidaTransformacionProductosDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/transformacion_productos/validar_serie_salida/detalle_tabla.html'
        context = {}
        salida_transformacion_productos = SalidaTransformacionProductos.objects.get(id = pk)
        context['contexto_salida_transformacion_productos'] = salida_transformacion_productos
        context['contexto_series'] = ValidarSerieSalidaTransformacionProductos.objects.filter(salida_transformacion_productos = salida_transformacion_productos)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesSalidaTransformacionProductosDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('calidad.delete_validarseriesalidatransformacionproductos')
    model = ValidarSerieSalidaTransformacionProductos
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:salida_transformacion_productos_validar_series_detalle', kwargs={'pk': self.get_object().salida_transformacion_productos.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesSalidaTransformacionProductosDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context