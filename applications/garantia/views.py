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
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(IngresoGarantiaListView, self).get_context_data(**kwargs)
        ingreso_garantia = IngresoReclamoGarantia.objects.all()


        context['contexto_ingreso_garantia'] = ingreso_garantia
        return context
    

def IngresoGarantiaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/ingreso_garantia/inicio_tabla.html'
        context = {}        
        ingreso_garantia = IngresoReclamoGarantia.objects.all()

        context['contexto_ingreso_garantia'] = ingreso_garantia
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)