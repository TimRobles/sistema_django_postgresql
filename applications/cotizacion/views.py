from django.shortcuts import render
from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.funciones import calculos_linea
from applications.importaciones import *
from django import forms

from .forms import (
    CotizacionVentaClienteForm,
    CotizacionVentaForm,
    CotizacionVentaMaterialDetalleForm,
)
    
from .models import (
    CotizacionVenta,
    CotizacionVentaDetalle,
)


class CotizacionVentaListView(ListView):
    model = CotizacionVenta
    template_name = ('cotizacion/cotizacion_venta/inicio.html')
    context_object_name = 'contexto_cotizacion_venta'

def CotizacionVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/inicio_tabla.html'
        context = {}
        context['contexto_cotizacion_venta'] = CotizacionVenta.objects.all()
                
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)   


def CotizacionVentaCreateView(request):
    obj = CotizacionVenta.objects.create()
    return HttpResponseRedirect(reverse_lazy('cotizacion_app:cotizacion_venta_ver', kwargs={'id_cotizacion':obj.id}))


class CotizacionVentaVerView(TemplateView):
    template_name = "cotizacion/cotizacion_venta/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = CotizacionVenta.objects.get(id = kwargs['id_cotizacion'])
        materiales = None
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass


        context = super(CotizacionVentaVerView, self).get_context_data(**kwargs)
        context['cotizacion'] = obj
        context['materiales'] = materiales
        return context


def CotizacionVentaVerTabla(request, id_cotizacion):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/inicio_tabla.html'
        context = {}
        context['contexto_cotizacion_venta'] = CotizacionVenta.objects.all()
        
                
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data) 


class CotizacionVentaClienteView(BSModalUpdateView):
    model = CotizacionVenta
    template_name = "cotizacion/cotizacion_venta/form_cliente.html"
    form_class = CotizacionVentaClienteForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cotizacion = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = cotizacion.cliente)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = cotizacion.cliente_interlocutor
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaClienteView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Cliente"
        return context


class ClienteInterlocutorForm(forms.Form):
    cliente_interlocutor = forms.ModelChoiceField(queryset = ClienteInterlocutor.objects.all(), required=False)

def ClienteInterlocutorView(request, id_cliente):
    form = ClienteInterlocutorForm()
    lista = []
    relaciones = ClienteInterlocutor.objects.filter(cliente = id_cliente)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)

    form.fields['cliente_interlocutor'].queryset = InterlocutorCliente.objects.filter(id__in = lista)
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


def CotizacionVentaDetalleTabla(request, cotizacion_id):
    data = dict()
    if request.method == 'GET':
        template = 'cotizacion/cotizacion_venta/detalle_tabla.html'
        context = {}
        obj = CotizacionVenta.objects.get(id = cotizacion_id)

        materiales = None
        print("***********************************")
        try:
            materiales = obj.CotizacionVentaDetalle_cotizacion_venta.all()
            print(materiales)

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
            print("***********************************")
        except:
            pass

        context['materiales'] = materiales
        context['cotizacion'] = obj

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class CotizacionVentaMaterialDetalleView(BSModalFormView):

    template_name = "cotizacion/cotizacion_venta/form_material.html"
    form_class = CotizacionVentaMaterialDetalleForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def form_valid(self, form):
        
        if self.request.session['primero']:
            cotizacion = CotizacionVenta.objects.get(id = self.kwargs['cotizacion_id'])
            item = len(CotizacionVentaDetalle.objects.filter(cotizacion_venta = cotizacion))

            material = form.cleaned_data.get('material')
            cantidad = form.cleaned_data.get('cantidad')

            obj, created = CotizacionVentaDetalle.objects.get_or_create(
                content_type = ContentType.objects.get_for_model(material),
                id_registro = material.id,
                cotizacion_venta = cotizacion,
            )
            if created:
                obj.item = item + 1
                obj.cantidad = cantidad
                try:
                    precio_unitario_con_igv = material.precio_lista.precio_lista
                    precio_final_con_igv = material.precio_lista.precio_lista
                except:
                    precio_unitario_con_igv = 0
                    precio_final_con_igv = 0

                respuesta = calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, 0.18)
                obj.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
                obj.precio_unitario_con_igv = precio_unitario_con_igv
                obj.precio_final_con_igv = precio_final_con_igv
                obj.sub_total = respuesta['subtotal']
                obj.descuento = respuesta['descuento']
                obj.igv = respuesta['igv']
                obj.total = respuesta['total']
            else:
                precio_unitario_con_igv = obj.precio_unitario_con_igv
                precio_final_con_igv = obj.precio_final_con_igv
                obj.cantidad = obj.cantidad + cantidad
                respuesta = calculos_linea(obj.cantidad, precio_unitario_con_igv, precio_final_con_igv, 0.18)
                obj.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
                obj.precio_unitario_con_igv = precio_unitario_con_igv
                obj.precio_final_con_igv = precio_final_con_igv
                obj.sub_total = respuesta['subtotal']
                obj.descuento = respuesta['descuento']
                obj.igv = respuesta['igv']
                obj.total = respuesta['total']

            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CotizacionVentaMaterialDetalleView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar'
        context['accion'] = 'Material'
        return context
