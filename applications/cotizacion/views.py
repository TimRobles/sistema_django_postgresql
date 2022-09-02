from django.shortcuts import render
from applications.importaciones import *
from applications.clientes.forms import Cliente

from .forms import (
    CotizacionVentaForm,
    ClienteForm,
)
    
from .models import (
    PrecioListaMaterial,
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
        context['contexto_cotizacion_venta'] = CotizacionVentaListView.objects.all()
                
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)   


class CotizacionVentaCreateView(FormView):
    template_name = "cotizacion/cotizacion_venta/detalle.html"
    form_class = CotizacionVentaForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def form_valid(self, form):
        obj = CotizacionVenta.objects.get(
            
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CotizacionVentaCreateView, self).get_context_data(**kwargs)
        context['cliente'] = Cliente.objects.all()
        context['cotizacion'] = CotizacionVenta.objects.all()
        return context

class ClienteView(BSModalUpdateView):
    model = Cliente
    template_name = "includes/formulario generico.html"
    form_class = ClienteForm
    success_url = reverse_lazy('cotizacion_app:cotizacion_venta_inicio')

    def form_valid(self, form):
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super(ClienteView, self).get_context_data(**kwargs)
        context['cliente'] = Cliente.objects.all()
        context['cotizacion'] = CotizacionVenta.objects.all()
        context['accion'] = "Elegir"
        context['titulo'] = "Cliente"
        return context
