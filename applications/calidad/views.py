from urllib import request
from django.shortcuts import render
from applications.importaciones import*
from applications.material.models import SubFamilia
from applications.calidad.forms import FallaMaterialForm
from .models import(
    EstadoSerie,
    Serie,
    FallaMaterial,
    HistorialEstadoSerie,
)

class FallaMaterialListView(ListView):
    model = FallaMaterial
    template_name = "calidad/falla_material/inicio.html"
    context_object_name = 'contexto_falla_material'
    
    def get_context_data(self, **kwargs):
        context = super(FallaMaterialListView, self).get_context_data(**kwargs)
        context['contexto_subfamilia'] = SubFamilia.objects.all()
        return context
    

def FallaMaterialTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'calidad/falla_material/inicio_tabla.html'
        context = {}

        context['contexto_falla_material'] = FallaMaterial.objects.all()
        context['contexto_subfamilia'] = SubFamilia.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class FallaMaterialDetalleView(TemplateView):
    template_name = "calidad/falla_material/detalle.html"

    def get_context_data(self, **kwargs):
        sub_familia = SubFamilia.objects.get(id=self.kwargs['id_sub_familia'])
        fallas = FallaMaterial.objects.filter(sub_familia = sub_familia)

        context = super(FallaMaterialDetalleView, self).get_context_data(**kwargs)
        context['fallas'] = fallas

        return context

class FallaMaterialCreateView(BSModalCreateView):
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle', kwargs={'pk':self.kwargs['falla_material_id']})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Falla"
        return context