from applications.importaciones import *
from .forms import (
    ModeloForm, MarcaForm
    )
from .models import (
    Modelo, 
    Marca,
    )

class ModeloListView(PermissionRequiredMixin, ListView):
    permission_required = ('material.view_modelo')

    model = Modelo
    template_name = "material/modelo/inicio.html"
    context_object_name = 'contexto_modelo'

def ModeloTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'material/modelo/inicio_tabla.html'
        context = {}
        context['contexto_modelo'] = Modelo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ModeloCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('material.add_modelo')
    model = Modelo
    template_name = "includes/formulario generico.html"
    form_class = ModeloForm 
    success_url = reverse_lazy('material_app:modelo_inicio')

    def get_context_data(self, **kwargs):
        context = super(ModeloCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Modelo"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class ModeloUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('material.change_modelo')

    model = Modelo
    template_name = "includes/formulario generico.html"
    form_class = ModeloForm
    success_url = reverse_lazy('material_app:modelo_inicio')

    def get_context_data(self, **kwargs):
        context = super(ModeloUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Modelo"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)
        
class MarcaListView(PermissionRequiredMixin, ListView):
    permission_required = ('material.view_marca')

    model = Marca
    template_name = "material/marca/inicio.html"
    context_object_name = 'contexto_marca'

def MarcaTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'material/marca/inicio_tabla.html'
        context = {}
        context['contexto_marca'] = Marca.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class MarcaCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('material.add_marca')
    model = Marca
    template_name = "includes/formulario generico.html"
    form_class = MarcaForm 
    success_url = reverse_lazy('material_app:marca_inicio')

    def get_context_data(self, **kwargs):
        context = super(MarcaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Marca"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class MarcaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('material.change_marca')

    model = Marca
    template_name = "includes/formulario generico.html"
    form_class = MarcaForm
    success_url = reverse_lazy('material_app:marca_inicio')

    def get_context_data(self, **kwargs):
        context = super(MarcaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Marca"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)