from django.shortcuts import render
from django import forms
from applications.calidad.models import Serie
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.datos_globales.models import SeriesComprobante, Unidad
from applications.funciones import numeroXn, registrar_excepcion
from applications.importaciones import *
from applications.logistica.pdf import generarSeries
from applications.material.funciones import stock, ver_tipo_stock
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from applications.sociedad.models import Sociedad

from .models import (
    EnvioTrasladoProducto,
    EnvioTrasladoProductoDetalle,
    MotivoTraslado,
    RecepcionTrasladoProducto,
    RecepcionTrasladoProductoDetalle,
    ValidarSerieEnvioTrasladoProductoDetalle,
    TraspasoStock,
    TraspasoStockDetalle,
    ValidarSerieTraspasoStockDetalle,
)

from .forms import (
    EnvioTrasladoProductoDetalleSeriesForm,
    EnvioTrasladoProductoForm,
    EnvioTrasladoProductoMaterialDetalleForm,
    EnvioTrasladoProductoObservacionesForm,
    EnvioTrasladoProductoMaterialActualizarDetalleForm,
    MotivoTrasladoForm,
    RecepcionTrasladoProductoActualizarForm,
    RecepcionTrasladoProductoForm,
    RecepcionTrasladoProductoObservacionesForm,
    RecepcionTrasladoProductoMaterialDetalleForm,
    RecepcionTrasladoProductoMaterialActualizarDetalleForm,
    TraspasoStockDetalleActualizarForm,
    TraspasoStockDetalleForm,
    TraspasoStockDetalleSeriesForm,
    TraspasoStockForm,
)


class EnvioTrasladoProductoListView(PermissionRequiredMixin, ListView):
    permission_required = ('traslado_producto.view_enviotrasladoproducto')
    model = EnvioTrasladoProducto
    template_name = "traslado_producto/envio/inicio.html"
    context_object_name = 'contexto_envio_traslado_producto'

def EnvioTrasladoProductoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/envio/inicio_tabla.html'
        context = {}
        context['contexto_envio_traslado_producto'] = EnvioTrasladoProducto.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

def EnvioTrasladoProductoCrearView(request):
    obj = EnvioTrasladoProducto.objects.create(
        created_by=request.user,
        updated_by=request.user,
    )
    obj.save()
    return HttpResponseRedirect(reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':obj.id}))

class EnvioTrasladoProductoVerView(PermissionRequiredMixin, TemplateView):
    permission_required = ('traslado_producto.view_enviotrasladoproducto')
    template_name = "traslado_producto/envio/detalle.html"

    def get_context_data(self, **kwargs):
        obj = EnvioTrasladoProducto.objects.get(id = kwargs['id_envio_traslado_producto'])
        sociedades = Sociedad.objects.filter(estado_sunat=1)

        materiales = None
        try:
            materiales = obj.EnvioTrasladoProductoDetalle_envio_traslado_producto.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = super(EnvioTrasladoProductoVerView, self).get_context_data(**kwargs)
        context['envio_traslado_producto'] = obj
        context['sociedades'] = sociedades
        context['materiales'] = materiales
        context['accion'] = "Crear"
        context['titulo'] = "Envio Traslado"
        return context

def EnvioTrasladoProductoVerTabla(request, id_envio_traslado_producto):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/envio/detalle_tabla.html'
        obj = EnvioTrasladoProducto.objects.get(id = id_envio_traslado_producto)

        materiales = None
        try:
            materiales = obj.EnvioTrasladoProductoDetalle_envio_traslado_producto.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except Exception as e:
            pass

        sociedades = Sociedad.objects.filter(estado_sunat=1)

        context = {}
        context['envio_traslado_producto'] = obj
        context['sociedades'] = sociedades
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class EnvioTrasladoProductoSeriesPdf(View):
    def get(self, request, *args, **kwargs):
        obj = EnvioTrasladoProducto.objects.get(id=self.kwargs['pk'])

        color = obj.sociedad.color
        titulo = 'SERIES DE EQUIPOS'
        vertical = True
        logo = [obj.sociedad.logo.url]
        pie_pagina = obj.sociedad.pie_pagina

        titulo = "%s - %s - %s" % (titulo, numeroXn(obj.numero_envio_traslado, 6), obj.responsable)

        movimientos = MovimientosAlmacen.objects.buscar_movimiento(obj, ContentType.objects.get_for_model(EnvioTrasladoProducto))
        series = Serie.objects.buscar_series(movimientos)
        series_unicas = []
        if series:
            series_unicas = series.order_by('id_registro', 'serie_base').distinct()
        
        texto_cabecera = 'Series trasladadas:'
        
        series_final = {}
        for serie in series_unicas:
            if not serie.producto in series_final:
                series_final[serie.producto] = []
            series_final[serie.producto].append(serie.serie_base)

        TablaEncabezado = ['DOCUMENTOS',
                           'FECHA',
                           'MOTIVO DEL TRASLADO',
                           'OBSERVACIONES',
                           ]

        TablaDatos = []
        TablaDatos.append(f"TRASLADO {numeroXn(obj.numero_envio_traslado, 6)} - {obj.responsable}")
        TablaDatos.append(obj.fecha.strftime('%d/%m/%Y'))
        TablaDatos.append(obj.motivo_traslado)
        TablaDatos.append(obj.observaciones)

        buf = generarSeries(titulo, vertical, logo, pie_pagina, texto_cabecera, TablaEncabezado, TablaDatos, series_final, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition'] = 'inline; filename=%s.pdf' % titulo

        return respuesta


class  EnvioTrasladoProductoActualizarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_enviotrasladoproducto')
    model = EnvioTrasladoProducto
    template_name = "traslado_producto/envio/form_actualizar.html"
    form_class = EnvioTrasladoProductoForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.object.id})

    def form_valid(self, form):
        envio_traslado_producto = EnvioTrasladoProducto.objects.get(id=form.instance.id)
        if form.instance.sede_origen != envio_traslado_producto.sede_origen or form.instance.sociedad != envio_traslado_producto.sociedad:
            for detalle in form.instance.EnvioTrasladoProductoDetalle_envio_traslado_producto.all():
                detalle.almacen_origen = None
                registro_guardar(detalle, self.request)
                detalle.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoActualizarView, self).get_context_data(**kwargs)
        context['accion'] = "Envio"
        context['titulo'] = "Traslado Producto"
        context['url_sede'] = reverse_lazy('sociedad_app:sociedad_sede', kwargs={'id_sociedad':1})[:-2]
        return context

class EnvioTrasladoProductoGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.change_enviotrasladoproducto')
    model = EnvioTrasladoProducto
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cantidad_series = False
        error_almacen_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().EnvioTrasladoProductoDetalle_envio_traslado_producto.all()
        for detalle in detalles:
            for validar_serie in detalle.ValidarSerieEnvioTrasladoProductoDetalle_envio_traslado_producto_detalle.all():
                if detalle.control_serie and detalle.almacen_origen != validar_serie.serie.almacen:
                    error_almacen_series = True
            if detalle.control_serie and detalle.series_validar != detalle.cantidad_envio:
                error_cantidad_series = True
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_cantidad_series:
            context['texto'] = 'Hay Series sin registrar.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_almacen_series:
            context['texto'] = 'Hay errores en los almacenes de las series.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            movimiento_final = TipoMovimiento.objects.get(codigo=139)  # Salida por traslado
            for detalle in self.object.EnvioTrasladoProductoDetalle_envio_traslado_producto.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_envio,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=detalle.tipo_stock,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen_origen,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=None,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_envio,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_uno,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                for validar in detalle.ValidarSerieEnvioTrasladoProductoDetalle_envio_traslado_producto_detalle.all():
                    validar.serie.serie_movimiento_almacen.add(movimiento_uno)
                    validar.serie.serie_movimiento_almacen.add(movimiento_dos)

            numero_envio_traslado = EnvioTrasladoProducto.objects.all().aggregate(Count('numero_envio_traslado'))['numero_envio_traslado__count'] + 1
            self.object.numero_envio_traslado = numero_envio_traslado
            self.object.estado = 2
            self.object.fecha_traslado = datetime.now()

            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_GUARDAR_ENVIO)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Envio"
        context['dar_baja'] = True
        return context

class  EnvioTrasladoProductoObservacionesView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_enviotrasladoproducto')
    model = EnvioTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = EnvioTrasladoProductoObservacionesForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoObservacionesView, self).get_context_data(**kwargs)
        context['accion'] = "Observaciones"
        return context


class EnvioTrasladoProductoMaterialDetalleView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('traslado_producto.change_enviotrasladoproducto')
    template_name = "traslado_producto/envio/form_material.html"
    form_class = EnvioTrasladoProductoMaterialDetalleForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_sede = False
        context['titulo'] = 'Error de guardar'
        envio_traslado_producto = EnvioTrasladoProducto.objects.get(id = self.kwargs['id_envio_traslado_producto'])
        if not envio_traslado_producto.sede_origen:
            error_sede = True

        if error_sede:
            context['texto'] = 'Ingrese una sede de origen.'
            return render(request, 'includes/modal sin permiso.html', context)
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.kwargs['id_envio_traslado_producto']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        envio_traslado_producto = EnvioTrasladoProducto.objects.get(id = self.kwargs['id_envio_traslado_producto'])
        almacen_origen = form.cleaned_data.get('almacen_origen')
        tipo_stock = form.cleaned_data.get('tipo_stock')
        material = form.cleaned_data.get('material')
        cantidad_envio = form.cleaned_data.get('cantidad_envio')
        stock_disponible = ver_tipo_stock(ContentType.objects.get_for_model(material), material.id, envio_traslado_producto.sociedad.id, almacen_origen.id, tipo_stock.id)

        buscar = EnvioTrasladoProductoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
            almacen_origen=almacen_origen,
            tipo_stock=tipo_stock,
            envio_traslado_producto=envio_traslado_producto,
        ).exclude(envio_traslado_producto__estado=4)

        print(buscar)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_envio'))['cantidad_envio__sum']
        else:
            contar = 0
        
        print(stock_disponible)
        print(contar)
        print(cantidad_envio)

        if stock_disponible < contar + cantidad_envio:
            form.add_error('cantidad_envio', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (stock_disponible, contar + cantidad_envio))
            return super().form_invalid(form)

        try:
            if self.request.session['primero']:
                item = len(EnvioTrasladoProductoDetalle.objects.filter(envio_traslado_producto = envio_traslado_producto))

                obj, created = EnvioTrasladoProductoDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    envio_traslado_producto = envio_traslado_producto,
                    almacen_origen = almacen_origen,
                    tipo_stock = tipo_stock,
                    unidad = form.cleaned_data.get('unidad')
                )
                if created:
                    obj.item = item + 1
                    obj.cantidad_envio = cantidad_envio

                else:
                    obj.cantidad_envio = obj.cantidad_envio + cantidad_envio

                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero']=False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        envio_traslado_producto = EnvioTrasladoProducto.objects.get(id = self.kwargs['id_envio_traslado_producto'])
        kwargs['envio_traslado_producto'] = envio_traslado_producto
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        envio_traslado_producto = EnvioTrasladoProducto.objects.get(id = self.kwargs['id_envio_traslado_producto'])
        context = super(EnvioTrasladoProductoMaterialDetalleView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Material'
        context['sociedad'] = envio_traslado_producto.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context

class  EnvioTrasladoProductoActualizarMaterialDetalleView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_enviotrasladoproducto')
    model = EnvioTrasladoProductoDetalle
    template_name = "traslado_producto/envio/form_actualizar_material.html"
    form_class = EnvioTrasladoProductoMaterialActualizarDetalleForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_sede = False
        context['titulo'] = 'Error de guardar'
        detalle = EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        if not envio_traslado_producto.sede_origen:
            error_sede = True

        if error_sede:
            context['texto'] = 'Ingrese una sede de origen.'
            return render(request, 'includes/modal sin permiso.html', context)
    
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.get_object().envio_traslado_producto.id})

    def get_form_kwargs(self, *args, **kwargs):
        print(self.kwargs)
        detalle = EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        kwargs = super().get_form_kwargs()
        kwargs['envio_traslado_producto'] = envio_traslado_producto
        return kwargs

    def form_valid(self, form):
        detalle = EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        almacen_origen = form.cleaned_data.get('almacen_origen')
        tipo_stock = form.cleaned_data.get('tipo_stock')
        cantidad_envio = form.cleaned_data.get('cantidad_envio')
        material = detalle.producto
        stock_disponible = ver_tipo_stock(ContentType.objects.get_for_model(material), material.id, envio_traslado_producto.sociedad.id, almacen_origen.id, tipo_stock.id)

        buscar = EnvioTrasladoProductoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
            tipo_stock=tipo_stock,
            envio_traslado_producto=envio_traslado_producto,
        ).exclude(envio_traslado_producto__estado=4).exclude(id=detalle.id)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_envio'))['cantidad_envio__sum']
        else:
            contar = 0

        if stock_disponible < contar + cantidad_envio:
            form.add_error('cantidad_envio', 'Se superó la cantidad contada. Máximo: %s. Contado: %s.' % (stock_disponible, contar + cantidad_envio))
            return super().form_invalid(form)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        detalle = EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        context = super(EnvioTrasladoProductoActualizarMaterialDetalleView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Item"
        context['material'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        context['sociedad'] = envio_traslado_producto.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context

class EnvioTrasladoProductoMaterialDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.change_enviotrasladoproducto')
    model = EnvioTrasladoProductoDetalle
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.get_object().envio_traslado_producto.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = EnvioTrasladoProductoDetalle.objects.filter(envio_traslado_producto=self.get_object().envio_traslado_producto)
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
        context = super(EnvioTrasladoProductoMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)

        return context


class EnvioTrasladoProductoGenerarGuiaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('logistica.change_despachodetalle')
    model = EnvioTrasladoProducto
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.kwargs['guia'].id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            detalles = self.object.EnvioTrasladoProductoDetalle_envio_traslado_producto.all()
            serie_comprobante = SeriesComprobante.objects.por_defecto(ContentType.objects.get_for_model(Guia))
            observaciones = []
            observaciones.append('PRESENTACIÓN DE PRODUCTOS')
            if self.object.observaciones:
                observaciones.append(self.object.observaciones)

            guia = Guia.objects.create(
                sociedad=self.object.sociedad,
                serie_comprobante=serie_comprobante,
                motivo_traslado='13',
                observaciones=" | ".join(observaciones),
                created_by=self.request.user,
                updated_by=self.request.user,
            )

            for detalle in detalles:
                guia_detalle = GuiaDetalle.objects.create(
                    item=detalle.item,
                    content_type=detalle.content_type,
                    id_registro=detalle.id_registro,
                    guia=guia,
                    cantidad=detalle.cantidad_envio,
                    unidad=detalle.producto.unidad_base,
                    descripcion_documento=detalle.producto.descripcion_venta,
                    peso=detalle.producto.peso_unidad_base,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
            self.kwargs['guia'] = guia
            self.request.session['primero'] = False
            messages.success(request, MENSAJE_GENERAR_GUIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(EnvioTrasladoProductoGenerarGuiaView, self).get_context_data(**kwargs)
        context['accion'] = "Generar"
        context['titulo'] = "Guía"
        context['dar_baja'] = "true"
        context['item'] = self.get_object()
        return context


class ValidarSeriesEnvioTrasladoProductoDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('traslado_producto.view_enviotrasladoproductodetalle')
    template_name = "traslado_producto/validar_serie_envio_traslado_producto/detalle.html"
    form_class = EnvioTrasladoProductoDetalleSeriesForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session['primero']:
            serie = form.cleaned_data['serie']
            envio_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id = self.kwargs['pk'])
            try:
                buscar = Serie.objects.get(
                    serie_base=serie,
                    content_type=ContentType.objects.get_for_model(envio_traslado_producto_detalle.producto),
                    id_registro=envio_traslado_producto_detalle.producto.id,
                )
                buscar2 = ValidarSerieEnvioTrasladoProductoDetalle.objects.filter(serie = buscar)

                if len(buscar2) != 0:
                    form.add_error('serie', "Serie ya ha sido registrada")
                    return super().form_invalid(form)

                if buscar.ultimo_movimiento.tipo_stock != envio_traslado_producto_detalle.tipo_stock:
                    form.add_error('serie', "La serie no corresponde al tipo de stock: %s" % buscar.ultimo_movimiento.tipo_stock)
                    return super().form_invalid(form)
            except:
                form.add_error('serie', "Serie no encontrada: %s" % serie)
                return super().form_invalid(form)

            envio_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id = self.kwargs['pk'])
            obj, created = ValidarSerieEnvioTrasladoProductoDetalle.objects.get_or_create(
                envio_traslado_producto_detalle=envio_traslado_producto_detalle,
                serie=buscar,
            )
            if created:
                obj.estado = 1
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        envio_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id = self.kwargs['pk'])
        cantidad_envio = envio_traslado_producto_detalle.cantidad_envio
        cantidad_ingresada = len(ValidarSerieEnvioTrasladoProductoDetalle.objects.filter(envio_traslado_producto_detalle=envio_traslado_producto_detalle))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad_envio'] = cantidad_envio
        kwargs['cantidad_ingresada'] = cantidad_ingresada
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        envio_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesEnvioTrasladoProductoDetailView, self).get_context_data(**kwargs)
        context['contexto_envio_traslado_producto_detalle'] = envio_traslado_producto_detalle
        context['contexto_series'] = ValidarSerieEnvioTrasladoProductoDetalle.objects.filter(envio_traslado_producto_detalle = envio_traslado_producto_detalle)
        return context

def ValidarSeriesEnvioTrasladoProductoDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/validar_serie_envio_traslado_producto/detalle_tabla.html'
        context = {}
        envio_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id = pk)
        context['contexto_envio_traslado_producto_detalle'] = envio_traslado_producto_detalle
        context['contexto_series'] = ValidarSerieEnvioTrasladoProductoDetalle.objects.filter(envio_traslado_producto_detalle = envio_traslado_producto_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesEnvioTrasladoProductoDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.delete_validarseriesenviotrasladoproductodetalle')
    model = ValidarSerieEnvioTrasladoProductoDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:validar_series_envio_traslado_producto_detalle', kwargs={'pk': self.get_object().envio_traslado_producto_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesEnvioTrasladoProductoDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context

####################################################################################################


class RecepcionTrasladoProductoListView(PermissionRequiredMixin, ListView):
    permission_required = ('traslado_producto.view_recepciontrasladoproducto')
    model = RecepcionTrasladoProducto
    template_name = "traslado_producto/recepcion/inicio.html"
    context_object_name = 'contexto_recepcion_traslado_producto'

def RecepcionTrasladoProductoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/recepcion/inicio_tabla.html'
        context = {}
        context['contexto_recepcion_traslado_producto'] = RecepcionTrasladoProducto.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class RecepcionTrasladoProductoCrearView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('traslado_producto.add_recepciontrasladoproducto')
    model = RecepcionTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = RecepcionTrasladoProductoForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.kwargs['recepcion'].id})

    def form_valid(self, form):
        self.kwargs['recepcion'] = form.instance
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RecepcionTrasladoProductoCrearView, self).get_context_data(**kwargs)
        context['accion'] = "Recepción"
        context['titulo'] = "Traslado Producto"
        return context


class RecepcionTrasladoProductoVerView(PermissionRequiredMixin, TemplateView):
    permission_required = ('traslado_producto.view_recepciontrasladoproducto')
    template_name = "traslado_producto/recepcion/detalle.html"

    def get_context_data(self, **kwargs):
        obj = RecepcionTrasladoProducto.objects.get(id = kwargs['id_recepcion_traslado_producto'])
        sociedades = Sociedad.objects.filter(estado_sunat=1)

        materiales = None
        try:
            materiales = obj.RecepcionTrasladoProductoDetalle_recepcion_traslado_producto.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = super(RecepcionTrasladoProductoVerView, self).get_context_data(**kwargs)
        context['recepcion_traslado_producto'] = obj
        context['sociedades'] = sociedades
        context['materiales'] = materiales
        context['accion'] = "Crear"
        context['titulo'] = "Recepción Traslado"
        return context

def RecepcionTrasladoProductoVerTabla(request, id_recepcion_traslado_producto):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/recepcion/detalle_tabla.html'
        obj = RecepcionTrasladoProducto.objects.get(id = id_recepcion_traslado_producto)

        materiales = None
        try:
            materiales = obj.RecepcionTrasladoProductoDetalle_recepcion_traslado_producto.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except Exception as e:
            pass

        sociedades = Sociedad.objects.filter(estado_sunat=1)

        context = {}
        context['recepcion_traslado_producto'] = obj
        context['sociedades'] = sociedades
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class  RecepcionTrasladoProductoActualizarView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_recepciontrasladoproducto')
    model = RecepcionTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = RecepcionTrasladoProductoActualizarForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RecepcionTrasladoProductoActualizarView, self).get_context_data(**kwargs)
        context['accion'] = "Recepción"
        context['titulo'] = "Traslado Producto"
        return context


class RecepcionTrasladoProductoGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.change_recepciontrasladoproducto')
    model = RecepcionTrasladoProducto
    template_name = "traslado_producto/recepcion/form_guardar.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        context['titulo'] = 'Error de guardar'
        error_productos = True
        recepcion = self.get_object()
        if recepcion.RecepcionTrasladoProductoDetalle_recepcion_traslado_producto.all():
            error_productos = False
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_productos:
            context['texto'] = 'No hay productos.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            movimiento_inicial = TipoMovimiento.objects.get(codigo=139)  # Salida por traslado
            movimiento_final = TipoMovimiento.objects.get(codigo=140)  # Recepción por traslado
            for detalle in self.object.RecepcionTrasladoProductoDetalle_recepcion_traslado_producto.all():
                movimiento_cero = MovimientosAlmacen.objects.get(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.envio_traslado_producto_detalle.cantidad_envio,
                    tipo_movimiento=movimiento_inicial,
                    tipo_stock=detalle.envio_traslado_producto_detalle.tipo_stock,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object.envio_traslado_producto),
                    id_registro_documento_proceso=self.object.envio_traslado_producto.id,
                    almacen=detalle.envio_traslado_producto_detalle.almacen_origen,
                    sociedad=self.object.sociedad,
                )
                movimiento_anterior = MovimientosAlmacen.objects.get(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.envio_traslado_producto_detalle.cantidad_envio,
                    tipo_movimiento=movimiento_inicial,
                    tipo_stock=movimiento_inicial.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object.envio_traslado_producto),
                    id_registro_documento_proceso=self.object.envio_traslado_producto.id,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_cero,
                )
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_recepcion,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_anterior,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_recepcion,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=detalle.envio_traslado_producto_detalle.tipo_stock,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen_destino,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_uno,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                for validar in detalle.envio_traslado_producto_detalle.ValidarSerieEnvioTrasladoProductoDetalle_envio_traslado_producto_detalle.all():
                    validar.serie.serie_movimiento_almacen.add(movimiento_uno)
                    validar.serie.serie_movimiento_almacen.add(movimiento_dos)
                    validar.delete()

            numero_recepcion_traslado = RecepcionTrasladoProducto.objects.all().aggregate(Count('numero_recepcion_traslado'))['numero_recepcion_traslado__count'] + 1
            self.object.numero_recepcion_traslado = numero_recepcion_traslado
            self.object.estado = 3
            self.object.fecha_recepcion = datetime. now()
            registro_guardar(self.object, self.request)
            self.object.save()

            self.object.envio_traslado_producto.estado = 3
            registro_guardar(self.object.envio_traslado_producto, self.request)
            self.object.envio_traslado_producto.save()

            messages.success(request, MENSAJE_GUARDAR_RECEPCION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RecepcionTrasladoProductoGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Recepcion"
        context['guardar'] = "true"
        return context


class RecepcionTrasladoProductoAnularView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.change_recepciontrasladoproducto')
    model = RecepcionTrasladoProducto
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            movimiento_final = TipoMovimiento.objects.get(codigo=140)  # Recepción por traslado
            for detalle in self.object.RecepcionTrasladoProductoDetalle_recepcion_traslado_producto.all():
                movimiento_dos = MovimientosAlmacen.objects.get(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad_recepcion,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen_destino,
                    sociedad=self.object.sociedad,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

            movimiento_uno = movimiento_dos.movimiento_anterior

            movimiento_dos.delete()
            movimiento_uno.delete()

            self.object.estado = 4
            registro_guardar(self.object, self.request)
            self.object.save()

            self.object.envio_traslado_producto.estado = 2
            registro_guardar(self.object.envio_traslado_producto, self.request)
            self.object.envio_traslado_producto.save()
            messages.success(request, MENSAJE_GUARDAR_RECEPCION)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RecepcionTrasladoProductoAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Recepcion"
        context['guardar'] = "true"
        return context


class  RecepcionTrasladoProductoObservacionesView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_recepciontrasladoproducto')
    model = RecepcionTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = RecepcionTrasladoProductoObservacionesForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RecepcionTrasladoProductoObservacionesView, self).get_context_data(**kwargs)
        context['accion'] = "Observaciones"
        return context


class RecepcionTrasladoProductoMaterialDetalleView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('traslado_producto.change_recepciontrasladoproducto')
    template_name = "traslado_producto/recepcion/from_material.html"
    form_class = RecepcionTrasladoProductoMaterialDetalleForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_sede = False
        context['titulo'] = 'Error de guardar'
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        if not recepcion_traslado_producto.sede_destino:
            error_sede = True

        if error_sede:
            context['texto'] = 'Ingrese una sede de destino.'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.kwargs['id_recepcion_traslado_producto']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        almacen_destino = form.cleaned_data.get('almacen_destino')
        envio_traslado_producto_detalle = form.cleaned_data.get('material')
        try:
            if self.request.session['primero']:
                recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
                item = len(RecepcionTrasladoProductoDetalle.objects.filter(recepcion_traslado_producto = recepcion_traslado_producto))

                obj, created = RecepcionTrasladoProductoDetalle.objects.get_or_create(
                    envio_traslado_producto_detalle = envio_traslado_producto_detalle,
                    recepcion_traslado_producto = recepcion_traslado_producto,
                )

                print(obj, created)

                if created:
                    obj.item = item + 1
                    obj.content_type = envio_traslado_producto_detalle.content_type
                    obj.id_registro = envio_traslado_producto_detalle.id_registro
                    obj.almacen_destino = almacen_destino
                    obj.cantidad_recepcion = envio_traslado_producto_detalle.cantidad_envio
                    obj.unidad = envio_traslado_producto_detalle.unidad
                else:
                    obj.almacen_destino = almacen_destino

                registro_guardar(obj, self.request)
                print("Por grabar")
                obj.save()
                print("Grabado")
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        kwargs['recepcion_traslado_producto'] = recepcion_traslado_producto
        kwargs['lista_materiales'] = recepcion_traslado_producto.envio_traslado_producto.EnvioTrasladoProductoDetalle_envio_traslado_producto.all()
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        context = super(RecepcionTrasladoProductoMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar'
        context['accion'] = 'Material'
        context['sociedad'] = recepcion_traslado_producto.sociedad.id
        context['url_stock'] = reverse_lazy('traslado_producto_app:stock', kwargs={'id_recepcion_traslado_producto_detalle':1})[:-2]
        context['url_unidad'] = reverse_lazy('traslado_producto_app:unidad_material', kwargs={'id_recepcion_traslado_producto_detalle':1})[:-2]
        return context

class  RecepcionTrasladoProductoActualizarMaterialDetalleView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_recepciontrasladoproducto')
    model = RecepcionTrasladoProductoDetalle
    template_name = "traslado_producto/recepcion/form_actualizar_material.html"
    form_class = RecepcionTrasladoProductoMaterialActualizarDetalleForm

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_sede = False
        context['titulo'] = 'Error de guardar'
        detalle = RecepcionTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        recepcion_traslado_producto = detalle.recepcion_traslado_producto
        recepcion_traslado_producto = recepcion_traslado_producto
        if not recepcion_traslado_producto.sede_destino:
            error_sede = True

        if error_sede:
            context['texto'] = 'Ingrese una sede destino.'
            return render(request, 'includes/modal sin permiso.html', context)
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.get_object().recepcion_traslado_producto.id})

    def get_form_kwargs(self, *args, **kwargs):
        detalle = RecepcionTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        recepcion_traslado_producto = detalle.recepcion_traslado_producto
        kwargs = super().get_form_kwargs()
        kwargs['recepcion_traslado_producto'] = recepcion_traslado_producto
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        detalle = RecepcionTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        recepcion_traslado_producto = detalle.recepcion_traslado_producto
        context = super(RecepcionTrasladoProductoActualizarMaterialDetalleView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Item"
        context['material'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        context['id_material'] = self.get_object().id
        context['sociedad'] = recepcion_traslado_producto.sociedad.id
        context['url_stock'] = reverse_lazy('traslado_producto_app:stock', kwargs={'id_recepcion_traslado_producto_detalle':1})[:-2]
        context['url_unidad'] = reverse_lazy('traslado_producto_app:unidad_material', kwargs={'id_recepcion_traslado_producto_detalle':1})[:-2]
        return context

class RecepcionTrasladoProductoMaterialDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.delete_recepciontrasladoproducto')
    model = RecepcionTrasladoProductoDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.get_object().recepcion_traslado_producto.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            materiales = RecepcionTrasladoProductoDetalle.objects.filter(recepcion_traslado_producto=self.get_object().recepcion_traslado_producto)
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
        context = super(RecepcionTrasladoProductoMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)

        return context


class MotivoTrasladoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('traslado_producto.add_motivotraslado')
    model = MotivoTraslado
    template_name = "includes/formulario generico.html"
    form_class = MotivoTrasladoForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MotivoTrasladoCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Crear"
        context['titulo'] = "Motivo de Traslado"

        return context


def StockView(request, id_recepcion_traslado_producto_detalle):
    if request.method == 'GET':
        try:
            recepcion_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id=id_recepcion_traslado_producto_detalle)
            return HttpResponse(recepcion_traslado_producto_detalle.producto.stock)
        except:
            return HttpResponse("")


def StockSociedadAlmacenView(request, id_recepcion_traslado_producto_detalle, id_sociedad, id_almacen):
    if request.method == 'GET':
        try:
            recepcion_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id=id_recepcion_traslado_producto_detalle)
            return HttpResponse(stock(recepcion_traslado_producto_detalle.content_type, recepcion_traslado_producto_detalle.id_registro, id_sociedad, id_almacen))
        except:
            try:
                recepcion_traslado_producto_detalle = RecepcionTrasladoProductoDetalle.objects.get(id=id_recepcion_traslado_producto_detalle)
                return HttpResponse(stock(recepcion_traslado_producto_detalle.content_type, recepcion_traslado_producto_detalle.id_registro, id_sociedad, id_almacen))
            except:
                return HttpResponse("")


class UnidadForm(forms.Form):
    unidad = forms.ModelChoiceField(queryset = Unidad.objects.all(), required=False)


def UnidadMaterialView(request, id_recepcion_traslado_producto_detalle):
    form = UnidadForm()
    recepcion_traslado_producto_detalle = EnvioTrasladoProductoDetalle.objects.get(id=id_recepcion_traslado_producto_detalle)
    form.fields['unidad'].queryset = recepcion_traslado_producto_detalle.producto.subfamilia.unidad.all()
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


class TraspasoStockListView(PermissionRequiredMixin, ListView):
    permission_required = ('traslado_producto.view_traspasostock')
    model = TraspasoStock
    template_name = "traslado_producto/traspaso_stock/inicio.html"
    context_object_name = 'contexto_traspaso_stock'


def TraspasoStockTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/traspaso_stock/inicio_tabla.html'
        context = {}
        context['contexto_traspaso_stock'] = TraspasoStock.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class TraspasoStockCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('traslado_producto.add_traspasostock')
    model = TraspasoStock
    template_name = "traslado_producto/traspaso_stock/form_actualizar.html"
    form_class = TraspasoStockForm
    success_url = reverse_lazy('traslado_producto_app:traspaso_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item = len(TraspasoStock.objects.all())
        form.instance.nro_traspaso = item + 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TraspasoStockCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Traspaso de Stock"
        context['url_sede'] = reverse_lazy('sociedad_app:sociedad_sede', kwargs={'id_sociedad':1})[:-2]
        return context


class TraspasoStockUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_traspasostock')

    model = TraspasoStock
    template_name = "traslado_producto/traspaso_stock/form_actualizar.html"
    form_class = TraspasoStockForm
    success_url = reverse_lazy('traslado_producto_app:traspaso_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TraspasoStockUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Traspaso Stock"
        context['url_sede'] = reverse_lazy('sociedad_app:sociedad_sede', kwargs={'id_sociedad':1})[:-2]
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class TraspasoStockConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.delete_traspasostock')
    model = TraspasoStock
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cantidad_series = False
        error_almacen_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().TraspasoStockDetalle_traspaso_stock.all()
        for detalle in detalles:
            for validar_serie in detalle.ValidarSerieTraspasoStockDetalle_traspaso_stock_detalle.all():
                if detalle.control_serie and detalle.almacen != validar_serie.serie.almacen:
                    error_almacen_series = True
            if detalle.control_serie and detalle.series_validar != detalle.cantidad:
                error_cantidad_series = True
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')

        if error_cantidad_series:
            context['texto'] = 'Hay Series sin registrar.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_almacen_series:
            context['texto'] = 'Hay errores en los almacenes de las series.'
            return render(request, 'includes/modal sin permiso.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:traspaso_stock_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            movimiento_inicial = TipoMovimiento.objects.get(codigo=142)  # Salida por traspaso
            movimiento_final = TipoMovimiento.objects.get(codigo=143)  # Recepción por traspaso
            for detalle in self.object.TraspasoStockDetalle_traspaso_stock.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    tipo_movimiento=movimiento_inicial,
                    tipo_stock=detalle.tipo_stock_inicial,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=None,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                movimiento_dos = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    tipo_movimiento=movimiento_inicial,
                    tipo_stock=movimiento_inicial.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_uno,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                movimiento_tres = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=movimiento_final.tipo_stock_inicial,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_dos,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                movimiento_cuatro = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    tipo_movimiento=movimiento_final,
                    tipo_stock=detalle.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_tres,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                for validar in detalle.ValidarSerieTraspasoStockDetalle_traspaso_stock_detalle.all():
                    validar.serie.serie_movimiento_almacen.add(movimiento_uno)
                    validar.serie.serie_movimiento_almacen.add(movimiento_dos)
                    validar.serie.serie_movimiento_almacen.add(movimiento_tres)
                    validar.serie.serie_movimiento_almacen.add(movimiento_cuatro)
                    validar.delete()
            
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONCLUIR_TRASPASO_STOCK)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(TraspasoStockConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Traspaso Stock"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class TraspasoStockDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('traslado_producto.view_traspasostock')

    model = TraspasoStock
    template_name = "traslado_producto/traspaso_stock/detalle.html"
    context_object_name = 'contexto_traspaso_stock'

    def get_context_data(self, **kwargs):
        traspaso_stock = TraspasoStock.objects.get(id = self.kwargs['pk'])
        context = super(TraspasoStockDetailView, self).get_context_data(**kwargs)
        context['contexto_traspaso_stock_detalle'] = TraspasoStockDetalle.objects.filter(traspaso_stock = traspaso_stock)

        return context


def TraspasoStockDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/traspaso_stock/detalle_tabla.html'
        context = {}
        traspaso_stock = TraspasoStock.objects.get(id = pk)
        context['contexto_traspaso_stock'] = traspaso_stock
        context['contexto_traspaso_stock_detalle'] = TraspasoStockDetalle.objects.filter(traspaso_stock = traspaso_stock)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class TraspasoStockDetalleCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('traslado_producto.add_traspasostock')
    model = TraspasoStockDetalle
    template_name = "traslado_producto/traspaso_stock/form material.html"
    form_class = TraspasoStockDetalleForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:traspaso_stock_detalle', kwargs={'pk':self.kwargs['traspaso_stock_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        traspaso_stock = TraspasoStock.objects.get(id = self.kwargs['traspaso_stock_id'])
        kwargs['traspaso_stock'] = traspaso_stock
        return kwargs

    def form_valid(self, form):
        traspaso_stock = TraspasoStock.objects.get(id = self.kwargs['traspaso_stock_id'])
        form.instance.traspaso_stock = traspaso_stock
        item = len(TraspasoStockDetalle.objects.filter(traspaso_stock=traspaso_stock))
        form.instance.item = item + 1
        form.instance.content_type = ContentType.objects.get_for_model(form.cleaned_data['material'])
        form.instance.id_registro = form.cleaned_data['material'].id
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        traspaso_stock = TraspasoStock.objects.get(id = self.kwargs['traspaso_stock_id'])
        context = super(TraspasoStockDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        context['sociedad'] = traspaso_stock.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context


class TraspasoStockDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('traslado_producto.change_traspasostock')
    model = TraspasoStockDetalle
    template_name = "traslado_producto/traspaso_stock/form_actualizar_material.html"
    form_class = TraspasoStockDetalleActualizarForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:traspaso_stock_detalle', kwargs={'pk':self.kwargs['traspaso_stock_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        traspaso_stock = TraspasoStock.objects.get(id = self.kwargs['traspaso_stock_id'])
        kwargs['traspaso_stock'] = traspaso_stock
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        traspaso_stock = TraspasoStock.objects.get(id = self.kwargs['traspaso_stock_id'])
        context = super(TraspasoStockDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Material"
        context['material'] = self.get_object().producto
        context['sociedad'] = traspaso_stock.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context


class ValidarSeriesTraspasoStockDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('traslado_producto.view_traspasostockdetalle')
    template_name = "traslado_producto/validar_serie_traspaso_stock/detalle.html"
    form_class = TraspasoStockDetalleSeriesForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session['primero']:
            serie = form.cleaned_data['serie']
            traspaso_stock_detalle = TraspasoStockDetalle.objects.get(id = self.kwargs['pk'])
            try:
                buscar = Serie.objects.get(
                    serie_base=serie,
                    content_type=ContentType.objects.get_for_model(traspaso_stock_detalle.producto),
                    id_registro=traspaso_stock_detalle.producto.id,
                )
                buscar2 = ValidarSerieTraspasoStockDetalle.objects.filter(serie = buscar)

                if len(buscar2) != 0:
                    form.add_error('serie', "Serie ya ha sido registrada")
                    return super().form_invalid(form)

                if buscar.estado != 'DISPONIBLE' or buscar.estado != 'REPARADO':
                    form.add_error('serie', "Serie no disponible, su estado es: %s" % buscar.estado)
                    return super().form_invalid(form)
            except:
                form.add_error('serie', "Serie no encontrada: %s" % serie)
                return super().form_invalid(form)

            traspaso_stock_detalle = TraspasoStockDetalle.objects.get(id = self.kwargs['pk'])
            obj, created = ValidarSerieTraspasoStockDetalle.objects.get_or_create(
                traspaso_stock_detalle=traspaso_stock_detalle,
                serie=buscar,
            )
            if created:
                obj.estado = 1
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        traspaso_stock_detalle = TraspasoStockDetalle.objects.get(id = self.kwargs['pk'])
        cantidad = traspaso_stock_detalle.cantidad
        cantidad_registrada = len(ValidarSerieTraspasoStockDetalle.objects.filter(traspaso_stock_detalle=traspaso_stock_detalle))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad'] = cantidad
        kwargs['cantidad_registrada'] = cantidad_registrada
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        traspaso_stock_detalle = TraspasoStockDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesTraspasoStockDetailView, self).get_context_data(**kwargs)
        context['contexto_traspaso_stock_detalle'] = traspaso_stock_detalle
        context['contexto_series'] = ValidarSerieTraspasoStockDetalle.objects.filter(traspaso_stock_detalle = traspaso_stock_detalle)
        return context

def ValidarSeriesTraspasoStockDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'traslado_producto/validar_serie_traspaso_stock/detalle_tabla.html'
        context = {}
        traspaso_stock_detalle = TraspasoStockDetalle.objects.get(id = pk)
        context['contexto_traspaso_stock_detalle'] = traspaso_stock_detalle
        context['contexto_series'] = ValidarSerieTraspasoStockDetalle.objects.filter(traspaso_stock_detalle = traspaso_stock_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesTraspasoStockDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('traslado_producto.delete_validarseriesenviotrasladoproductodetalle')
    model = ValidarSerieTraspasoStockDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:validar_series_traspaso_stock_detalle', kwargs={'pk': self.get_object().traspaso_stock_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesTraspasoStockDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context