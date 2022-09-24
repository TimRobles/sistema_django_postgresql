from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from applications.funciones import slug_aleatorio
from applications.material.models import ProveedorMaterial
from applications.requerimiento_de_materiales.pdf import generarRequerimientoMaterialProveedor
from applications.importaciones import *
from django import forms
from applications.proveedores.models import InterlocutorProveedor, Proveedor
from applications.sociedad.models import Sociedad
from applications.oferta_proveedor.models import OfertaProveedor, OfertaProveedorDetalle
from datetime import datetime
from django.shortcuts import render


from .forms import (
    ListaRequerimientoMaterialForm,
    ListaRequerimientoMaterialDetalleForm,
    ListaRequerimientoMaterialDetalleUpdateForm,
    RequerimientoMaterialProveedorEnviarCorreoForm,
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


class ListaRequerimientoMaterialListView(PermissionRequiredMixin,ListView):
    permission_required = ('requerimiento_de_materiales.view_listarequerimientomaterial')

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

class ListaRequerimientoMaterialCreateView(PermissionRequiredMixin, FormView):
    permission_required = ('requerimiento_de_materiales.add_listarequerimientomaterialdetalle')
    template_name = "requerimiento_material/lista_requerimiento_material/detalle.html"
    form_class = ListaRequerimientoMaterialForm
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def form_valid(self, form):
        obj = ListaRequerimientoMaterial.objects.get(
            titulo = None,
            created_by = self.request.user,
        )
        obj.titulo = form.cleaned_data['titulo']
        registro_guardar(obj, self.request)
        obj.save()
        return HttpResponseRedirect(reverse_lazy('requerimiento_material_app:lista_requerimiento_material_actualizar', kwargs={'pk':obj.id}))

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ListaRequerimientoMaterialCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['titulo'] = None
        return kwargs

    def get_context_data(self, **kwargs):
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

class ListaRequerimientoMaterialDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('requerimiento_de_materiales.delete_listarequerimientomaterial')
    model = ListaRequerimientoMaterial
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListaRequerimientoMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Lista de materiales"
        context['item'] = self.get_object().titulo
        context['dar_baja'] = "true"
        return context

class ListaRequerimientoMaterialUpdateView(PermissionRequiredMixin, FormView):
    permission_required = ('requerimiento_de_materiales.change_listarequerimientomaterialdetalle')
    template_name = "requerimiento_material/lista_requerimiento_material/detalle.html"
    form_class = ListaRequerimientoMaterialForm
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def form_valid(self, form):
        obj = ListaRequerimientoMaterial.objects.get(id=self.kwargs['pk'])
        titulo = form.cleaned_data['titulo']
        obj.titulo = titulo

        registro_guardar(obj, self.request)
        obj.save()

        return HttpResponseRedirect(reverse_lazy('requerimiento_material_app:lista_requerimiento_material_actualizar', kwargs={'pk':obj.id}))

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

class ListaRequerimientoMaterialDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('requerimiento_de_materiales.add_listarequerimientomaterialdetalle')

    template_name = "requerimiento_material/lista_requerimiento_material/form_material.html"
    form_class = ListaRequerimientoMaterialDetalleForm
    success_url = reverse_lazy('requerimiento_material_app:lista_requerimiento_material_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session['primero']:
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
                obj.cantidad = cantidad
                obj.comentario = comentario
            else:
                obj.cantidad = obj.cantidad + cantidad
                obj.comentario = obj.comentario + ' | ' + comentario

            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ListaRequerimientoMaterialDetalleCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Material '
        context['accion'] = 'Guardar'
        return context

class ListaRequerimientoMaterialDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('requerimiento_de_materiales.change_listarequerimientomaterialdetalle')
    model = ListaRequerimientoMaterialDetalle
    template_name = "includes/formulario generico.html"
    form_class = ListaRequerimientoMaterialDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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

class ListaRequerimientoMaterialDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('requerimiento_de_materiales.delete_listarequerimientomaterialdetalle')
    model = ListaRequerimientoMaterialDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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



class RequerimientoMaterialProveedorListView(PermissionRequiredMixin, ListView):
    permission_required = ('requerimiento_de_materiales.view_requerimientomaterialproveedor')
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

class RequerimientoMaterialProveedorCreateView(PermissionRequiredMixin,BSModalCreateView):
    permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedor')
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/lista_requerimiento_material/form_proveedor.html"
    form_class = RequerimientoMaterialProveedorForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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

class RequerimientoMaterialProveedorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('requerimiento_de_materiales.change_requerimientomaterialproveedor')
    model = RequerimientoMaterialProveedor
    template_name = "includes/formulario generico.html"
    form_class = RequerimientoMaterialProveedorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def form_valid(self, form):

        registro_guardar(form.instance, self.request)

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Material"
        return context

class RequerimientoMaterialProveedorDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('requerimiento_de_materiales.delete_requerimientomaterialproveedor')
    model = RequerimientoMaterialProveedor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Lista de materiales"
        context['item'] = self.get_object().titulo
        context['dar_baja'] = "true"
        return context

class RequerimientoMaterialProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('requerimiento_de_materiales.view_requerimientomaterialproveedordetalle')
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/requerimiento_material_proveedor/detalle.html"
    context_object_name = 'contexto_requerimiento_material_proveedor'

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDetailView, self).get_context_data(**kwargs)
        obj = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['pk'])

        materiales = obj.RequerimientoMaterialProveedorDetalle_requerimiento_material.all()
        for material in materiales:
            material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id=material.id_requerimiento_material_detalle.id_registro)
            material.proveedor_material, created = ProveedorMaterial.objects.get_or_create(
                content_type = material.id_requerimiento_material_detalle.content_type,
                id_registro = material.id_requerimiento_material_detalle.id_registro,
                proveedor = obj.proveedor,
                estado_alta_baja = 1,
            )

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
            material.proveedor_material, created = ProveedorMaterial.objects.get_or_create(
                content_type = material.id_requerimiento_material_detalle.content_type,
                id_registro = material.id_requerimiento_material_detalle.id_registro,
                proveedor = obj.proveedor,
                estado_alta_baja = 1,
            )

        context['requerimiento'] = obj
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class RequerimientoMaterialProveedorDuplicarView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedor')
    model = RequerimientoMaterialProveedor
    template_name = "requerimiento_material/requerimiento_material_proveedor/form_proveedor.html"
    form_class = RequerimientoMaterialProveedorForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        duplicado = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['requerimiento_id'])
        lista = duplicado.lista_requerimiento
        form.instance.lista_requerimiento = lista
        form.instance.slug = slug_aleatorio(RequerimientoMaterialProveedor)

        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDuplicarView, self).get_context_data(**kwargs)
        context['accion']="Duplicar"
        context['titulo']="Requerimiento"
        return context

class RequerimientoMaterialProveedorDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('requerimiento_de_materiales.change_requerimientomaterialproveedordetalle')

    model = RequerimientoMaterialProveedorDetalle
    template_name = "requerimiento_material/requerimiento_material_proveedor/actualizar.html"
    form_class = RequerimientoMaterialProveedorDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_detalle', kwargs={'pk':self.get_object().requerimiento_material.id})

    def form_valid(self, form):
        proveedor_material = ProveedorMaterial.objects.get(
                content_type = form.instance.id_requerimiento_material_detalle.content_type,
                id_registro = form.instance.id_requerimiento_material_detalle.id_registro,
                proveedor = form.instance.requerimiento_material.proveedor,
                estado_alta_baja = 1,
            )
        proveedor_material.name = form.cleaned_data['name']
        proveedor_material.brand = form.cleaned_data['brand']
        proveedor_material.description = form.cleaned_data['description']
        proveedor_material.save()
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimientoMaterialProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Material"
        return context

class RequerimientoMaterialProveedorDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('requerimiento_de_materiales.delete_requerimientomaterialproveedordetalle')
    model = RequerimientoMaterialProveedorDetalle
    template_name = "includes/eliminar generico.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

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
    template_name = "requerimiento_material/lista_requerimiento_material/form_material.html"
    form_class = RequerimientoMaterialProveedorDetalleForm
    success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

    def form_valid(self, form):
        if self.request.session['primero']:
            registro = RequerimientoMaterialProveedor.objects.get(id = self.kwargs['requerimiento_id'])
            item = len(registro.RequerimientoMaterialProveedorDetalle_requerimiento_material.all())
            material = form.cleaned_data.get('material')
            cantidad = form.cleaned_data.get('cantidad')

            requerimiento_material_detalle = ListaRequerimientoMaterialDetalle.objects.get(
                content_type = ContentType.objects.get_for_model(material),
                id_registro = material.id ,
                lista_requerimiento_material = registro.lista_requerimiento,
            )

            obj, created = RequerimientoMaterialProveedorDetalle.objects.get_or_create(
                id_requerimiento_material_detalle = requerimiento_material_detalle,
                requerimiento_material = registro
            )

            if created:
                obj.item = item + 1
                obj.cantidad = cantidad
                # obj.comentario = comentario
            else:
                obj.cantidad = obj.cantidad + cantidad
                # if obj.comentario[-len(' | ' + comentario):] != ' | ' + comentario:
                #     obj.comentario = obj.comentario + ' | ' + comentario


            registro_guardar(obj, self.request)
            obj.save()
            self.request.session['primero'] = False
        return super().form_valid(form)


    def get_form_kwargs(self):
        registro = RequerimientoMaterialProveedor.objects.get(id = self.kwargs['requerimiento_id'])
        materiales = registro.lista_requerimiento.ListaRequerimientoMaterialDetalle_requerimiento_material.all()
        kwargs = super().get_form_kwargs()
        kwargs['materiales'] = materiales
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RequerimientoMaterialProveedorDetalleCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Material'
        return context

class RequerimientoMaterialProveedorPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Requerimiento'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = RequerimientoMaterialProveedor.objects.get(slug=self.kwargs['slug'])

        fecha=datetime.strftime(obj.fecha,'%d - %m - %Y')

        Texto = obj.titulo + '\n' +str(obj.proveedor) + '\n' + str(fecha) + '\n' + obj.comentario

        TablaEncabezado = ['Item','Name', 'Brand', 'Description', 'Unidad', 'Cantidad']

        detalle = obj.RequerimientoMaterialProveedorDetalle_requerimiento_material
        materiales = detalle.all()

        TablaDatos = []
        for material in materiales:
            material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id = material.id_requerimiento_material_detalle.id_registro)
            proveedor_material = ProveedorMaterial.objects.get(
                content_type = ContentType.objects.get_for_model(material.material),
                id_registro = material.material.id,
                proveedor = obj.proveedor,
                estado_alta_baja = 1,
            )
            fila = []
            fila.append(material.item)
            fila.append(proveedor_material.name)
            fila.append(proveedor_material.brand)
            fila.append(proveedor_material.description)
            fila.append(material.material.unidad_base)
            fila.append(material.cantidad.quantize(Decimal('0.01')))

            TablaDatos.append(fila)

        buf = generarRequerimientoMaterialProveedor(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        obj.estado = 2
        obj.save()

        return respuesta

class RequerimientoMaterialProveedorEnviarCorreoView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedor')

    template_name = "includes/formulario generico.html"
    form_class = RequerimientoMaterialProveedorEnviarCorreoForm
    success_url = reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.session['primero']:
            # requerimiento = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['requerimiento_id'])
            requerimiento = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['slug'])
            correos_proveedor = form.cleaned_data['correos_proveedor']
            correos_internos = form.cleaned_data['correos_internos']
            internacional_nacional = form.cleaned_data['internacional_nacional']
            moneda = form.cleaned_data['moneda']

            oferta = OfertaProveedor.objects.create(
                internacional_nacional=internacional_nacional,
                requerimiento_material=requerimiento,
                moneda=moneda,
                slug = slug_aleatorio(OfertaProveedor),
            )

            requerimiento_detalle = requerimiento.RequerimientoMaterialProveedorDetalle_requerimiento_material.all()
            for detalle in requerimiento_detalle:

                proveedor_material, created = ProveedorMaterial.objects.get_or_create(
                    content_type = detalle.id_requerimiento_material_detalle.content_type,
                    id_registro = detalle.id_requerimiento_material_detalle.id_registro,
                    proveedor = requerimiento.proveedor,
                    estado_alta_baja = 1,
                )
                if internacional_nacional=='1':
                    igv = 8
                else:
                    igv = 1

                oferta_detalle = OfertaProveedorDetalle.objects.create(
                    item=detalle.item,
                    proveedor_material=proveedor_material,
                    cantidad=detalle.cantidad,
                    oferta_proveedor=oferta,
                    tipo_igv = igv,
                    )
            self.request.session['primero'] = False

            asunto = "Requerimiento - %s" % (requerimiento.titulo)
            mensaje = '<p>Estimado,</p><p>Se le invita a cotizar el siguiente requerimiento: <a href="%s%s">%s</a></p>' % (self.request.META['HTTP_ORIGIN'], reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_pdf', kwargs={'slug':requerimiento.slug}), 'Requerimiento')
            email_remitente = EMAIL_REMITENTE

            correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to=correos_proveedor, cc=correos_internos,)
            correo.attach_alternative(mensaje, "text/html")
            try:
                correo.send()
                requerimiento.estado = 3
                requerimiento.save()

                messages.success(self.request, 'Correo enviado.')
                self.request.session['primero'] = False
            except:
                messages.warning(self.request, 'Hubo un error al enviar el correo.')

        # registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(RequerimientoMaterialProveedorEnviarCorreoView, self).get_form_kwargs()
        kwargs['proveedor'] = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['slug']).proveedor
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RequerimientoMaterialProveedorEnviarCorreoView, self).get_context_data(**kwargs)
        context['accion']="Enviar"
        context['titulo']="Correos"
        return context





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
