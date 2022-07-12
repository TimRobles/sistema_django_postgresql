from django.shortcuts import render
from applications.importaciones import *
from applications.oferta_proveedor.models import OfertaProveedor, OfertaProveedorDetalle
from applications.oferta_proveedor.forms import OfertaProveedorDetalleUpdateForm, OfertaProveedorForm

class OfertaProveedorListView(PermissionRequiredMixin, ListView):
    permission_required = ('oferta_proveedor.view_ofertaproveedor')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/inicio.html"
    context_object_name = 'contexto_oferta_proveedor'

def OfertaProveedorTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/inicio_tabla.html'
        context = {}
        context['contexto_oferta_proveedor'] = OfertaProveedor.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

# class OfertaProveedorCreateView(PermissionRequiredMixin,BSModalCreateView):
#     permission_required = ('oferta_proveedor.add_requerimientomaterialproveedor')
#     model = RequerimientoMaterialProveedor
#     template_name = "oferta_proveedor/lista_oferta_proveedor/form_material.html"
#     form_class = OfertaProveedorForm
#     success_url = reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')


#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         lista = ListaRequerimientoMaterial.objects.get(id=self.kwargs['lista_id'])

#         form.instance.lista_requerimiento = lista
#         form.instance.slug = slug_aleatorio(RequerimientoMaterialProveedor)

#         registro_guardar(form.instance, self.request)
#         return super().form_valid(form)


#     def get_context_data(self, **kwargs):
#         context = super(RequerimientoMaterialProveedorCreateView, self).get_context_data(**kwargs)
#         context['accion']="Asignar"
#         context['titulo']="Requerimiento a Proveedor"
#         return context

class OfertaProveedorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedor')
    model = OfertaProveedor
    template_name = "includes/formulario generico.html"
    form_class = OfertaProveedorForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Precios"
        return context

# class RequerimientoMaterialProveedorDeleteView(PermissionRequiredMixin, BSModalDeleteView):
#     permission_required = ('requerimiento_de_materiales.delete_requerimientomaterialproveedor')
#     model = RequerimientoMaterialProveedor
#     template_name = "includes/eliminar generico.html"
#     success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')
    
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(RequerimientoMaterialProveedorDeleteView, self).get_context_data(**kwargs)
#         context['accion'] = "Eliminar"
#         context['titulo'] = "Lista de materiales"
#         context['item'] = self.get_object().titulo
#         context['dar_baja'] = "true"
#         return context

class OfertaProveedorDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('oferta_proveedor.view_OfertaProveedordetalle')
    model = OfertaProveedor
    template_name = "oferta_proveedor/oferta_proveedor/detalle.html"
    context_object_name = 'contexto_oferta_proveedor'

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetailView, self).get_context_data(**kwargs)
        obj = OfertaProveedor.objects.get(id=self.kwargs['pk'])
        # print('***************************************************************')            
        # print(obj)                
        # print('***************************************************************')  

        materiales = obj.requerimiento_material.RequerimientoMaterialProveedorDetalle_requerimiento_material.all() 
        
        for material in materiales:
            material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id=material.id_requerimiento_material_detalle.id_registro)

        context['requerimiento'] = obj
        context['materiales'] = materiales

        return context

def OfertaProveedorDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'oferta_proveedor/oferta_proveedor/detalle_tabla.html'
        context = {}
        obj = OfertaProveedor.objects.get(id=pk)
      
        materiales = obj.requerimiento_material.RequerimientoMaterialProveedorDetalle_requerimiento_material.all() 

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

# class RequerimientoMaterialProveedorDuplicarView(PermissionRequiredMixin, BSModalCreateView):
#     permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedor')
#     model = RequerimientoMaterialProveedor
#     template_name = "requerimiento_material/requerimiento_material_proveedor/form_material.html"
#     form_class = RequerimientoMaterialProveedorForm
#     success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         duplicado = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['requerimiento_id'])
#         lista = duplicado.lista_requerimiento
#         form.instance.lista_requerimiento = lista
        
#         registro_guardar(form.instance, self.request)
#         return super().form_valid(form)


#     def get_context_data(self, **kwargs):
#         context = super(RequerimientoMaterialProveedorDuplicarView, self).get_context_data(**kwargs)
#         context['accion']="Duplicar"
#         context['titulo']="Requerimiento"
#         return context

class OfertaProveedorDetalleUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('oferta_proveedor.change_ofertaproveedordetalle')

    model = OfertaProveedorDetalle
    template_name = "oferta_proveedor/oferta_proveedor/actualizar.html"
    form_class = OfertaProveedorDetalleUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('oferta_proveedor_app:oferta_proveedor_detalle', kwargs={'pk':self.get_object().oferta_proveedor.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OfertaProveedorDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Precios"
        return context

# class RequerimientoMaterialProveedorDetalleDeleteView(PermissionRequiredMixin, BSModalDeleteView):
#     permission_required = ('requerimiento_de_materiales.delete_requerimientomaterialproveedordetalle')
#     model = RequerimientoMaterialProveedorDetalle
#     template_name = "includes/eliminar generico.html"

#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_detalle', kwargs={'pk':self.get_object().requerimiento_material.id})

#     def delete(self, request, *args, **kwargs):
#         materiales = RequerimientoMaterialProveedorDetalle.objects.filter(requerimiento_material=self.get_object().requerimiento_material)
#         contador = 1
#         for material in materiales:
#             if material == self.get_object():continue
#             material.item = contador
#             material.save()
#             contador += 1

#         return super().delete(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(RequerimientoMaterialProveedorDetalleDeleteView, self).get_context_data(**kwargs)
#         context['accion'] = "Eliminar"
#         context['titulo'] = "Material."
#         context['item'] = self.get_object().item 
#         context['dar_baja'] = "true"
#         return context

# class RequerimientoMaterialProveedorDetalleCreateView(PermissionRequiredMixin, BSModalFormView):
#     permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedordetalle')
#     template_name = "includes/formulario generico.html"
#     form_class = RequerimientoMaterialProveedorDetalleForm
#     success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         registro = RequerimientoMaterialProveedor.objects.get(id = self.kwargs['requerimiento_id'])
#         print('********registro**********')
#         print(registro)
#         print('********item**********')
#         item = len(RequerimientoMaterialProveedorDetalle.objects.filter(lista_requerimiento_material = registro))
#         print('************************')
#         print(item)
#         print('************************')
#         material = form.cleaned_data.get('material')
#         cantidad = form.cleaned_data.get('cantidad')
#         # comentario = form.cleaned_data.get('comentario')

#         obj, created = RequerimientoMaterialProveedorDetalle.objects.get_or_create(
#             content_type = ContentType.objects.get_for_model(material),
#             id_registro = material.id,
#             lista_requerimiento_material = registro,
#         )
#         if created:
#             obj.item = item + 1
#             obj.cantidad = cantidad/2
#             # obj.comentario = comentario
#         else:
#             obj.cantidad = obj.cantidad + cantidad/2
#             # if obj.comentario[-len(' | ' + comentario):] != ' | ' + comentario:
#             #     obj.comentario = obj.comentario + ' | ' + comentario

#         registro_guardar(obj, self.request)
#         obj.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super(RequerimientoMaterialProveedorDetalleCreateView, self).get_context_data(**kwargs)
#         context['accion'] = 'Agregar'
#         context['titulo'] = 'Material '
#         return context

# class RequerimientoMaterialProveedorPdfView(View):
#     def get(self, request, *args, **kwargs):
#         color = COLOR_DEFAULT
#         titulo = 'Requerimiento'
#         vertical = True
#         logo = None
#         pie_pagina = PIE_DE_PAGINA_DEFAULT

#         obj = RequerimientoMaterialProveedor.objects.get(slug=self.kwargs['slug'])

#         fecha=datetime.strftime(obj.fecha,'%d - %m - %Y')

#         Texto = obj.titulo + '\n' +str(obj.proveedor) + '\n' + str(fecha)

#         TablaEncabezado = ['Item','Material', 'Unidad', 'Cantidad']

#         detalle = obj.RequerimientoMaterialProveedorDetalle_requerimiento_material
#         materiales = detalle.all()

#         TablaDatos = []
#         for material in materiales:
#             fila = []
#             material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(id = material.id_requerimiento_material_detalle.id_registro)
#             fila.append(material.item)
#             fila.append(material.material)
#             fila.append(material.material.unidad_base)
#             fila.append(material.cantidad.quantize(Decimal('0.01')))
#             TablaDatos.append(fila)

#         buf = generarRequerimientoMaterialProveedor(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color)

#         respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
#         respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

#         obj.estado = 2
#         obj.save()

#         return respuesta


# class RequerimientoMaterialProveedorEnviarCorreoView(PermissionRequiredMixin, BSModalFormView):
#     permission_required = ('requerimiento_de_materiales.add_requerimientomaterialproveedor')

#     template_name = "includes/formulario generico.html"
#     form_class = RequerimientoMaterialProveedorEnviarCorreoForm
#     success_url = reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_inicio')

#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return render(request, 'includes/modal sin permiso.html')
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         if self.request.session['primero']:
#             requerimiento = RequerimientoMaterialProveedor.objects.get(id=self.kwargs['requerimiento_id'])

#             correos_proveedor = form.cleaned_data['correos_proveedor']
#             correos_internos = form.cleaned_data['correos_internos']
#             asunto = "Requerimiento - %s" % (requerimiento.titulo)
#             mensaje = '<p>Estimado,</p><p>Se le invita a cotizar el siguiente requerimiento: <a href="%s%s">%s</a></p>' % (self.request.META['HTTP_ORIGIN'], reverse_lazy('requerimiento_material_app:requerimiento_material_proveedor_pdf', kwargs={'slug':requerimiento.slug}), 'Requerimiento')
#             email_remitente = EMAIL_REMITENTE

#             print("*******************")
#             print(correos_proveedor)
#             print(correos_internos)
#             print("*******************")

#             correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to=correos_proveedor, cc=correos_internos,)
#             correo.attach_alternative(mensaje, "text/html")
#             try:
#                 correo.send()
#                 requerimiento.estado = 3
#                 requerimiento.save()
#                 messages.success(self.request, 'Correo enviado.')
#                 self.request.session['primero'] = False
#             except:
#                 messages.warning(self.request, 'Hubo un error al enviar el correo.')

#         return super().form_valid(form)


#     def get_context_data(self, **kwargs):
#         self.request.session['primero'] = True
#         context = super(RequerimientoMaterialProveedorEnviarCorreoView, self).get_context_data(**kwargs)
#         context['accion']="Enviar"
#         context['titulo']="Correos"
#         return context



# class ProveedorForm(forms.Form):
#     interlocutor_proveedor = forms.ModelChoiceField(queryset = ProveedorInterlocutor.objects.all(), required=False)

# def ProveedorView(request, id_interlocutor_proveedor):
#     form = ProveedorForm()
#     lista = []
#     relaciones = ProveedorInterlocutor.objects.filter(proveedor = id_interlocutor_proveedor)
#     for relacion in relaciones:
#         lista.append(relacion.interlocutor.id)
#     form.fields['interlocutor_proveedor'].queryset = InterlocutorProveedor.objects.filter(id__in = lista)
#     data = dict()
#     if request.method == 'GET':
#         template = 'includes/form.html'
#         context = {'form':form}

#         data['info'] = render_to_string(
#             template,
#             context,
#             request=request
#         ).replace('selected', 'selected=""')
#         return JsonResponse(data)

