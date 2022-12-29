from applications.funciones import numeroXn, registrar_excepcion
from applications.links import link_detalle
from applications.home.templatetags.funciones_propias import filename
from applications.importaciones import *
from applications.movimiento_almacen.models import MovimientosAlmacen
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from applications.recepcion_compra.forms import ArchivoRecepcionCompraForm, FotoRecepcionCompraForm, RecepcionCompraAnularForm, RecepcionCompraGenerarNotaIngresoForm
from .models import FotoRecepcionCompra, RecepcionCompra, ArchivoRecepcionCompra

# Create your views here.

class RecepcionCompraDetailView(DetailView):
    model = RecepcionCompra
    template_name = "recepcion_compra/recepcion_compra/detalle.html"
    context_object_name = 'contexto_recepcion_compra'

    def get_context_data(self, **kwargs):
        context = super(RecepcionCompraDetailView, self).get_context_data(**kwargs)
        context['materiales'] = self.get_object().content_type.model_class().objects.ver_detalle(self.get_object().id_registro)
        context['archivos'] = ArchivoRecepcionCompra.objects.filter(recepcion_compra=self.get_object())
        context['fotos'] = FotoRecepcionCompra.objects.filter(recepcion_compra=self.get_object())
        context['regresar'] = link_detalle(self.get_object().content_type, self.get_object().content_type.get_object_for_this_type(id=self.get_object().id_registro).slug)
        return context
    

def RecepcionCompraDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'recepcion_compra/recepcion_compra/detalle_tabla.html'
        context = {}
        recepcion_compra = RecepcionCompra.objects.get(id = pk)
        context['contexto_recepcion_compra'] = recepcion_compra
        context['materiales'] = recepcion_compra.content_type.model_class().objects.ver_detalle(recepcion_compra.id_registro)
        context['archivos'] = ArchivoRecepcionCompra.objects.filter(recepcion_compra=recepcion_compra)
        context['fotos'] = FotoRecepcionCompra.objects.filter(recepcion_compra=recepcion_compra)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RecepcionCompraAnularView(BSModalUpdateView):
    model = RecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = RecepcionCompraAnularForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            documento = form.instance.documento
            detalles = documento.detalle
            for detalle in detalles:
                movimiento_dos = MovimientosAlmacen.objects.get(
                    content_type_producto = detalle.orden_compra_detalle.content_type,
                    id_registro_producto = detalle.orden_compra_detalle.id_registro,
                    cantidad = detalle.cantidad,
                    signo_factor_multiplicador = +1,
                    content_type_documento_proceso = ContentType.objects.get_for_model(form.instance),
                    id_registro_documento_proceso = form.instance.id,
                    almacen = None,
                    sociedad = documento.sociedad,
                    movimiento_reversion = False,
                )

                movimiento_uno = movimiento_dos.movimiento_anterior

                movimiento_dos.delete()
                movimiento_uno.delete()

            form.instance.estado = 2
            registro_guardar(form.instance, self.request)
            documento.estado=1
            registro_guardar(documento, self.request)
            documento.save()
            messages.success(self.request, MENSAJE_ANULAR_CONTEO)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RecepcionCompraAnularView, self).get_context_data(**kwargs)
        context['accion'] = "Anular"
        context['titulo'] = "Conteo"
        return context


class ArchivoRecepcionCompraCreateView(BSModalCreateView):
    model = ArchivoRecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = ArchivoRecepcionCompraForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.recepcion_compra = RecepcionCompra.objects.get(pk=self.kwargs['pk'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ArchivoRecepcionCompraCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        return context
    

class ArchivoRecepcionCompraDeleteView(BSModalDeleteView):
    model = ArchivoRecepcionCompra
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.recepcion_compra.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoRecepcionCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Archivo"
        context['item'] = filename(self.object.archivo)
        return context


class FotoRecepcionCompraCreateView(BSModalCreateView):
    model = FotoRecepcionCompra
    template_name = "includes/formulario generico.html"
    form_class = FotoRecepcionCompraForm
    success_url = '.'

    def form_valid(self, form):
        form.instance.recepcion_compra = RecepcionCompra.objects.get(pk=self.kwargs['pk'])
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(FotoRecepcionCompraCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Foto"
        return context
    

class FotoRecepcionCompraDeleteView(BSModalDeleteView):
    model = FotoRecepcionCompra
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('recepcion_compra_app:recepcion_compra_detalle', kwargs={'pk':self.object.recepcion_compra.id})

    def get_context_data(self, **kwargs):
        context = super(FotoRecepcionCompraDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Foto"
        context['item'] = filename(self.object.foto)
        return context


class RecepcionCompraGenerarNotaIngresoView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = RecepcionCompraGenerarNotaIngresoForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('nota_ingreso_app:nota_ingreso_detalle', kwargs={'pk':self.kwargs['nota'].id})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                recepcion_compra = RecepcionCompra.objects.get(id=self.kwargs['pk'])
                numero_nota = len(NotaIngreso.objects.all()) + 1
                nota = NotaIngreso.objects.create(
                    nro_nota_ingreso = numeroXn(numero_nota, 6),
                    content_type=ContentType.objects.get_for_model(recepcion_compra),
                    id_registro=recepcion_compra.id,
                    sociedad = recepcion_compra.sociedad,
                    fecha_ingreso = form.cleaned_data['fecha_ingreso'],
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                self.kwargs['nota']=nota
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RecepcionCompraGenerarNotaIngresoView, self).get_context_data(**kwargs)
        context['accion'] = "Recibir"
        context['titulo'] = "Comprobante de Compra"
        return context
