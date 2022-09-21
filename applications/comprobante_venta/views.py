from urllib import request
from django.shortcuts import render
from applications.cotizacion.models import ConfirmacionVenta
from applications.funciones import slug_aleatorio
from applications.importaciones import *

from . models import(
    FacturaVenta,
    FacturaVentaDetalle,
)

class FacturaVentaListView(ListView):
    model = FacturaVenta
    template_name = 'comprobante_venta/factura_venta/inicio.html'
    context_object_name = 'contexto_factura_venta'

def FacturaVentaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/factura_venta/inicio_tabla.html'
        context = {}
        context['contexto_factura_venta'] = FacturaVenta.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class FacturaVentaDetalleView(TemplateView):
    template_name = "comprobante_venta/factura_venta/detalle.html"

    def get_context_data(self, **kwargs):
        obj = FacturaVenta.objects.get(id = kwargs['id_factura_venta'])

        materiales = None
        try:
            materiales = obj.FacturaVentaDetalle_factura_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = super(FacturaVentaDetalleView, self).get_context_data(**kwargs)
        context['factura'] = obj
        context['materiales'] = materiales

        return context


def FacturaVentaDetalleVerTabla(request, id_factura_venta):
    data = dict()
    if request.method == 'GET':
        template = 'comprobante_venta/factura_venta/detalle_tabla.html'
        obj = FacturaVenta.objects.get(id=id_factura_venta)

        materiales = None
        try:
            materiales = obj.FacturaVentaDetalle_factura_venta.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = {}
        context['factura'] = obj
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)




class FacturaVentaCrearView(DeleteView):
    model = ConfirmacionVenta
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('comprobante_venta_app:factura_venta_detalle', kwargs={'id_factura_venta':self.object.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        print('*********************')
        print(self.object)
        print('*********************')

        detalles = self.object.ConfirmacionVentaDetalle_confirmacion_venta.all()

        factura_venta = FacturaVenta.objects.create(
            sociedad = self.object.sociedad,
            tipo_cambio = self.object.tipo_cambio,
            observaciones = self.object.observacion,
            condiciones_pago = self.object.condiciones_pago,
            tipo_venta = self.object.tipo_venta,
            descuento_global = self.object.descuento_global,
            otros_cargos = self.object.otros_cargos,
            total = self.object.total,
            slug = slug_aleatorio(FacturaVenta),
            created_by=self.request.user,
            updated_by=self.request.user,
        )
        

        for detalle in detalles:
            factura_venta_detalle = FacturaVentaDetalle.objects.create(
            item=detalle.item,
            content_type=detalle.content_type,
            id_registro=detalle.id_registro,
            cantidad=detalle.cantidad_confirmada,
            precio_unitario_sin_igv=detalle.precio_unitario_sin_igv,
            precio_unitario_con_igv=detalle.precio_unitario_con_igv,
            precio_final_con_igv=detalle.precio_final_con_igv,
            descuento=detalle.descuento,
            sub_total=detalle.sub_total,
            igv=detalle.igv,
            total=detalle.total,
            tipo_igv=detalle.tipo_igv,
            factura_venta=factura_venta,
            created_by=self.request.user,
            updated_by=self.request.user,
            )

        messages.success(request, MENSAJE_CLONAR_COTIZACION)
        # return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse_lazy('comprobante_venta_app:factura_venta_detalle', kwargs={'id_factura_venta':factura_venta.id}))

