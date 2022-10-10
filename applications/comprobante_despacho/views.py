import requests
from django import forms
from applications.importaciones import*
from applications.logistica.models import Despacho
from applications.envio_clientes.models import Transportista
from applications.datos_globales.models import SeriesComprobante

from .models import(
    Guia,
    GuiaDetalle,
)

from .forms import(
    GuiaBultosForm,
    GuiaDestinoForm,
    GuiaPartidaForm,
    GuiaTransportistaForm,
)


class GuiaListView(ListView):
    model = Guia
    template_name = 'comprobante_despacho/guia/inicio.html'
    context_object_name = 'contexto_guia'

def GuiaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_despacho/guia/inicio_tabla.html'
        context = {}
        context['contexto_guia'] = Guia.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class GuiaDetalleView(TemplateView):
    template_name = "comprobante_despacho/guia/detalle.html"

    def get_context_data(self, **kwargs):
        obj = Guia.objects.get(id = kwargs['id_guia'])

        materiales = None
        try:
            materiales = obj.GuiaDetalle_guia_venta.all()
            print('*****************************************')
            print(materiales)
            print('*****************************************')

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass
        
        context = super(GuiaDetalleView, self).get_context_data(**kwargs)
        context['guia'] = obj
        context['materiales'] = materiales

        return context

def GuiaDetalleVerTabla(request, id_guia):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_despacho/guia/detalle_tabla.html'
        obj = Guia.objects.get(id=id_guia)

        materiales = None
        try:
            materiales = obj.GuiaDetalle_factura_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = {}
        context['guia'] = obj
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class GuiaCrearView(DeleteView):
    model = Despacho
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':self.object.id})
   
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        detalles = self.object.DespachoDetalle_despacho.all()

        serie_comprobante = SeriesComprobante.objects.filter(tipo_comprobante=ContentType.objects.get_for_model(Guia)).earliest('created_at')

        guia = Guia.objects.create(
            sociedad = self.object.sociedad,
            serie_comprobante = serie_comprobante,
            cliente = self.object.cliente,
            created_by = self.request.user,
            updated_by = self.request.user,
        )

        for detalle in detalles:
            guia_detalle = GuiaDetalle.objects.create(
                item = detalle.item,
                guia=guia,
                created_by=self.request.user,
                updated_by=self.request.user,                
            )

        registro_guardar(self.object, self.request)
        self.object.save()

        messages.success(request, MENSAJE_GENERAR_GUIA)
        return HttpResponseRedirect(reverse_lazy('comprobante_despacho_app:guia_detalle', kwargs={'id_guia':guia.id}))

    def get_context_data(self, **kwargs):
        context = super(GuiaCrearView, self).get_context_data(**kwargs)
        context['accion'] = 'Generar'
        context['titulo'] = 'Guía'
        context['texto'] = '¿Seguro que desea generar Guía?'
        context['item'] = str(self.object.cliente) 
        return context

class GuiaTransportistaView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form.html"
    form_class = GuiaTransportistaForm
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaTransportistaView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Transportista"
        return context


class GuiaPartidaView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form.html"
    form_class = GuiaPartidaForm
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaPartidaView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Dirección de Partida"
        return context


class GuiaDestinoView(BSModalUpdateView):
    model = Guia
    template_name = "comprobante_despacho/guia/form.html"
    form_class = GuiaDestinoForm
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaDestinoView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Dirección de Destino"
        return context

class GuiaBultosView(BSModalUpdateView):
    model = Guia
    template_name = "includes/form generico.html"
    form_class = GuiaBultosForm
    success_url = reverse_lazy('comprobante_despacho_app:guia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GuiaBultosView, self).get_context_data(**kwargs)
        context['accion'] = "Asignar"
        context['titulo'] = "Número de Bultos"
        return context