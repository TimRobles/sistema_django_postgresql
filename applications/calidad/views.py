from urllib import request
from django.core.paginator import Paginator
from django.shortcuts import render
from applications.importaciones import*
from applications.material.models import SubFamilia
from applications.calidad.forms import(
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
    NotaControlCalidadStockAgregarMaloSinSerieCreateForm,
    SerieBuscarForm,
)
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from .models import(
    EstadoSerie,
    NotaControlCalidadStock,
    NotaControlCalidadStockDetalle,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
    SerieCalidad,
)
from applications.funciones import numeroXn, registrar_excepcion

class FallaMaterialTemplateView(PermissionRequiredMixin, TemplateView):
    permission_required = ('calidad.view_fallamaterial')
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
    template_name = "includes/formulario generico.html"
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
                    elif detalle.nota_ingreso_detalle.comprobante_compra_detalle.producto.control_serie:
                        movimiento_final = TipoMovimiento.objects.get(codigo=106) #Inspección, material bueno, sin registrar serie
                    else:
                        movimiento_final = TipoMovimiento.objects.get(codigo=107) #Inspección, material bueno, no requiere serie

                    movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                        id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso = form.instance.id,
                        almacen = detalle.nota_ingreso_detalle.almacen,
                        sociedad = form.instance.nota_ingreso.recepcion_compra.sociedad,
                    )
                    movimiento_uno = movimiento_dos.movimiento_anterior
                    
                    movimiento_dos.delete()
                    movimiento_uno.delete()
            elif form.instance.estado == 3:
                detalles = form.instance.NotaControlCalidadStockDetalle_nota_control_calidad_stock.all()
                for detalle in detalles:
                    if detalle.inspeccion == 2:
                        movimiento_final = TipoMovimiento.objects.get(codigo=141) #Registro de Serie, material dañado
                    elif detalle.nota_ingreso_detalle.comprobante_compra_detalle.producto.control_serie:
                        movimiento_final = TipoMovimiento.objects.get(codigo=108) #Registro de Serie

                    movimiento_dos = MovimientosAlmacen.objects.get(
                        content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                        id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                        id_registro_documento_proceso = form.instance.id,
                        almacen = detalle.nota_ingreso_detalle.almacen,
                        sociedad = form.instance.nota_ingreso.recepcion_compra.sociedad,
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
                if detalle.nota_ingreso_detalle.comprobante_compra_detalle.producto.control_calidad:
                    if detalle.inspeccion == 1:
                        if detalle.nota_ingreso_detalle.comprobante_compra_detalle.producto.control_serie:
                            movimiento_inicial = TipoMovimiento.objects.get(codigo=106) #Inspección, material bueno, sin registrar serie
                            movimiento_final = TipoMovimiento.objects.get(codigo=108) #Registro de Serie
                        else:
                            continue
                    else:
                        print("Producto malo")
                        movimiento_inicial = TipoMovimiento.objects.get(codigo=105) #Inspección, material dañado
                        movimiento_final = TipoMovimiento.objects.get(codigo=141) #Registro de Serie, material dañado

                    movimiento_anterior = MovimientosAlmacen.objects.get(
                        content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                        id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                        tipo_movimiento = movimiento_inicial,
                        tipo_stock = movimiento_inicial.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso = self.object.id,
                        almacen = detalle.nota_ingreso_detalle.almacen,
                        sociedad = self.object.nota_ingreso.recepcion_compra.sociedad,
                        movimiento_reversion = False,
                    )

                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                        id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador = -1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso = self.object.id,
                        almacen = movimiento_anterior.almacen,
                        sociedad = self.object.nota_ingreso.recepcion_compra.sociedad,
                        movimiento_anterior = movimiento_anterior,
                        movimiento_reversion = False,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                        id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                        cantidad = detalle.cantidad_calidad,
                        tipo_movimiento = movimiento_final,
                        tipo_stock = movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador = +1,
                        content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso = self.object.id,
                        almacen = movimiento_anterior.almacen,
                        sociedad = self.object.nota_ingreso.recepcion_compra.sociedad,
                        movimiento_anterior = movimiento_uno,
                        movimiento_reversion = False,
                        created_by = self.request.user,
                        updated_by = self.request.user,
                    )

                    for serie_calidad in detalle.SerieCalidad_nota_control_calidad_stock_detalle.all():
                        serie = Serie.objects.create(
                            serie_base = serie_calidad.serie,
                            content_type = serie_calidad.content_type,
                            id_registro = serie_calidad.id_registro,
                            sociedad = serie_calidad.nota_control_calidad_stock_detalle.nota_ingreso_detalle.comprobante_compra_detalle.sociedad,
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
            if ContentType.objects.get_for_model(self.object.nota_ingreso) == ContentType.objects.get_for_model(NotaIngreso):
                movimiento_inicial = TipoMovimiento.objects.get(codigo=104) #Ingreso por compra, c/QA
            else:
                movimiento_inicial = TipoMovimiento.objects.get(codigo=999) #Stock inicial
            
            finalizar = True
            for detalle in detalles:
                if detalle.inspeccion == 2:
                    movimiento_final = TipoMovimiento.objects.get(codigo=105) #Inspección, material dañado
                    finalizar &= False
                elif detalle.nota_ingreso_detalle.comprobante_compra_detalle.producto.control_serie:
                    movimiento_final = TipoMovimiento.objects.get(codigo=106) #Inspección, material bueno, sin registrar serie
                    finalizar &= False
                else:
                    movimiento_final = TipoMovimiento.objects.get(codigo=107) #Inspección, material bueno, no requiere serie

                movimiento_anterior = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    tipo_movimiento = movimiento_inicial,
                    tipo_stock = movimiento_inicial.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object.nota_ingreso),
                    id_registro_documento_proceso = self.object.nota_ingreso.id,
                    sociedad = self.object.nota_ingreso.recepcion_compra.sociedad,
                    almacen = detalle.nota_ingreso_detalle.almacen,
                    movimiento_reversion = False,
                )

                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad_calidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador = -1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = movimiento_anterior.almacen,
                    sociedad = self.object.nota_ingreso.recepcion_compra.sociedad,
                    movimiento_anterior = movimiento_anterior,
                    movimiento_reversion = False,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad_calidad,
                    tipo_movimiento = movimiento_final,
                    tipo_stock = movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso = self.object.id,
                    almacen = movimiento_anterior.almacen,
                    sociedad = self.object.nota_ingreso.recepcion_compra.sociedad,
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
                cantidad_calidad = form.cleaned_data.get('cantidad_calidad')
                inspeccion = form.cleaned_data.get('inspeccion')
                
                buscar = NotaControlCalidadStockDetalle.objects.filter(
                    nota_ingreso_detalle=nota_ingreso_detalle,
                ).exclude(nota_control_calidad_stock__estado=4)
                
                if buscar:
                    contar = buscar.aggregate(Sum('cantidad_calidad'))['cantidad_calidad__sum']
                else:
                    contar = 0

                
                if nota_ingreso_detalle.cantidad_conteo < contar + cantidad_calidad:
                    form.add_error('cantidad_calidad', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (nota_ingreso_detalle.cantidad_conteo, contar + cantidad_calidad))
                    return super().form_invalid(form)

                obj, created = NotaControlCalidadStockDetalle.objects.get_or_create(
                    nota_ingreso_detalle = nota_ingreso_detalle,
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
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        nota_control_calidad = NotaControlCalidadStock.objects.get(id = self.kwargs['nota_control_calidad_stock_id'])
        nota_ingreso = nota_control_calidad.nota_ingreso
        materiales = NotaIngresoDetalle.objects.filter(nota_ingreso = nota_ingreso)
        materiales_sin_calidad = []
        for material in materiales:
            if not material.comprobante_compra_detalle.producto.control_calidad:
                materiales_sin_calidad.append(material.id)
        materiales = materiales.exclude(id__in = materiales_sin_calidad)

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:nota_control_calidad_stock_detalle', kwargs={'pk':self.get_object().nota_control_calidad_stock_id})

    def form_valid(self, form):
        nota_ingreso_detalle = form.instance.nota_ingreso_detalle

        buscar = NotaControlCalidadStockDetalle.objects.filter(
            nota_ingreso_detalle=nota_ingreso_detalle,
            inspeccion=form.instance.inspeccion,
            nota_control_calidad_stock=form.instance.nota_control_calidad_stock,
        ).exclude(id=form.instance.id)

        if len(buscar) > 0:
            form.add_error('inspeccion', f'Ya existe un producto como {form.instance.get_inspeccion_display()}')
            return super().form_invalid(form)

        buscar = NotaControlCalidadStockDetalle.objects.filter(
            nota_ingreso_detalle=nota_ingreso_detalle,
        ).exclude(id=form.instance.id).exclude(nota_control_calidad_stock__estado=4)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_calidad'))['cantidad_calidad__sum']
        else:
            contar = 0

        if nota_ingreso_detalle.cantidad_conteo < contar + form.instance.cantidad_calidad:
            form.add_error('cantidad_calidad', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (nota_ingreso_detalle.cantidad_conteo, contar + form.instance.cantidad_calidad))
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
            buscar_serie = Serie.objects.filter(serie_base = serie)
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

