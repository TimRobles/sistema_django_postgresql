from datetime import timedelta
from reportlab.lib import colors
from applications.clientes.models import Cliente
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda
from applications.importaciones import *
from .models import(
    Deuda,
    LineaCredito,
)

from .forms import(
    LineaCreditoForm,
)

class LineaCreditoView(ListView):
    model = LineaCredito
    template_name = 'cobranza/linea_credito/inicio.html'
    context_object_name = 'contexto_linea_credito'

def LineaCreditoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cobranza/linea_credito/inicio_tabla.html'
        context = {}
        context['contexto_linea_credito'] = LineaCredito.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class LineaCreditoCreateView(BSModalCreateView):
    model = LineaCredito
    template_name = "cobranza/linea_credito/form.html"
    form_class = LineaCreditoForm
    success_url = reverse_lazy('cobranza_app:linea_credito_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LineaCreditoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Linea de Crédito"
        return context


class DeudoresView(TemplateView):
    template_name = "cobranza/deudas/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super(DeudoresView, self).get_context_data(**kwargs)
        context['contexto_cliente'] = Cliente.objects.all()
        context['moneda'] = Moneda.objects.get(principal=True)
        return context
    

class DeudaView(TemplateView):
    template_name = "cobranza/deudas/detalle.html"
    
    def get_context_data(self, **kwargs):
        context = super(DeudaView, self).get_context_data(**kwargs)
        deudas = Deuda.objects.filter(cliente__id=self.kwargs['id_cliente'])
        for deuda in deudas:
            if deuda.content_type:
                deuda.documento = '%s F001-000100' % (deuda.content_type.name)
            if deuda.fecha_vencimiento > (date.today() + timedelta(5)):
                deuda.estado = 'PENDIENTE'
                deuda.color = "#" + colors.green.hexval()[2:]
            elif deuda.fecha_vencimiento < date.today():
                deuda.estado = 'VENCIDO'
                deuda.color = "#" + colors.red.hexval()[2:]
            else:
                deuda.estado = '%s DÍAS PARA VENCER' % ((deuda.fecha_vencimiento - date.today()).days)
                deuda.color = "#" + colors.orange.hexval()[2:]
            
        context['contexto_deuda'] = deudas
        return context


class CuentaBancariaView(TemplateView):
    template_name = "bancos/cuenta bancaria/inicio.html"

    
    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaView, self).get_context_data(**kwargs)
        context['contexto_cuenta_bancaria'] = CuentaBancariaSociedad.objects.filter(estado=1)
        return context
    