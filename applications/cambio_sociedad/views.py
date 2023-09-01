from django.shortcuts import render
from django import forms
from applications.calidad.models import Serie
from applications.comprobante_despacho.models import Guia, GuiaDetalle
from applications.datos_globales.models import SeriesComprobante, Unidad
from applications.funciones import numeroXn, registrar_excepcion, slug_aleatorio
from applications.importaciones import *

from applications.logistica.pdf import generarSeriesNotaSalida
from applications.material.funciones import stock, ver_tipo_stock
from applications.material.models import Material
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento, TipoStock
from applications.sociedad.models import Sociedad
from applications.orden_compra.models import OrdenCompra, OrdenCompraDetalle

from .models import (
    CambioSociedadStock,
    CambioSociedadStockDetalle,
    ValidarSerieCambioSociedadStockDetalle,
)

from .forms import (
    CambioSociedadStockDetalleActualizarForm,
    CambioSociedadStockDetalleForm,
    CambioSociedadStockDetalleSeriesForm,
    CambioSociedadStockForm,
)

class CambioSociedadStockListView(PermissionRequiredMixin, ListView):
    permission_required = ('cambio_sociedad.view_cambiosociedadstock')
    model = CambioSociedadStock
    template_name = "cambio_sociedad/cambio_sociedad_stock/inicio.html"
    context_object_name = 'contexto_cambio_sociedad_stock'


def CambioSociedadStockTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cambio_sociedad/cambio_sociedad_stock/inicio_tabla.html'
        context = {}
        context['contexto_cambio_sociedad_stock'] = CambioSociedadStock.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class CambioSociedadStockCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('cambiosociedad.add_cambiosociedadstock')
    model = CambioSociedadStock
    template_name = "cambio_sociedad/cambio_sociedad_stock/form_actualizar.html"
    form_class = CambioSociedadStockForm
    success_url = reverse_lazy('cambio_sociedad_app:cambio_sociedad_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item = len(CambioSociedadStock.objects.all())
        form.instance.nro_cambio = item + 1
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CambioSociedadStockCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Cambio de Sociedad Stock"
        context['url_sede'] = reverse_lazy('sociedad_app:sociedad_sede', kwargs={'id_sociedad':1})[:-2]
        return context


class CambioSociedadStockUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cambiosociedad.change_cambiosociedadstock')

    model = CambioSociedadStock
    template_name = "cambio_sociedad/cambio_sociedad_stock/form_actualizar.html"
    form_class = CambioSociedadStockForm
    success_url = reverse_lazy('cambio_sociedad_app:cambio_sociedad_stock_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CambioSociedadStockUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cambio de Sociedad Stock"
        context['url_sede'] = reverse_lazy('sociedad_app:sociedad_sede', kwargs={'id_sociedad':1})[:-2]
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class CambioSociedadStockConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cambiosociedad.delete_cambiosociedadstock')
    model = CambioSociedadStock
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_cantidad_series = False
        error_almacen_series = False
        context['titulo'] = 'Error de guardar'
        detalles = self.get_object().CambioSociedadStockDetalle_cambio_sociedad_stock.all()
        for detalle in detalles:
            for validar_serie in detalle.ValidarSerieCambioSociedadStockDetalle_cambio_sociedad_stock_detalle.all():
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
        return reverse_lazy('cambio_sociedad_app:cambio_sociedad_stock_detalle', kwargs={'pk': self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            movimiento_inicial = TipoMovimiento.objects.get(codigo=169)  # Salida por cambio sociedad
            movimiento_final = TipoMovimiento.objects.get(codigo=170)  # Recepción por cambio sociedad
            for detalle in self.object.CambioSociedadStockDetalle_cambio_sociedad_stock.all():
                movimiento_uno = MovimientosAlmacen.objects.create(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    cantidad=detalle.cantidad,
                    tipo_movimiento=movimiento_inicial,
                    tipo_stock=detalle.tipo_stock,
                    signo_factor_multiplicador=-1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen,
                    sociedad=self.object.sociedad_inicial,
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
                    sociedad=self.object.sociedad_inicial,
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
                    sociedad=self.object.sociedad_final,
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
                    tipo_stock=detalle.tipo_stock,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                    id_registro_documento_proceso=self.object.id,
                    almacen=detalle.almacen,
                    sociedad=self.object.sociedad_final,
                    movimiento_anterior=movimiento_tres,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

                for validar in detalle.ValidarSerieCambioSociedadStockDetalle_cambio_sociedad_stock_detalle.all():
                    validar.serie.serie_movimiento_almacen.add(movimiento_uno)
                    validar.serie.serie_movimiento_almacen.add(movimiento_dos)
                    validar.serie.serie_movimiento_almacen.add(movimiento_tres)
                    validar.serie.serie_movimiento_almacen.add(movimiento_cuatro)
                    validar.delete()
            
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_CONCLUIR_CAMBIO_SOCIEDAD_STOCK)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CambioSociedadStockConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir"
        context['titulo'] = "Cambio de Sociedad Stock"
        context['dar_baja'] = "true"
        context['item'] = self.object
        return context


class CambioSociedadStockDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('cambiosociedad.view_cambiosociedadstock')

    model = CambioSociedadStock
    template_name = "cambio_sociedad/cambio_sociedad_stock/detalle.html"
    context_object_name = 'contexto_cambio_sociedad_stock'

    def get_context_data(self, **kwargs):
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = self.kwargs['pk'])
        context = super(CambioSociedadStockDetailView, self).get_context_data(**kwargs)
        context['contexto_cambio_sociedad_stock_detalle'] = CambioSociedadStockDetalle.objects.filter(cambio_sociedad_stock = cambio_sociedad_stock)

        return context


def CambioSociedadStockDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'cambio_sociedad/cambio_sociedad_stock/detalle_tabla.html'
        context = {}
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = pk)
        context['contexto_cambio_sociedad_stock'] = cambio_sociedad_stock
        context['contexto_cambio_sociedad_stock_detalle'] = CambioSociedadStockDetalle.objects.filter(cambio_sociedad_stock = cambio_sociedad_stock)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class CambioSociedadStockDetalleCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('cambiosociedad.add_cambiosociedadstock')
    model = CambioSociedadStockDetalle
    template_name = "cambio_sociedad/cambio_sociedad_stock/form material.html"
    form_class = CambioSociedadStockDetalleForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cambio_sociedad_app:cambio_sociedad_stock_detalle', kwargs={'pk':self.kwargs['cambio_sociedad_stock_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = self.kwargs['cambio_sociedad_stock_id'])
        kwargs['cambio_sociedad_stock'] = cambio_sociedad_stock
        return kwargs

    def form_valid(self, form):
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = self.kwargs['cambio_sociedad_stock_id'])
        form.instance.cambio_sociedad_stock = cambio_sociedad_stock
        item = len(CambioSociedadStockDetalle.objects.filter(cambio_sociedad_stock=cambio_sociedad_stock))
        form.instance.item = item + 1
        form.instance.content_type = ContentType.objects.get_for_model(form.cleaned_data['material'])
        form.instance.id_registro = form.cleaned_data['material'].id
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = self.kwargs['cambio_sociedad_stock_id'])
        context = super(CambioSociedadStockDetalleCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        context['sociedad'] = cambio_sociedad_stock.sociedad_inicial.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context


class CambioSociedadStockDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('cambiosociedad.change_cambiosociedadstock')
    model = CambioSociedadStockDetalle
    template_name = "cambio_sociedad/cambio_sociedad_stock/form_actualizar_material.html"
    form_class = CambioSociedadStockDetalleActualizarForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cambio_sociedad_app:cambio_sociedad_stock_detalle', kwargs={'pk':self.kwargs['cambio_sociedad_stock_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = self.kwargs['cambio_sociedad_stock_id'])
        kwargs['cambio_sociedad_stock'] = cambio_sociedad_stock
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        cambio_sociedad_stock = CambioSociedadStock.objects.get(id = self.kwargs['cambio_sociedad_stock_id'])
        context = super(CambioSociedadStockDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Material"
        context['material'] = self.get_object().producto
        context['sociedad'] = cambio_sociedad_stock.sociedad_inicial.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context


class ValidarSeriesCambioSociedadStockDetailView(PermissionRequiredMixin, FormView):
    permission_required = ('cambiosociedad.view_cambiosociedadstockdetalle')
    template_name = "cambio_sociedad/validar_serie_cambio_sociedad_stock/detalle.html"
    form_class = CambioSociedadStockDetalleSeriesForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session['primero']:
            serie = form.cleaned_data['serie']
            cambio_sociedad_stock_detalle = CambioSociedadStockDetalle.objects.get(id = self.kwargs['pk'])
            try:
                buscar = Serie.objects.get(
                    serie_base=serie,
                    content_type=ContentType.objects.get_for_model(cambio_sociedad_stock_detalle.producto),
                    id_registro=cambio_sociedad_stock_detalle.producto.id,
                )
                buscar2 = ValidarSerieCambioSociedadStockDetalle.objects.filter(serie = buscar)

                if len(buscar2) != 0:
                    form.add_error('serie', "Serie ya ha sido registrada")
                    return super().form_invalid(form)

            except:
                form.add_error('serie', "Serie no encontrada: %s" % serie)
                return super().form_invalid(form)

            cambio_sociedad_stock_detalle = CambioSociedadStockDetalle.objects.get(id = self.kwargs['pk'])
            obj, created = ValidarSerieCambioSociedadStockDetalle.objects.get_or_create(
                cambio_sociedad_stock_detalle=cambio_sociedad_stock_detalle,
                serie=buscar,
            )
            if created:
                obj.estado = 1
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        cambio_sociedad_stock_detalle = CambioSociedadStockDetalle.objects.get(id = self.kwargs['pk'])
        cantidad = cambio_sociedad_stock_detalle.cantidad
        cantidad_registrada = len(ValidarSerieCambioSociedadStockDetalle.objects.filter(cambio_sociedad_stock_detalle=cambio_sociedad_stock_detalle))
        kwargs = super().get_form_kwargs()
        kwargs['cantidad'] = cantidad
        kwargs['cantidad_registrada'] = cantidad_registrada
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        cambio_sociedad_stock_detalle = CambioSociedadStockDetalle.objects.get(id = self.kwargs['pk'])
        context = super(ValidarSeriesCambioSociedadStockDetailView, self).get_context_data(**kwargs)
        context['contexto_cambio_sociedad_stock_detalle'] = cambio_sociedad_stock_detalle
        context['contexto_series'] = ValidarSerieCambioSociedadStockDetalle.objects.filter(cambio_sociedad_stock_detalle = cambio_sociedad_stock_detalle)
        return context

def ValidarSeriesCambioSociedadStockDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'cambio_sociedad/validar_serie_cambio_sociedad_stock/detalle_tabla.html'
        context = {}
        cambio_sociedad_stock_detalle = CambioSociedadStockDetalle.objects.get(id = pk)
        context['contexto_cambio_sociedad_stock_detalle'] = cambio_sociedad_stock_detalle
        context['contexto_series'] = ValidarSerieCambioSociedadStockDetalle.objects.filter(cambio_sociedad_stock_detalle = cambio_sociedad_stock_detalle)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ValidarSeriesCambioSociedadStockSeriesPdf(View):
    def get(self, request, *args, **kwargs):
        obj = CambioSociedadStock.objects.get(id=self.kwargs['pk'])

        color = obj.sociedad_final.color
        titulo = 'REGISTRO DE SERIES DE EQUIPOS'
        vertical = True
        logo = [obj.sociedad_final.logo.url]
        pie_pagina = obj.sociedad_final.pie_pagina

        titulo = "%s - %s - %s" % (titulo, numeroXn(obj.nro_cambio, 6), obj.encargado)

        movimientos = MovimientosAlmacen.objects.buscar_movimiento(obj, ContentType.objects.get_for_model(CambioSociedadStock))
        series = Serie.objects.buscar_series(movimientos)
        series_unicas = []
        if series:
            series_unicas = series.order_by('id_registro', 'serie_base').distinct()
        
        texto_cabecera = 'Series registradas:'
        
        series_final = {}
        for serie in series_unicas:
            if not serie.producto in series_final:
                series_final[serie.producto] = []
            series_final[serie.producto].append(serie.serie_base)

        TablaEncabezado = ['DOCUMENTO',
                           'FECHA',
                           'ENCARGADO',
                           ]

        TablaDatos = []
        TablaDatos.append(numeroXn(obj.nro_cambio, 6))
        TablaDatos.append(obj.fecha.strftime('%d/%m/%Y'))
        TablaDatos.append(obj.encargado)
        
        buf = generarSeriesNotaSalida(titulo, vertical, logo, pie_pagina, texto_cabecera, TablaEncabezado, TablaDatos, series_final, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition'] = 'inline; filename=%s.pdf' % titulo

        return respuesta


class ValidarSeriesCambioSociedadStockDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('cambiosociedad.delete_validarseriesenviotrasladoproductodetalle')
    model = ValidarSerieCambioSociedadStockDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('cambio_sociedad_app:validar_series_cambio_sociedad_stock_detalle', kwargs={'pk': self.get_object().cambio_sociedad_stock_detalle.id})

    def get_context_data(self, **kwargs):
        context = super(ValidarSeriesCambioSociedadStockDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Serie"
        context['item'] = self.get_object().serie
        context['dar_baja'] = "true"
        return context
    

# class CambioSociedadGenerarOrdenCompraView(PermissionRequiredMixin, BSModalFormView):
#     permission_required = ('orden_compra.add_ordencompra')

#     form_class = OrdenCompraSociedadForm
#     template_name = "includes/formulario generico.html"
#     success_url = reverse_lazy('orden_compra_app:orden_compra_inicio')

#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     @transaction.atomic
#     def form_valid(self, form):
#         sid = transaction.savepoint()
#         try:
#             if self.request.session['primero']:
#                 cambio_sociedad = CambioSociedadStock.objects.get(id=self.kwargs['id'])
#                 numero_orden_compra = form.cleaned_data['sociedad'].abreviatura + numeroXn(len(OrdenCompra.objects.filter(sociedad = form.cleaned_data['sociedad']))+1, 6)

#                 orden_compra = OrdenCompra.objects.create(
#                     internacional_nacional = oferta.internacional_nacional,
#                     incoterms = oferta.incoterms,
#                     numero_orden_compra = numero_orden_compra,
#                     oferta_proveedor = oferta,
#                     sociedad = form.cleaned_data['sociedad'],
#                     fecha_orden = date.today(),
#                     moneda = oferta.moneda,
#                     slug = slug_aleatorio(OrdenCompra),
#                     created_by = self.request.user,
#                     updated_by = self.request.user,
#                 )

#                 oferta_detalle = oferta.OfertaProveedorDetalle_oferta_proveedor.all()
#                 for detalle in oferta_detalle:
#                     orden_compra_detalle = OrdenCompraDetalle.objects.create(
#                         item = detalle.item,
#                         content_type = detalle.proveedor_material.content_type,
#                         id_registro = detalle.proveedor_material.id_registro,
#                         cantidad = detalle.cantidad,
#                         precio_unitario_sin_igv = detalle.precio_unitario_sin_igv,
#                         precio_unitario_con_igv = detalle.precio_unitario_con_igv,
#                         precio_final_con_igv = detalle.precio_final_con_igv,
#                         descuento = detalle.descuento,
#                         sub_total = detalle.sub_total,
#                         igv = detalle.igv,
#                         total = detalle.total,
#                         tipo_igv = detalle.tipo_igv,
#                         orden_compra = orden_compra,
#                         created_by = self.request.user,
#                         updated_by = self.request.user,
#                         )
#                 self.request.session['primero'] = False

#             return super().form_valid(form)
#         except Exception as ex:
#             transaction.savepoint_rollback(sid)
#             registrar_excepcion(self, ex, __file__)
#         return HttpResponseRedirect(self.get_success_url())

#     def get_context_data(self, **kwargs):
#         self.request.session['primero'] = True
#         context = super(CambioSociedadGenerarOrdenCompraView, self).get_context_data(**kwargs)
#         context['accion'] = "Generar"
#         context['titulo'] = "Orden de Compra"
#         return context