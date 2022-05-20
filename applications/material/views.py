from applications.importaciones import *
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat
from django import forms
from django.shortcuts import render

from .forms import (
    ModeloForm, MarcaForm,MaterialForm, 
    RelacionMaterialComponenteForm,EspecificacionForm, DatasheetForm,DatosImportacionForm,ProductoSunatForm,
    )
from .models import (
    Modelo, 
    Marca,
    Material,
    RelacionMaterialComponente,
    Especificacion,
    Datasheet,
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


class MaterialListView(ListView):
    model = Material
    template_name = "material/material/inicio.html"
    context_object_name = 'contexto_material'

def MaterialTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'material/material/inicio_tabla.html'
        context = {}
        context['contexto_material'] = Material.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class MaterialCreateView(BSModalCreateView):
    model = Material
    template_name = "includes/formulario generico.html"
    form_class = MaterialForm 
    success_url = reverse_lazy('material_app:material_inicio')

    def get_context_data(self, **kwargs):
        context = super(MaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        return context
        

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class MaterialUpdateView(BSModalUpdateView):
    model = Material
    template_name = "includes/formulario generico.html"
    form_class = MaterialForm
    success_url = reverse_lazy('material_app:material_inicio')

    def get_context_data(self, **kwargs):
        context = super(MaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)

class MaterialDarBajaView(BSModalDeleteView):
    model = Material
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('material_app:material_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MaterialDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Materiales"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_venta
        return context

class MaterialDarAltaView(BSModalDeleteView):
    model = Material
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('material_app:material_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MaterialDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Material"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_venta
        return context


class MaterialDetailView(DetailView):
    model = Material
    template_name = "material/material/detalle.html"
    context_object_name = 'contexto_material'

    def get_context_data(self, **kwargs):
        material = Material.objects.get(id = self.kwargs['pk'])
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        context['componentes'] = RelacionMaterialComponente.objects.filter(material = material)
        context['especificaciones'] = Especificacion.objects.filter(material = material)
        context['datasheets'] = Datasheet.objects.filter(material = material)
        return context

def MaterialDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'material/material/detalle_tabla.html'
        context = {}
        material = Material.objects.get(id = pk)
        context['contexto_material'] = material
        context['componentes'] = RelacionMaterialComponente.objects.filter(material = material)
        context['especificaciones'] = Especificacion.objects.filter(material = material)
        context['datasheets'] = Datasheet.objects.filter(material = material)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ComponenteCreateView(BSModalCreateView):
    model = RelacionMaterialComponente
    template_name = "includes/formulario generico.html"
    form_class = RelacionMaterialComponenteForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        material = Material.objects.get(id = self.kwargs['material_id'])
        kwargs = super(ComponenteCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['componentes'] = material.subfamilia.componentes.all()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ComponenteCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Componente"
        return context

class ComponenteUpdateView(BSModalUpdateView):
    model = RelacionMaterialComponente
    template_name = "includes/formulario generico.html"
    form_class = RelacionMaterialComponenteForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComponenteUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Componentes"
        return context

class ComponenteDeleteView(BSModalDeleteView):
    model = RelacionMaterialComponente
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_context_data(self, **kwargs):
        context = super(ComponenteDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Componente"
        return context

class EspecificacionCreateView(BSModalCreateView):
    model = Especificacion
    template_name = "includes/formulario generico.html"
    form_class = EspecificacionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        material = Material.objects.get(id = self.kwargs['material_id'])
        kwargs = super(EspecificacionCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['atributos'] = material.subfamilia.familia.atributos.all()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EspecificacionCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Especificación"
        return context     

class EspecificacionUpdateView(BSModalUpdateView):
    model = Especificacion
    template_name = "includes/formulario generico.html"
    form_class = EspecificacionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EspecificacionUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Especificación"
        return context

class EspecificacionDeleteView(BSModalDeleteView):
    model = Especificacion
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_context_data(self, **kwargs):
        context = super(EspecificacionDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Especificación"
        return context

class DatasheetCreateView(BSModalCreateView):
    model = Datasheet
    template_name = "includes/formulario generico.html"
    form_class = DatasheetForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatasheetCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Datasheet"
        return context     

class DatasheetUpdateView(BSModalUpdateView):
    model = Datasheet
    template_name = "includes/formulario generico.html"
    form_class = DatasheetForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatasheetUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Especificación"
        return context

class DatasheetDeleteView(BSModalDeleteView):
    model = Datasheet
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_context_data(self, **kwargs):
        context = super(DatasheetDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Especificación"
        return context

class DatosImportacionUpdateView(BSModalUpdateView):
    model = Material
    template_name = "includes/formulario generico.html"
    form_class = DatosImportacionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatosImportacionUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Importaciones"
        return context

class ProductoSunatUpdateView(BSModalUpdateView):
    model = Material
    template_name = "material/material/form.html"
    form_class = ProductoSunatForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoSunatUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Producto Sunat"
        return context

class FamiliaSunatForm(forms.Form):
    familia = forms.ModelChoiceField(queryset = FamiliaSunat.objects.all(), required=False, empty_label=None)

def FamiliaSunatView(request, id_segmento):
    form = FamiliaSunatForm()
    form.fields['familia'].queryset = FamiliaSunat.objects.filter(segmento = id_segmento)
    return render(request, 'includes/form.html', context={'form':form})

class ClaseSunatForm(forms.Form):
    clase = forms.ModelChoiceField(queryset = ClaseSunat.objects.all(), required=False, empty_label=None)

def ClaseSunatView(request, id_familia):
    form = ClaseSunatForm()
    form.fields['clase'].queryset = ClaseSunat.objects.filter(familia = id_familia)
    return render(request, 'includes/form.html', context={'form':form})

class ProductoSunatForm(forms.Form):
    producto = forms.ModelChoiceField(queryset = ProductoSunat.objects.all(), required=False, empty_label=None)

def ProductoSunatView(request, id_clase):
    form = ProductoSunatForm()
    form.fields['producto'].queryset = ProductoSunat.objects.filter(clase = id_clase)
    return render(request, 'includes/form.html', context={'form':form})