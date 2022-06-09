from applications.importaciones import *
from django import forms

from applications.proveedores.models import InterlocutorProveedor, Proveedor

from .forms import (
    RequerimientoMaterialForm,
    RequerimientoMaterialDetalleForm,
    RequerimientoMaterialDetalleUpdateForm,
)

from .models import (
    RequerimientoMaterial,
    ProveedorInterlocutor,
    RequerimientoMaterialDetalle,
)

class RequerimientoMaterialListView(ListView):
    model = RequerimientoMaterial
    template_name = "requerimiento_material/requerimiento_material/inicio.html"
    context_object_name = 'contexto_requerimiento_material'

def RequerimientoMaterialTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'requerimiento_material/requerimiento_material/inicio_tabla.html'
        context = {}
        context['contexto_requerimiento_material'] = RequerimientoMaterial.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RequerimientoMaterialCreateView(FormView):
    template_name = "requerimiento_material/requerimiento_material/detalle.html"
    form_class = RequerimientoMaterialForm 
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_inicio')
    global obj

    def form_valid(self, form):
        global obj
        obj.titulo = form.cleaned_data['titulo']
        obj.proveedor = form.cleaned_data['proveedor']
        obj.interlocutor_proveedor = form.cleaned_data['interlocutor_proveedor']
        registro_guardar(obj, self.request)
        obj.save()

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RequerimientoMaterialCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['titulo'] = None
        kwargs['proveedor'] = None
        kwargs['interlocutor'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        global obj
        context = super(RequerimientoMaterialCreateView, self).get_context_data(**kwargs)
        obj, created = RequerimientoMaterial.objects.get_or_create(
            titulo = None,
            proveedor = None,
            interlocutor_proveedor = None,
            created_by = self.request.user,
        )
        if obj.updated_by == None:
            obj.updated_by = self.request.user
            obj.save()

        materiales = None
        try:
            obj.RequerimientoMaterialDetalle_requerimiento_material
            materiales = obj.RequerimientoMaterialDetalle_requerimiento_material.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass
        context['requerimiento'] = obj
        context['creado'] = created
        context['materiales'] = materiales
        return context

def RequerimientoMaterialDetalleTabla(request, requerimiento_id):
    data = dict()
    if request.method == 'GET':
        template = 'requerimiento_material/requerimiento_material/detalle_tabla.html'
        context = {}
        obj = RequerimientoMaterial.objects.get(id = requerimiento_id)
        instance = {}
        instance['titulo'] = obj.titulo
        instance['proveedor'] = obj.proveedor
        instance['interlocutor'] = obj.interlocutor_proveedor
        
        materiales = None
        try:
            materiales = obj.RequerimientoMaterialDetalle_requerimiento_material.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)

        except:
            pass
        context['requerimiento'] = obj
        context['materiales'] = materiales
        context['form'] = RequerimientoMaterialForm(instance=instance)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RequerimientoMaterialUpdateView(FormView):
    template_name = "requerimiento_material/requerimiento_material/detalle.html"
    form_class = RequerimientoMaterialForm 
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_inicio')

    def form_valid(self, form):
        obj = RequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        titulo = form.cleaned_data['titulo']
        proveedor = form.cleaned_data['proveedor']
        interlocutor_proveedor = form.cleaned_data['interlocutor_proveedor']
        obj.titulo = titulo
        obj.proveedor = proveedor
        obj.interlocutor_proveedor = interlocutor_proveedor

        registro_guardar(obj, self.request)
        obj.save()

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        requerimiento = RequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        kwargs = super(RequerimientoMaterialUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['titulo'] = requerimiento.titulo
        kwargs['proveedor'] = requerimiento.proveedor
        kwargs['interlocutor'] = requerimiento.interlocutor_proveedor
        return kwargs

    def get_context_data(self, **kwargs):
        requerimiento = RequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        materiales = None
        try:
            requerimiento.RequerimientoMaterialDetalle_requerimiento_material
            materiales = requerimiento.RequerimientoMaterialDetalle_requerimiento_material.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass
        context = super(RequerimientoMaterialUpdateView, self).get_context_data(**kwargs)
        context['requerimiento'] = requerimiento
        context['materiales'] = materiales
        context['accion']="Actualizar"
        context['titulo']="Requerimiento"
        return context


class RequerimientoMaterialDetalleCreateView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoMaterialDetalleForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_inicio')

    def form_valid(self, form):
        registro = RequerimientoMaterial.objects.get(id = self.kwargs['requerimiento_id'])
        item = len(RequerimientoMaterialDetalle.objects.filter(requerimiento_material = registro))
        material = form.cleaned_data.get('material')
        cantidad = form.cleaned_data.get('cantidad')

        obj, created = RequerimientoMaterialDetalle.objects.get_or_create(
            content_type = ContentType.objects.get_for_model(material),
            id_registro = material.id,
            requerimiento_material = registro,
        )
        if created:
            obj.item = item + 1
            obj.cantidad = cantidad/2
        else:
            obj.cantidad = obj.cantidad + cantidad/2
        
        registro_guardar(obj, self.request)
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialDetalleCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Material '
        context['accion'] = 'Guardar'
        return context


class RequerimientoMaterialDetalleUpdateView(BSModalUpdateView):
    model = RequerimientoMaterialDetalle
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoMaterialDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_inicio')

    def form_valid(self, form):
        material = form.cleaned_data.get('material')
        cantidad = form.cleaned_data.get('cantidad')
        
        obj = RequerimientoMaterialDetalle.objects.get(
            content_type = ContentType.objects.get_for_model(material),
            id_registro = material.id,
        )
        
        registro_guardar(obj, self.request)
        obj.save()
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialDetalleUpdateView, self).get_context_data(**kwargs)        
        context['accion']="Actualizar"
        context['titulo']="material"
        return context
    

class RequerimientoMaterialDetalleDeleteView(BSModalDeleteView):
    model = RequerimientoMaterialDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_actualizar', kwargs={'pk':self.get_object().requerimiento_material.id})

    def delete(self, request, *args, **kwargs):
        materiales = RequerimientoMaterialDetalle.objects.filter(requerimiento_material=self.get_object().requerimiento_material)
        contador = 1
        for material in materiales:
            if material == self.get_object():continue
            material.item = contador
            material.save()
            contador += 1

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material del requerimiento"
        context['item'] = self.get_object().item
        context['dar_baja'] = "true"
        return context




class ProveedorForm(forms.Form):
    interlocutor_proveedor = forms.ModelChoiceField(queryset = ProveedorInterlocutor.objects.all(), required=False)

def ProveedorView(request, id_interlocutor_proveedor):
    form = ProveedorForm()
    lista = []
    relaciones = ProveedorInterlocutor.objects.filter(proveedor = id_interlocutor_proveedor)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)
    print(lista)
    form.fields['interlocutor_proveedor'].queryset = InterlocutorProveedor.objects.filter(id__in = lista)
    data = dict()
    if request.method == 'GET':
        template = 'includes/form.html'
        context = {'form':form}

        data['info'] = render_to_string(
            template,
            context,
            request=request
        ).replace('selected', 'selected=""')
        return JsonResponse(data)