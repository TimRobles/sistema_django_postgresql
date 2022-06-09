from applications.importaciones import *
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat, Unidad
from django import forms
from django.shortcuts import render

from .forms import (
    ModeloForm, MarcaForm,MaterialForm, 
    RelacionMaterialComponenteForm,EspecificacionForm, 
    DatasheetForm,DatosImportacionForm,ProductoSunatForm,
    ImagenMaterialForm,VideoMaterialForm,ProveedorMaterialForm,EquivalenciaUnidadForm,IdiomaMaterialForm,
    )
from .models import (
    Modelo, 
    Marca,
    Material,
    RelacionMaterialComponente,
    Especificacion,
    Datasheet,
    SubFamilia,
    ImagenMaterial,
    VideoMaterial,
    ProveedorMaterial,
    EquivalenciaUnidad,
    IdiomaMaterial,
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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super(MarcaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Marca"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)


class MaterialListView(PermissionRequiredMixin,ListView):
    permission_required = ('material.view_material')
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

class MaterialCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_material')
    model = Material
    template_name = "material/material/form_material.html"
    form_class = MaterialForm 
    success_url = reverse_lazy('material_app:material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Material"
        return context
        
class MaterialUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_material')
    model = Material
    template_name = "material/material/form_material.html"
    form_class = MaterialForm
    success_url = reverse_lazy('material_app:material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super(MaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)

class MaterialDarBajaView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_material')
    model = Material
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('material_app:material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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

class MaterialDarAltaView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_material')
    model = Material
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('material_app:material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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


class MaterialDetailView(PermissionRequiredMixin,DetailView):
    permission_required = ('material.view_material')
    model = Material
    template_name = "material/material/detalle.html"
    context_object_name = 'contexto_material'

    def get_context_data(self, **kwargs):
        material = Material.objects.get(id = self.kwargs['pk'])
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        context['componentes'] = RelacionMaterialComponente.objects.filter(material = material)
        context['especificaciones'] = Especificacion.objects.filter(material = material)
        context['datasheets'] = Datasheet.objects.filter(material = material)
        context['imagenes'] = ImagenMaterial.objects.filter(material = material)
        context['videos'] = VideoMaterial.objects.filter(material = material)
        context['proveedores'] = ProveedorMaterial.objects.filter(material = material)
        context['equivalencias'] = EquivalenciaUnidad.objects.filter(material = material)
        context['idiomas'] = IdiomaMaterial.objects.filter(material = material)
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
        context['imagenes'] = ImagenMaterial.objects.filter(material = material)
        context['videos'] = VideoMaterial.objects.filter(material = material)
        context['proveedores'] = ProveedorMaterial.objects.filter(material = material)
        context['equivalencias'] = EquivalenciaUnidad.objects.filter(material = material)
        context['idiomas'] = IdiomaMaterial.objects.filter(material = material)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ComponenteCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_relacionmaterialcomponente')
    model = RelacionMaterialComponente
    template_name = "includes/formulario generico.html"
    form_class = RelacionMaterialComponenteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        material = Material.objects.get(id = self.kwargs['material_id'])
        filtro = RelacionMaterialComponente.objects.filter(
            componentematerial = form.instance.componentematerial,
            material = material)
        if len(filtro)>0:
            form.add_error('componentematerial', 'El material ya cuenta con el componente seleccionado.')
            return super().form_invalid(form)
            
        form.instance.material = material
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

class ComponenteUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_relacionmaterialcomponente')
    model = RelacionMaterialComponente
    template_name = "includes/formulario generico.html"
    form_class = RelacionMaterialComponenteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ComponenteUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['componentes'] = self.object.material.subfamilia.componentes.all()
        return kwargs

    def form_valid(self, form):
        filtro = RelacionMaterialComponente.objects.filter(
            componentematerial = form.instance.componentematerial,
            material = self.object.material).exclude(
                id = self.object.id
            )
        if len(filtro)>0:
            form.add_error('componentematerial', 'El material ya cuenta con el componente seleccionado.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComponenteUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Componentes"
        return context

class ComponenteDeleteView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_relacionmaterialcomponente')
    model = RelacionMaterialComponente
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_context_data(self, **kwargs):
        context = super(ComponenteDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Componente"
        return context


class EspecificacionCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_especificacion')
    model = Especificacion
    template_name = "includes/formulario generico.html"
    form_class = EspecificacionForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        material = Material.objects.get(id = self.kwargs['material_id'])
        filtro = Especificacion.objects.filter(
            atributomaterial = form.instance.atributomaterial,
            material = material)
        if len(filtro)>0:
            form.add_error('atributomaterial', 'El material ya cuenta con el atributo seleccionado.')
            return super().form_invalid(form)
            
        form.instance.material = material
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

class EspecificacionUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_especificacion')
    model = Especificacion
    template_name = "includes/formulario generico.html"
    form_class = EspecificacionForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EspecificacionUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['atributos'] = self.object.material.subfamilia.familia.atributos.all()
        return kwargs

    def form_valid(self, form):
        filtro = Especificacion.objects.filter(
            atributomaterial = form.instance.atributomaterial,
            material = self.object.material).exclude(
                id = self.object.id
            )
        if len(filtro)>0:
            form.add_error('atributomaterial', 'El material ya cuenta con el atributo seleccionado.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EspecificacionUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Especificación"
        return context

class EspecificacionDeleteView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_especificacion')
    model = Especificacion
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_context_data(self, **kwargs):
        context = super(EspecificacionDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Especificación"
        return context


class DatasheetCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_datasheet')
    model = Datasheet
    template_name = "includes/formulario generico.html"
    form_class = DatasheetForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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

class DatasheetUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_datasheet')
    model = Datasheet
    template_name = "includes/formulario generico.html"
    form_class = DatasheetForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatasheetUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Datasheet"
        return context

class DatasheetDeleteView(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_datasheet')
    model = Datasheet
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_context_data(self, **kwargs):
        context = super(DatasheetDeleteView, self).get_context_data(**kwargs)
        context['accion']="Eliminar"
        context['titulo']="Datasheet"
        return context

class DatosImportacionUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_material')
    model = Material
    template_name = "includes/formulario generico.html"
    form_class = DatosImportacionForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    


    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DatosImportacionUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Datos de Importación"
        return context


class ProductoSunatUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_material')
    model = Material
    template_name = "material/material/form_sunat.html"
    form_class = ProductoSunatForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

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
    familia = forms.ModelChoiceField(queryset = FamiliaSunat.objects.all(), required=False)

def FamiliaSunatView(request, id_segmento):
    form = FamiliaSunatForm()
    form.fields['familia'].queryset = FamiliaSunat.objects.filter(segmento = id_segmento)
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

class ClaseSunatForm(forms.Form):
    clase = forms.ModelChoiceField(queryset = ClaseSunat.objects.all(), required=False)

def ClaseSunatView(request, id_familia):
    form = ClaseSunatForm()
    form.fields['clase'].queryset = ClaseSunat.objects.filter(familia = id_familia)
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

class ProductoSunatForm(forms.Form):
    producto = forms.ModelChoiceField(queryset = ProductoSunat.objects.all(), required=False)

def ProductoSunatView(request, id_clase):
    form = ProductoSunatForm()
    form.fields['producto'].queryset = ProductoSunat.objects.filter(clase = id_clase)
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

class SubfamiliaForm(forms.Form):
    subfamilia = forms.ModelChoiceField(queryset = SubFamilia.objects.all(), required=False)

def SubfamiliaView(request, id_familia):
    form = SubfamiliaForm()
    form.fields['subfamilia'].queryset = SubFamilia.objects.filter(familia = id_familia)
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

class UnidadForm(forms.Form):
    unidad = forms.ModelChoiceField(queryset = Unidad.objects.all(), required=False)

def UnidadView(request, id_subfamilia):
    form = UnidadForm()
    form.fields['unidad'].queryset = SubFamilia.objects.get(id = id_subfamilia).unidad.all()
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


class ModeloForm(forms.Form):
    modelo = forms.ModelChoiceField(queryset = Modelo.objects.all(), required=False)

def ModeloView(request, id_marca):
    form = ModeloForm()
    if id_marca != "0":
        form.fields['modelo'].queryset = Marca.objects.get(id = id_marca).modelos.all()
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


class ImagenMaterialCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_imagenmaterial')
    model = ImagenMaterial
    template_name = "includes/formulario generico.html"
    form_class = ImagenMaterialForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        material = Material.objects.get(id = self.kwargs['material_id'])
        filtro = ImagenMaterial.objects.filter(
            descripcion = form.instance.descripcion,
            material = material)
        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de imagen ya registrada.')
            return super().form_invalid(form)

        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImagenMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Imagen Material"
        return context     

class ImagenMaterialUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.delete_imagenmaterial')
    model = ImagenMaterial
    template_name = "includes/formulario generico.html"
    form_class = ImagenMaterialForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        filtro = ImagenMaterial.objects.filter(
            descripcion = form.instance.descripcion,
            material = self.object.material).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de imagen ya registrada.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImagenMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Imagen"
        return context

class ImagenMaterialDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_imagenmaterial')
    model = ImagenMaterial
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( ImagenMaterialDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Imagen"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context

class ImagenMaterialDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_imagenmaterial')
    model = ImagenMaterial
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ImagenMaterialDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Imagen"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context


class VideoMaterialCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_videomaterial')
    model = VideoMaterial
    template_name = "includes/formulario generico.html"
    form_class = VideoMaterialForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        material = Material.objects.get(id = self.kwargs['material_id'])
        filtro = VideoMaterial.objects.filter(
            descripcion = form.instance.descripcion,
            material = material)
        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de video ya registrada.')
            return super().form_invalid(form)

        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VideoMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Video Material"
        return context     

class VideoMaterialUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_videomaterial')
    model = VideoMaterial
    template_name = "includes/formulario generico.html"
    form_class = VideoMaterialForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        filtro = VideoMaterial.objects.filter(
            descripcion = form.instance.descripcion,
            material = self.object.material).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('descripcion', 'Descripción de video ya registrada.')
            return super().form_invalid(form)
        else:
            pass
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VideoMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Video"
        return context

class VideoMaterialDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_videomaterial')
    model = VideoMaterial
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( VideoMaterialDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Video"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context

class VideoMaterialDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_videomaterial')
    model = VideoMaterial
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(VideoMaterialDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Video"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion
        return context


class ProveedorMaterialCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_proveedormaterial')
    model = ProveedorMaterial
    template_name = "includes/formulario generico.html"
    form_class = ProveedorMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)        

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        material = Material.objects.get(id = self.kwargs['material_id'])
        filtro = ProveedorMaterial.objects.filter(
            proveedor = form.instance.proveedor,
            material = material)
        if len(filtro)>0:
            form.add_error('proveedor', 'Proveedor ya asignado al material.')
            return super().form_invalid(form)

        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProveedorMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Proveedor"
        return context     

class ProveedorMaterialUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_proveedormaterial')
    model = ProveedorMaterial
    template_name = "includes/formulario generico.html"
    form_class = ProveedorMaterialForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        filtro = ProveedorMaterial.objects.filter(
            proveedor = form.instance.proveedor,
            material = self.object.material).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('proveedor', 'Proveedor ya asignado al material.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProveedorMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Proveedor Material"
        return context

class ProveedorMaterialDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_proveedormaterial')
    model = ProveedorMaterial
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( ProveedorMaterialDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Proveedor Material"
        context['dar_baja'] = "true"
        context['item'] = self.object.proveedor
        return context

class ProveedorMaterialDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_proveedormaterial')
    model = ProveedorMaterial
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProveedorMaterialDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Proveedor Material"
        context['dar_baja'] = "true"
        context['item'] = self.object.proveedor
        return context


class EquivalenciaUnidadCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('material.add_equivalenciaunidad')
    model = EquivalenciaUnidad
    template_name = "includes/formulario generico.html"
    form_class = EquivalenciaUnidadForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def get_form_kwargs(self, *args, **kwargs):
        material = Material.objects.get(id = self.kwargs['material_id'])
        kwargs = super(EquivalenciaUnidadCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['material'] = material
        return kwargs

    def form_valid(self, form):
        form.instance.material = Material.objects.get(id = self.kwargs['material_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquivalenciaUnidadCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Equivalencia Unidad"
        return context     

class EquivalenciaUnidadUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_equivalenciaunidad')
    model = EquivalenciaUnidad
    template_name = "includes/formulario generico.html"
    form_class = EquivalenciaUnidadForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EquivalenciaUnidadUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['material'] = self.object.material
        return kwargs

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquivalenciaUnidadUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Equivalencia Unidad"
        return context

class EquivalenciaUnidadDarBaja(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_equivalenciaunidad')
    model = EquivalenciaUnidad
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super( EquivalenciaUnidadDarBaja, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Equivalencia Unidad"
        context['dar_baja'] = "true"
        return context

class EquivalenciaUnidadDarAlta(PermissionRequiredMixin,BSModalDeleteView):
    permission_required = ('material.delete_equivalenciaunidad')
    model = EquivalenciaUnidad
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_alta_baja = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EquivalenciaUnidadDarAlta, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Equivalencia Unidad"
        context['dar_baja'] = "true"
        return context


class IdiomaMaterialCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('material.add_idiomamaterial')
    model = IdiomaMaterial
    template_name = "includes/formulario generico.html"
    form_class = IdiomaMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)    

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.kwargs['material_id']})

    def form_valid(self, form):
        material = Material.objects.get(id = self.kwargs['material_id'])
        filtro = IdiomaMaterial.objects.filter(
            idioma = form.instance.idioma,
            material = material)
        if len(filtro)>0:
            form.add_error('idioma', 'Idioma ya registrado.')
            return super().form_invalid(form)

        form.instance.material = material
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IdiomaMaterialCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="IdiomaMaterial"
        return context     

class IdiomaMaterialUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('material.add_idiomamaterial')
    model = IdiomaMaterial
    template_name = "includes/formulario generico.html"
    form_class = IdiomaMaterialForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)   

    def get_success_url(self, **kwargs):
        return reverse_lazy('material_app:material_detalle', kwargs={'pk':self.object.material.id})

    def form_valid(self, form):
        filtro = IdiomaMaterial.objects.filter(
            idioma = form.instance.idioma,
            material = self.object.material).exclude(
                id = self.object.id
            )

        if len(filtro)>0:
            form.add_error('idioma', 'Idioma ya registrado.')
            return super().form_invalid(form)
        else:
            pass

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IdiomaMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Idioma del Material"
        return context

