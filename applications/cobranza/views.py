from datetime import timedelta
from reportlab.lib import colors
from applications.clientes.models import Cliente
from applications.cobranza.funciones import movimientos_bancarios
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda
from applications.importaciones import *
from .models import(
    Deuda,
    Ingreso,
    LineaCredito,
    Pago,
)

from .forms import(
    CuentaBancariaIngresoForm,
    CuentaBancariaIngresoPagarForm,
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
            
        context['contexto_deuda'] = deudas
        return context


class CuentaBancariaView(TemplateView):
    template_name = "bancos/cuenta bancaria/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaView, self).get_context_data(**kwargs)
        context['contexto_cuenta_bancaria'] = CuentaBancariaSociedad.objects.filter(estado=1)
        return context


class CuentaBancariaDetalleView(DetailView):
    model = CuentaBancariaSociedad
    template_name = "bancos/cuenta bancaria/detalle.html"
    context_object_name = 'cuenta_bancaria'

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaDetalleView, self).get_context_data(**kwargs)
        context['movimientos'] = movimientos_bancarios(self.object.id)
        return context
    

class CuentaBancariaIngresoPagarView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaIngresoPagarForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            deuda = form.cleaned_data.get('deuda')
            monto = form.cleaned_data.get('monto')
            tipo_cambio = form.cleaned_data.get('tipo_cambio')
            content_type = ContentType.objects.get_for_model(Ingreso)
            id_registro = self.kwargs['id_ingreso']
            obj, created = Pago.objects.get_or_create(
                deuda = deuda,
                content_type = content_type,
                id_registro = id_registro,
            )
            if created:
                obj.monto = monto
            else:
                obj.monto = obj.monto + monto
            obj.tipo_cambio = tipo_cambio
            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaIngresoPagarView, self).get_context_data(**kwargs)
        context['accion'] = 'Pagar'
        context['titulo'] = 'Deuda'
        return context
    

class CuentaBancariaIngresoView(BSModalCreateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaIngresoForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        cuenta_bancaria = CuentaBancariaSociedad.objects.get(id=self.kwargs['id_cuenta_bancaria'])
        form.instance.cuenta_bancaria = cuenta_bancaria
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaIngresoView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaIngresoUpdateView(BSModalUpdateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaIngresoForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaIngresoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaIngresoDeleteView(BSModalDeleteView):
    model = Ingreso
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaIngresoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Ingreso'
        context['item'] = self.get_object()
        return context
    

