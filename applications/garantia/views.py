from django import forms
from applications.importaciones import*

from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente


from .models import(
    IngresoReclamoGarantia,
    ControlCalidadReclamoGarantia,
    SalidaReclamoGarantia,
)
from .forms import(
    IngresoGarantiaBuscarForm,
)


class IngresoGarantiaListView(FormView):
    template_name = 'garantia/ingreso_garantia/inicio.html'
    form_class = IngresoGarantiaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(IngresoGarantiaListView, self).get_form_kwargs()
        kwargs['fecha_ingreso'] = self.request.GET.get('fecha_ingreso')
        kwargs['numero_ingreso_garantia'] = self.request.GET.get('numero_ingreso_garantia')
        kwargs['cliente'] = self.request.GET.get('cliente')
        kwargs['sociedad'] = self.request.GET.get('sociedad')
        kwargs['estado'] = self.request.GET.get('estado')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(IngresoGarantiaListView, self).get_context_data(**kwargs)
        ingreso_garantia = IngresoReclamoGarantia.objects.all()
        filtro_fecha_ingreso = self.request.GET.get('fecha_ingreso')
        filtro_numero_ingreso_garantia = self.request.GET.get('numero_ingreso_garantia')
        filtro_cliente = self.request.GET.get('cliente')
        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_estado = self.request.GET.get('estado')

        contexto_filtro = []
        if filtro_fecha_ingreso:
            condicion = Q(fecha_ingreso = filtro_fecha_ingreso)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("fecha_ingreso=" + filtro_fecha_ingreso)
        if filtro_numero_ingreso_garantia:
            condicion = Q(numero_ingreso_garantia = filtro_numero_ingreso_garantia)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("numero_ingreso_garantia=" + filtro_numero_ingreso_garantia)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        if filtro_sociedad:
            condicion = Q(sociedad = filtro_sociedad)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)
        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['contexto_ingreso_garantia'] = ingreso_garantia
        return context
    

def IngresoGarantiaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/ingreso_garantia/inicio_tabla.html'
        context = {}        
        ingreso_garantia = IngresoReclamoGarantia.objects.all()
        filtro_fecha_ingreso = request.GET.get('fecha_ingreso')
        filtro_numero_ingreso_garantia = request.GET.get('numero_ingreso_garantia')
        filtro_cliente = request.GET.get('cliente')
        filtro_sociedad = request.GET.get('sociedad')
        filtro_estado = request.GET.get('estado')

        contexto_filtro = []
        if filtro_fecha_ingreso:
            condicion = Q(fecha_ingreso = filtro_fecha_ingreso)
            guias = guias.filter(condicion)
            contexto_filtro.append("fecha_ingreso=" + filtro_fecha_ingreso)
        if filtro_numero_ingreso_garantia:
            condicion = Q(numero_ingreso_garantia = filtro_numero_ingreso_garantia)
            guias = guias.filter(condicion)
            contexto_filtro.append("numero_ingreso_garantia=" + filtro_numero_ingreso_garantia)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            guias = guias.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        if filtro_sociedad:
            condicion = Q(sociedad = filtro_sociedad)
            guias = guias.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)
        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            guias = guias.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['contexto_ingreso_garantia'] = ingreso_garantia
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)