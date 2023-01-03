from django.shortcuts import render
from applications.funciones import registrar_excepcion
from applications.importaciones import *
from applications.material.funciones import stock, tipo_stock_sede
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.sociedad.models import Sociedad

from .models import (
    EnvioTrasladoProducto,
    EnvioTrasladoProductoDetalle,
    MotivoTraslado,
    RecepcionTrasladoProducto,
    RecepcionTrasladoProductoDetalle,
)

from .forms import (
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
)


class EnvioTrasladoProductoListView(ListView):
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

class EnvioTrasladoProductoVerView(TemplateView):
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


class  EnvioTrasladoProductoActualizarView(BSModalUpdateView):
    model = EnvioTrasladoProducto
    template_name = "traslado_producto/envio/form_actualizar.html"
    form_class = EnvioTrasladoProductoForm

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

class EnvioTrasladoProductoGuardarView(BSModalDeleteView):
    model = EnvioTrasladoProducto
    template_name = "includes/eliminar generico.html"

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

class  EnvioTrasladoProductoObservacionesView(BSModalUpdateView):
    model = EnvioTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = EnvioTrasladoProductoObservacionesForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoObservacionesView, self).get_context_data(**kwargs)
        context['accion'] = "Observaciones"
        return context


class EnvioTrasladoProductoMaterialDetalleView(BSModalFormView):
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
        return super(EnvioTrasladoProductoMaterialDetalleView, self).dispatch(request, *args, **kwargs)

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
        stock_disponible = stock(ContentType.objects.get_for_model(material), material.id, envio_traslado_producto.sociedad.id, almacen_origen.id)

        buscar = EnvioTrasladoProductoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
            envio_traslado_producto=envio_traslado_producto,
        ).exclude(envio_traslado_producto__estado=4)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_envio'))['cantidad_envio__sum']
        else:
            contar = 0

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

class  EnvioTrasladoProductoActualizarMaterialDetalleView(BSModalUpdateView):
    model = EnvioTrasladoProductoDetalle
    template_name = "traslado_producto/envio/form_actualizar_material.html"
    form_class = EnvioTrasladoProductoMaterialActualizarDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.get_object().envio_traslado_producto.id})

    def get_form_kwargs(self, *args, **kwargs):
        print(self.kwargs)
        detalle = EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        kwargs = super().get_form_kwargs()
        kwargs['envio_traslado_producto'] = envio_traslado_producto
        return kwargs

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
        return super(EnvioTrasladoProductoActualizarMaterialDetalleView, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        detalle = EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        almacen_origen = form.cleaned_data.get('almacen_origen')
        tipo_stock = form.cleaned_data.get('tipo_stock')
        cantidad_envio = form.cleaned_data.get('cantidad_envio')
        material = detalle.producto
        stock_disponible = tipo_stock_sede(ContentType.objects.get_for_model(material), material.id, envio_traslado_producto.sociedad.id, almacen_origen.id, tipo_stock.id)

        buscar = EnvioTrasladoProductoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
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

class EnvioTrasladoProductoMaterialDeleteView(BSModalDeleteView):
    model = EnvioTrasladoProductoDetalle
    template_name = "includes/eliminar generico.html"

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



class RecepcionTrasladoProductoListView(ListView):
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

class RecepcionTrasladoProductoCrearView(BSModalCreateView):
    model = RecepcionTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = RecepcionTrasladoProductoForm

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


class RecepcionTrasladoProductoVerView(TemplateView):
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


class  RecepcionTrasladoProductoActualizarView(BSModalUpdateView):
    model = RecepcionTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = RecepcionTrasladoProductoActualizarForm

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


class RecepcionTrasladoProductoGuardarView(BSModalDeleteView):
    model = RecepcionTrasladoProducto
    template_name = "traslado_producto/recepcion/form_guardar.html"

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
                movimiento_anterior = MovimientosAlmacen.objects.get(
                    content_type_producto=detalle.content_type,
                    id_registro_producto=detalle.id_registro,
                    tipo_movimiento=movimiento_inicial,
                    tipo_stock=movimiento_inicial.tipo_stock_final,
                    signo_factor_multiplicador=+1,
                    content_type_documento_proceso=ContentType.objects.get_for_model(self.object.envio_traslado_producto),
                    id_registro_documento_proceso=self.object.envio_traslado_producto.id,
                    almacen=detalle.envio_traslado_producto_detalle.almacen_origen,
                    sociedad=self.object.envio_traslado_producto.sociedad,
                    movimiento_anterior=None,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
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
                    almacen=detalle.almacen_destino,
                    sociedad=self.object.sociedad,
                    movimiento_anterior=movimiento_anterior,
                    movimiento_reversion=False,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )

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


class RecepcionTrasladoProductoAnularView(BSModalDeleteView):
    model = RecepcionTrasladoProducto
    template_name = "includes/eliminar generico.html"

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


class  RecepcionTrasladoProductoObservacionesView(BSModalUpdateView):
    model = RecepcionTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = RecepcionTrasladoProductoObservacionesForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RecepcionTrasladoProductoObservacionesView, self).get_context_data(**kwargs)
        context['accion'] = "Observaciones"
        return context


class RecepcionTrasladoProductoMaterialDetalleView(BSModalFormView):
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
        return super(RecepcionTrasladoProductoMaterialDetalleView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.kwargs['id_recepcion_traslado_producto']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        almacen_destino = form.cleaned_data.get('almacen_destino')
        material = form.cleaned_data.get('material')
        cantidad_recepcion = form.cleaned_data.get('cantidad_recepcion')
        cantidad_enviada = recepcion_traslado_producto.envio_traslado_producto.EnvioTrasladoProductoDetalle_envio_traslado_producto.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
        ).aggregate(Sum('cantidad_envio'))['cantidad_envio__sum']

        buscar = RecepcionTrasladoProductoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
            recepcion_traslado_producto=recepcion_traslado_producto,
        ).exclude(recepcion_traslado_producto__estado=4)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_recepcion'))['cantidad_recepcion__sum']
        else:
            contar = 0

        if cantidad_enviada < contar + cantidad_recepcion:
            form.add_error('cantidad_recepcion', 'Se superó la cantidad enviada. Máximo: %s. Contado: %s.' % (cantidad_enviada, contar + cantidad_recepcion))
            return super().form_invalid(form)

        try:
            if self.request.session['primero']:
                recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
                item = len(RecepcionTrasladoProductoDetalle.objects.filter(recepcion_traslado_producto = recepcion_traslado_producto))

                material = form.cleaned_data.get('material')
                cantidad_recepcion = form.cleaned_data.get('cantidad_recepcion')

                obj, created = RecepcionTrasladoProductoDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    recepcion_traslado_producto = recepcion_traslado_producto,
                    almacen_destino = form.cleaned_data.get('almacen_destino'),
                    unidad = form.cleaned_data.get('unidad')
                )
                if created:
                    obj.item = item + 1
                    obj.cantidad_recepcion = cantidad_recepcion

                else:
                    obj.cantidad_recepcion = obj.cantidad_recepcion + cantidad_recepcion

                registro_guardar(obj, self.request)
                obj.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        kwargs['recepcion_traslado_producto'] = recepcion_traslado_producto
        lista_materiales = []
        for detalle in recepcion_traslado_producto.envio_traslado_producto.EnvioTrasladoProductoDetalle_envio_traslado_producto.all():
            lista_materiales.append(detalle.id_registro)
        kwargs['lista_materiales'] = lista_materiales
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        recepcion_traslado_producto = RecepcionTrasladoProducto.objects.get(id = self.kwargs['id_recepcion_traslado_producto'])
        context = super(RecepcionTrasladoProductoMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar'
        context['accion'] = 'Material'
        context['sociedad'] = recepcion_traslado_producto.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context

class  RecepcionTrasladoProductoActualizarMaterialDetalleView(BSModalUpdateView):
    model = RecepcionTrasladoProductoDetalle
    template_name = "traslado_producto/recepcion/form_actualizar_material.html"
    form_class = RecepcionTrasladoProductoMaterialActualizarDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:recepcion_ver', kwargs={'id_recepcion_traslado_producto':self.get_object().recepcion_traslado_producto.id})

    def get_form_kwargs(self, *args, **kwargs):
        detalle = RecepcionTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        recepcion_traslado_producto = detalle.recepcion_traslado_producto
        kwargs = super().get_form_kwargs()
        kwargs['recepcion_traslado_producto'] = recepcion_traslado_producto
        return kwargs

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
        return super(RecepcionTrasladoProductoActualizarMaterialDetalleView, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        detalle = RecepcionTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        recepcion_traslado_producto = detalle.recepcion_traslado_producto
        material = detalle.producto
        cantidad_recepcion = form.cleaned_data.get('cantidad_recepcion')
        cantidad_enviada = recepcion_traslado_producto.envio_traslado_producto.EnvioTrasladoProductoDetalle_envio_traslado_producto.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
        ).aggregate(Sum('cantidad_envio'))['cantidad_envio__sum']

        buscar = RecepcionTrasladoProductoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(material),
            id_registro=material.id,
            recepcion_traslado_producto=recepcion_traslado_producto,
        ).exclude(recepcion_traslado_producto__estado=4).exclude(id=detalle.id)

        if buscar:
            contar = buscar.aggregate(Sum('cantidad_recepcion'))['cantidad_recepcion__sum']
        else:
            contar = 0

        if cantidad_enviada < contar + cantidad_recepcion:
            form.add_error('cantidad_recepcion', 'Se superó la cantidad enviada. Máximo: %s. Contado: %s.' % (cantidad_enviada, contar + cantidad_recepcion))
            return super().form_invalid(form)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        detalle = RecepcionTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        recepcion_traslado_producto = detalle.recepcion_traslado_producto
        context = super(RecepcionTrasladoProductoActualizarMaterialDetalleView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Item"
        context['material'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        context['sociedad'] = recepcion_traslado_producto.sociedad.id
        context['url_stock'] = reverse_lazy('material_app:stock', kwargs={'id_material':1})[:-2]
        context['url_unidad'] = reverse_lazy('material_app:unidad_material', kwargs={'id_material':1})[:-2]
        return context

class RecepcionTrasladoProductoMaterialDeleteView(BSModalDeleteView):
    model = RecepcionTrasladoProductoDetalle
    template_name = "includes/eliminar generico.html"

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


class MotivoTrasladoCreateView(BSModalCreateView):
    model = MotivoTraslado
    template_name = "includes/formulario generico.html"
    form_class = MotivoTrasladoForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(MotivoTrasladoCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Crear"
        context['titulo'] = "Motivo de Traslado"

        return context
