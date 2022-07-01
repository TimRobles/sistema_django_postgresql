from decimal import Decimal
from applications.funciones import slug_aleatorio
from applications.requerimiento_de_materiales.pdf import generarRequerimientoMaterialProveedor
from applications.importaciones import *
from django import forms
from applications.proveedores.models import InterlocutorProveedor, Proveedor
from applications.sociedad.models import Sociedad
from datetime import datetime

from .forms import (
    ListaRequerimientoMaterialForm,
    ListaRequerimientoMaterialDetalleForm,
    ListaRequerimientoMaterialDetalleUpdateForm,
    RequerimientoMaterialProveedorForm,
    RequerimientoMaterialProveedorDetalleUpdateForm,
    RequerimientoMaterialProveedorDetalleForm,
)

from .models import (
    ListaRequerimientoMaterial,
    ListaRequerimientoMaterialDetalle,
    RequerimientoMaterialProveedor,
    RequerimientoMaterialProveedorDetalle,
    ProveedorInterlocutor,
)


class ListaRequerimientoMaterialListView(ListView):
    model = ListaRequerimientoMaterial
    template_name = "requerimiento_material/lista_requerimiento_material/inicio.html"
    context_object_name = 'contexto_lista_requerimiento_material'

def ListaRequerimientoMaterialTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'requerimiento_material/lista_requerimiento_material/inicio_tabla.html'
        context = {}
        context['contexto_lista_requerimiento_material'] = ListaRequerimientoMaterial.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ListaRequerimientoMaterialCreateView(FormView):
    template_name = "requerimiento_material/lista_requerimiento_material/detalle.html"
    form_class = ListaRequerimientoMaterialForm
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')
    global obj

    def form_valid(self, form):
        global obj
        obj.titulo = form.cleaned_data['titulo']
        registro_guardar(obj, self.request)
        obj.save()

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ListaRequerimientoMaterialCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['titulo'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        global obj
        context = super(ListaRequerimientoMaterialCreateView, self).get_context_data(**kwargs)
        obj, created = ListaRequerimientoMaterial.objects.get_or_create(
            titulo = None,
            created_by = self.request.user,
        )
        if obj.updated_by == None:
            obj.updated_by = self.request.user
            obj.save()

        materiales = None
        try:
            obj.ListaRequerimientoMaterialDetalle_requerimiento_material
            materiales = obj.ListaRequerimientoMaterialDetalle_requerimiento_material.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context['requerimiento'] = obj
        context['creado'] = created
        context['materiales'] = materiales
        return context

def ListaRequerimientoMaterialDetalleTabla(request, requerimiento_id):
    data = dict()
    if request.method == 'GET':
        template = 'requerimiento_material/lista_requerimiento_material/detalle_tabla.html'
        context = {}
        obj = ListaRequerimientoMaterial.objects.get(id = requerimiento_id)

        instance = {}
        instance['titulo'] = obj.titulo

        materiales = None
        try:
            materiales = obj.ListaRequerimientoMaterialDetalle_requerimiento_material.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context['requerimiento'] = obj
        context['materiales'] = materiales
        context['form'] = ListaRequerimientoMaterialForm(instance=instance)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ListaRequerimientoMaterialUpdateView(FormView):
    template_name = "requerimiento_material/lista_requerimiento_material/detalle.html"
    form_class = ListaRequerimientoMaterialForm
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def form_valid(self, form):
        obj = ListaRequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        titulo = form.cleaned_data['titulo']
        obj.titulo = titulo

        registro_guardar(obj, self.request)
        obj.save()

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        requerimiento = ListaRequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        kwargs = super(ListaRequerimientoMaterialUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['titulo'] = requerimiento.titulo
        return kwargs

    def get_context_data(self, **kwargs):
        requerimiento = ListaRequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        materiales = None
        try:
            requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material
            materiales = requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all()
            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass
        context = super(ListaRequerimientoMaterialUpdateView, self).get_context_data(**kwargs)
        context['requerimiento'] = requerimiento
        context['materiales'] = materiales
        context['accion']="Actualizar"
        context['titulo']="Requerimiento"
        return context

class ListaRequerimientoMaterialDetalleCreateView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = ListaRequerimientoMaterialDetalleForm
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def form_valid(self, form):
        registro = ListaRequerimientoMaterial.objects.get(id = self.kwargs['requerimiento_id'])
        item = len(ListaRequerimientoMaterialDetalle.objects.filter(lista_requerimiento_material = registro))
        material = form.cleaned_data.get('material')
        cantidad = form.cleaned_data.get('cantidad')
        comentario = form.cleaned_data.get('comentario')

        obj, created = ListaRequerimientoMaterialDetalle.objects.get_or_create(
            content_type = ContentType.objects.get_for_model(material),
            id_registro = material.id,
            lista_requerimiento_material = registro,
        )
        if created:
            obj.item = item + 1
            obj.cantidad = cantidad/2
            obj.comentario = comentario
        else:
            obj.cantidad = obj.cantidad + cantidad/2
            if obj.comentario[-len(' | ' + comentario):] != ' | ' + comentario:
                obj.comentario = obj.comentario + ' | ' + comentario

        registro_guardar(obj, self.request)
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ListaRequerimientoMaterialDetalleCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Material '
        context['accion'] = 'Guardar'
        return context

class ListaRequerimientoMaterialDetalleUpdateView(BSModalUpdateView):
    model = ListaRequerimientoMaterialDetalle
    template_name = "includes/formulario generico.html"
    form_class = ListaRequerimientoMaterialDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def form_valid(self, form):

        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ListaRequerimientoMaterialDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="material"
        return context

class ListaRequerimientoMaterialDetalleDeleteView(BSModalDeleteView):
    model = ListaRequerimientoMaterialDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:lista_requerimiento_material_actualizar', kwargs={'pk':self.get_object().lista_requerimiento_material.id})

    def delete(self, request, *args, **kwargs):
        
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListaRequerimientoMaterialDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material del requerimiento"
        context['item'] = self.get_object().item
        context['dar_baja'] = "true"
        return context

class ListaRequerimientoMaterialDeleteView(BSModalDeleteView):
    model = ListaRequerimientoMaterial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListaRequerimientoMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Lista de materiales"
        context['item'] = self.get_object().titulo
        context['dar_baja'] = "true"
        return context



class RequerimientoMaterialProveedorListView(ListView):
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/requerimiento_material_proveedor/inicio.html"
    context_object_name = 'contexto_requerimiento_material_proveedor'

def RequerimientoMaterialProveedorTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'requerimiento_material/requerimiento_material_proveedor/inicio_tabla.html'
        context = {}
        context['contexto_requerimiento_material_proveedor'] = RequerimientoMaterialProveedor.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class RequerimientoMaterialProveedorCreateView(BSModalCreateView):
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/lista_requerimiento_material/form_material.html"
    form_class = RequerimientoMaterialProveedorForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def form_valid(self, form):
        lista = ListaRequerimientoMaterial.objects.get(id=self.kwargs['lista_id'])

        form.instance.lista_requerimiento = lista
        form.instance.slug = slug_aleatorio(RequerimientoMaterialProveedor)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorCreateView, self).get_context_data(**kwargs)
        context['accion']="Asignar"
        context['titulo']="Requerimiento a Proveedor"
        return context

class RequerimientoMaterialProveedorUpdateView(BSModalUpdateView):
    model = RequerimientoMaterialProveedor
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoMaterialProveedorForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def form_valid(self, form):

        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="material"
        return context

class RequerimientoMaterialProveedorDeleteView(BSModalDeleteView):
    model = RequerimientoMaterialProveedor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Lista de materiales"
        context['item'] = self.get_object().titulo
        context['dar_baja'] = "true"
        return context

class RequerimientoMaterialProveedorDetailView(DetailView):
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/requerimiento_material_proveedor/detalle.html"
    context_object_name = 'contexto_requerimiento_material_proveedor'

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDetailView, self).get_context_data(**kwargs)
        obj = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['pk'])

        materiales = obj.RequerimientoMaterialProveedorDetalle_requerimiento_material.all()                
        for material in materiales:
            material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id=material.id_requerimiento_material_detalle.id_registro)

        context['requerimiento'] = obj
        context['materiales'] = materiales

        return context

def RequerimientoMaterialProveedorDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'requerimiento_material/requerimiento_material_proveedor/detalle_tabla.html'
        context = {}
        obj = RequerimientoMaterialProveedor.objects.get(id=pk)
        
        materiales = obj.RequerimientoMaterialProveedorDetalle_requerimiento_material.all()  

        for material in materiales:
            material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id=material.id_requerimiento_material_detalle.id_registro)

        context['requerimiento'] = obj
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class RequerimientoMaterialProveedorDuplicarView(BSModalCreateView):
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/requerimiento_material_proveedor/form_material.html"
    form_class = RequerimientoMaterialProveedorForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def form_valid(self, form):
        duplicado = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['requerimiento_id'])
        lista = duplicado.lista_requerimiento
        form.instance.lista_requerimiento = lista
        
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDuplicarView, self).get_context_data(**kwargs)
        context['accion']="Duplicar"
        context['titulo']="Requerimiento"
        return context

class RequerimientoMaterialProveedorDetalleUpdateView(BSModalUpdateView):
    model = RequerimientoMaterialProveedorDetalle
    template_name = "requerimiento_material/requerimiento_material_proveedor/actualizar.html"
    form_class = RequerimientoMaterialProveedorDetalleUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_detalle', kwargs={'pk':self.get_object().requerimiento_material.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="material"
        return context

class RequerimientoMaterialProveedorDetalleDeleteView(BSModalDeleteView):
    model = RequerimientoMaterialProveedorDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_detalle', kwargs={'pk':self.get_object().requerimiento_material.id})

    def delete(self, request, *args, **kwargs):
        materiales = RequerimientoMaterialProveedorDetalle.objects.filter(requerimiento_material=self.get_object().requerimiento_material)
        contador = 1
        for material in materiales:
            if material == self.get_object():continue
            material.item = contador
            material.save()
            contador += 1

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDetalleDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material."
        context['item'] = self.get_object().item 
        context['dar_baja'] = "true"
        return context

class RequerimientoMaterialProveedorDetalleCreateView(BSModalFormView):
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoMaterialProveedorDetalleForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def form_valid(self, form):
        registro = RequerimientoMaterialProveedor.objects.get(id = self.kwargs['requerimiento_id'])
        print('********registro**********')
        print(registro)
        print('********item**********')
        item = len(RequerimientoMaterialProveedorDetalle.objects.filter(lista_requerimiento_material = registro))
        print('************************')
        print(item)
        print('************************')
        material = form.cleaned_data.get('material')
        cantidad = form.cleaned_data.get('cantidad')
        # comentario = form.cleaned_data.get('comentario')

        obj, created = RequerimientoMaterialProveedorDetalle.objects.get_or_create(
            content_type = ContentType.objects.get_for_model(material),
            id_registro = material.id,
            lista_requerimiento_material = registro,
        )
        if created:
            obj.item = item + 1
            obj.cantidad = cantidad/2
            # obj.comentario = comentario
        else:
            obj.cantidad = obj.cantidad + cantidad/2
            # if obj.comentario[-len(' | ' + comentario):] != ' | ' + comentario:
            #     obj.comentario = obj.comentario + ' | ' + comentario

        registro_guardar(obj, self.request)
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Material '
        return context

class RequerimientoMaterialProveedorPdfView(View):
    def get(self, request, *args, **kwargs):
        sociedad = Sociedad.objects.get(ruc='20518487303')
        color = sociedad.color
        titulo = 'Requerimiento'
        vertical = True
        logo = 'https://www.multiplay.com.pe/img/header/20220530095828.png'
        # logo = 'http://127.0.0.1:8000/media/img/sociedad/Logo_Multiplay_1A00E6b.jpg'
        pie_pagina = sociedad

        obj = RequerimientoMaterialProveedor.objects.get(slug=self.kwargs['slug'])

        fecha=datetime.strftime(obj.fecha,'%d - %m - %Y')

        Texto = obj.titulo + '\n' +str(obj.proveedor) + '\n' + str(fecha)

        TablaEncabezado = ['Item','Material', 'Unidad', 'Cantidad']

        detalle = obj.RequerimientoMaterialProveedorDetalle_requerimiento_material
        materiales = detalle.all()

        TablaDatos = []
        for material in materiales:
            fila = []
            material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id = material.id_requerimiento_material_detalle.id_registro)
            fila.append(material.item)
            fila.append(material.material)
            fila.append(material.material.unidad_base)
            fila.append(material.cantidad.quantize(Decimal('0.01')))
            TablaDatos.append(fila)

        buf = generarRequerimientoMaterialProveedor(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta



class ProveedorForm(forms.Form):
    interlocutor_proveedor = forms.ModelChoiceField(queryset = ProveedorInterlocutor.objects.all(), required=False)

def ProveedorView(request, id_interlocutor_proveedor):
    form = ProveedorForm()
    lista = []
    relaciones = ProveedorInterlocutor.objects.filter(proveedor = id_interlocutor_proveedor)
    for relacion in relaciones:
        lista.append(relacion.interlocutor.id)
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
