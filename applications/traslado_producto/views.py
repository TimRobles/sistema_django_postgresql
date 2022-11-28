from django.shortcuts import render
from applications.funciones import registrar_excepcion
from applications.importaciones import *
from applications.sociedad.models import Sociedad

from .models import (
    EnvioTrasladoProducto,
    EnvioTrasladoProductoDetalle,
)

from .forms import (
    EnvioTrasladoProductoForm,
    EnvioTrasladoProductoMaterialDetalleForm,
    EnvioTrasladoProductoObservacionesForm,
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
            materiales = obj.EnvioTrasladoProductoDetalle_.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
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

class  EnvioTrasladoProductoActualizarView(BSModalUpdateView):
    model = EnvioTrasladoProducto
    template_name = "includes/formulario generico.html"
    form_class = EnvioTrasladoProductoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoActualizarView, self).get_context_data(**kwargs)
        context['accion'] = "Envio"
        context['titulo'] = "Traslado Producto"
        return context

class EnvioTrasladoProductoGuardarView(BSModalDeleteView):
    model = EnvioTrasladoProducto
    template_name = "traslado_producto/envio/form_guardar.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            numero_envio_traslado = EnvioTrasladoProducto.objects.all().aggregate(Count('numero_envio_traslado'))['numero_envio_traslado__count'] + 1
            self.object.numero_envio_traslado = numero_envio_traslado
            self.object.fecha_traslado = datetime. now()

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
        context['guardar'] = "true"
        return context


class EnvioTrasladoProductoMaterialDetalleView(BSModalFormView):
    template_name = "traslado_producto/envio/from_material.html"
    form_class = EnvioTrasladoProductoMaterialDetalleForm
    # success_url = reverse_lazy('traslado_producto_app:envio_inicio')

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.get_object().envio_traslado_producto.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                envio_traslado_producto = EnvioTrasladoProducto.objects.get(id = self.kwargs['id_envio_traslado_producto'])
                item = len(EnvioTrasladoProductoDetalle.objects.filter(envio_traslado_almacen = envio_traslado_producto))

                material = form.cleaned_data.get('material')
                cantidad_envio = form.cleaned_data.get('cantidad_envio')

                obj, created = EnvioTrasladoProductoDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    envio_traslado_almacen = envio_traslado_producto,
                )
                if created:
                    obj.item = item + 1
                    obj.cantidad_envio = cantidad_envio

                else:
                    obj.cantidad_envio = obj.cantidad_envio + cantidad_envio


                registro_guardar(obj, self.request)
                obj.save()

                cantidad_total = obj.cantidad_envio
                cantidades = {}
                sociedades = Sociedad.objects.all()

            return HttpResponseRedirect(self.success_url)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(EnvioTrasladoProductoMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar'
        context['accion'] = 'Material'
        return context

class  EnvioTrasladoProductoActualizarMaterialDetalleView(BSModalFormView):
    model = EnvioTrasladoProductoDetalle
    template_name = "includes/formulario generico.html"
    form_class = EnvioTrasladoProductoMaterialDetalleForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.get_object().envio_traslado_producto.id})

    def get_form_kwargs(self, *args, **kwargs):
        print(self.kwargs)
        # envio_traslado_producto =EnvioTrasladoProducto.objects.get(id=self.kwargs['id_envio_traslado_producto'])
        detalle =EnvioTrasladoProductoDetalle.objects.get(id=self.kwargs['pk'])
        envio_traslado_producto = detalle.envio_traslado_producto
        sociedad = envio_traslado_producto.sociedad
        sede_origen = envio_traslado_producto.sede_origen
        print('********************')
        print(envio_traslado_producto)
        print(sociedad)
        print(sede_origen)
        print('********************')
        kwargs = super().get_form_kwargs()
        return kwargs

    # def dispatch(self, request, *args, **kwargs):
    #     context = {}
    #     error_sede = False
    #     context['titulo'] = 'Error Sede'
    #     if not self.get_object().sede_origen:
    #         error_sede = True

    #     if error_sede:
    #         context['texto'] = 'Ingrese sede origen.'
    #         return render(request, 'includes/modal sin permiso.html', context)
    #     return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoActualizarMaterialDetalleView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Item"
        return context

class EnvioTrasladoProductoMaterialDeleteView(BSModalDeleteView):
    model = EnvioTrasladoProductoDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('traslado_producto_app:envio_ver', kwargs={'id_envio_traslado_producto':self.get_object().envio_traslado_producto.id})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EnvioTrasladoProductoMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)

        return context
