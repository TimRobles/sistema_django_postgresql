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
        context['contexto_subfamilia'] = sub_familia

        return context

class FallaMaterialCreateView(BSModalCreateView):
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('calidad_app:falla_material_detalle', kwargs={'id_sub_familia':self.kwargs['id_sub_familia']})
    
    def form_valid(self, form):
        sub_familia = SubFamilia.objects.get(id = self.kwargs['id_sub_familia'])
        form.instance.sub_familia = sub_familia
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        sub_familia = SubFamilia.objects.get(id = self.kwargs['id_sub_familia'])
        kwargs = super(FallaMaterialCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['sub_familia'] = sub_familia
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(FallaMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Falla"
        return context

class FallaMaterialUpdateView(BSModalUpdateView):
    model = FallaMaterial
    template_name = "includes/formulario generico.html"
    form_class = FallaMaterialForm
    # success_url = reverse_lazy('calidad_app:falla_material')

    def get_success_url(self, **kwargs):
        print('****************************')
        print(self.object)
        print(self.object.sub_familia)
        print('****************************')
        return reverse_lazy('calidad_app:falla_material_detalle', kwargs={'id_sub_familia':self.object.sub_familia.id})

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Falla"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class FallaMaterialDeleteView(BSModalDeleteView):
    model = FallaMaterial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('calidad_app:falla_material')

    def get_context_data(self, **kwargs):
        context = super(FallaMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Falla"
        context['item'] = self.object.titulo
        return context