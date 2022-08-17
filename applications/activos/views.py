from django.shortcuts import render
from applications.activos.models import ActivoBase, ArchivoAsignacionActivo, AsignacionActivo, AsignacionDetalleActivo, SubFamiliaActivo
from applications.activos.pdf import generarAsignacionActivos
from applications.datos_globales.models import SegmentoSunat,FamiliaSunat,ClaseSunat,ProductoSunat
from applications.importaciones import *
from django import forms
from bootstrap_modal_forms.generic import BSModalCreateView
from .forms import ActivoBaseForm, ArchivoAsignacionActivoForm, AsignacionActivoForm, AsignacionDetalleActivoForm, ProductoSunatActivoForm


class SubFamiliaActivoForm(forms.Form):
    sub_familia = forms.ModelChoiceField(queryset = SubFamiliaActivo.objects.all(), required=False)


def SubFamiliaActivoView(request, id_familia):
    form = SubFamiliaActivoForm()
    form.fields['sub_familia'].queryset = SubFamiliaActivo.objects.filter(familia = id_familia)
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


class ProductoSunatActivoUpdateView(PermissionRequiredMixin,BSModalUpdateView):
    permission_required = ('material.change_material')
    model = ActivoBase
    template_name = "material/material/form_sunat.html"
    form_class = ProductoSunatActivoForm
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('activos_app:activo_base_inicio')
        # return reverse_lazy('activos_app:activo_base_inicio', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductoSunatActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Producto Sunat"
        return context


class FamiliaSunatActivoForm(forms.Form):
    familia = forms.ModelChoiceField(queryset = FamiliaSunat.objects.all(), required=False)

def FamiliaSunatActivoView(request, id_segmento):
    form = FamiliaSunatActivoForm()
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


class ClaseSunatActivoForm(forms.Form):
    clase = forms.ModelChoiceField(queryset = ClaseSunat.objects.all(), required=False)

def ClaseSunatActivoView(request, id_familia):
    form = ClaseSunatActivoForm()
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


class ProductoSunatActivoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset = ProductoSunat.objects.all(), required=False)

def ProductoSunatActivoView(request, id_clase):
    form = ProductoSunatActivoForm()
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


class ActivoBaseListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_activo_base')
    model = ActivoBase
    template_name = "activos/activo_base/inicio.html"
    context_object_name = 'contexto_activo_base'


def ActivoBaseTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/activo_base/inicio_tabla.html'
        context = {}
        context['contexto_activo_base'] = ActivoBase.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)  


class ActivoBaseCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_activo_base')
    model = ActivoBase
    template_name = "activos/activo_base/form_activo_base.html"
    form_class = ActivoBaseForm
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def get_context_data(self, **kwargs):
            context = super(ActivoBaseCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Activo Base"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class ActivoBaseUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_activo_base')
    model = ActivoBase
    # template_name = "activos/activo_base/registro.html"
    template_name = "activos/activo_base/form_activo_base.html"
    form_class = ActivoBaseForm
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def get_context_data(self, **kwargs):
        context = super(ActivoBaseUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Activo Base"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

class ActivoBaseDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_activo_base')

    model = ActivoBase
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ActivoBaseDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Activo Base"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_corta
        return context

class ActivoBaseDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_activo_base')

    model = ActivoBase
    template_name = "includes/dar_alta_generico.html"
    success_url = reverse_lazy('activos_app:activo_base_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ActivoBaseDarAltaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Alta"
        context['titulo'] = "Activo Base"
        context['dar_baja'] = "true"
        context['item'] = self.object.descripcion_corta
        return context



class AsignacionActivoListView(PermissionRequiredMixin, ListView):
    permission_required = ('activos.view_asignacion_activo')
    model = AsignacionActivo
    template_name = "activos/asignacion_activo/inicio.html"
    context_object_name = 'contexto_asignacion_activo'


def AsignacionActivoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'activos/asignacion_activo/inicio_tabla.html'
        context = {}
        context['contexto_asignacion_activo'] = AsignacionActivo.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)  


class AsignacionActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_asignacion_activo')
    model = AsignacionActivo
    # template_name = "activos/asignacion_activo/form_asignacion_activo.html"
    template_name = "includes/formulario generico.html"
    form_class = AsignacionActivoForm
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def get_context_data(self, **kwargs):
            context = super(AsignacionActivoCreateView, self).get_context_data(**kwargs)
            context['accion']="Registrar"
            context['titulo']="Asignación Activo"
            return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class AsignacionActivoUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/formulario generico.html"
    form_class = AsignacionActivoForm
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Asignación de Activos"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)


class AsignacionActivoDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 4
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Asignación de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_asignacion)
        return context


class AsignacionActivoConcluirView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.change_asignacion_activo')
    model = AsignacionActivo
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('activos_app:asignacion_activo_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 3
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AsignacionActivoConcluirView, self).get_context_data(**kwargs)
        context['accion'] = "Concluir sin Asignar"
        context['titulo'] = "Asignación de Activos"
        context['dar_baja'] = "true"
        context['item'] = self.object.titulo + ' - Fecha Doc.: ' + str(self.object.fecha_asignacion)
        return context


class AsignacionActivoDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('activos.view_asignacion_activo_detalle')
    model = AsignacionActivo
    template_name = "activos/asignacion_activo/inicio_detalle.html"
    context_object_name = 'contexto_asignacion_activo'

    def get_context_data(self, **kwargs):
        asignacion = AsignacionActivo.objects.get(id = self.kwargs['pk'])
        context = super(AsignacionActivoDetailView, self).get_context_data(**kwargs)
        context['contexto_asignacion_activo_detalle'] = AsignacionDetalleActivo.objects.filter(asignacion = asignacion)
        context['contexto_asignacion_activo_archivo'] = ArchivoAsignacionActivo.objects.filter(asignacion = asignacion)
        return context


def AsignacionActivoDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'activos/asignacion_activo/inicio_tabla_detalle.html'
        context = {}
        asignacion = AsignacionActivo.objects.get(id = pk)
        context['contexto_asignacion_activo'] = asignacion
        context['contexto_asignacion_activo_detalle'] = AsignacionDetalleActivo.objects.filter(asignacion = asignacion)
        context['contexto_asignacion_activo_archivo'] = ArchivoAsignacionActivo.objects.filter(asignacion = asignacion)

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)  


# Lo hizo Tim, referencia

# class AsignacionActivoDetailView(PermissionRequiredMixin, DetailView):
#     permission_required = ('activos.view_asignacion_activo_detalle')
#     model = AsignacionActivo
#     template_name = "activos/asignacion_activo/inicio_detalle.html"
#     context_object_name = 'contexto_asignacion_activo'

#     def get_context_data(self, **kwargs):
#         context = super(AsignacionActivoDetailView, self).get_context_data(**kwargs)
#         context['contexto_asignacion_activo_detalle'] = self.object.AsignacionDetalleActivo_asignacion.all()
#         return context


# def AsignacionActivoDetalleTabla(request, pk):
#     data = dict()
#     if request.method == 'GET':
#         template = 'activos/asignacion_activo/inicio_tabla_detalle.html'
#         context = {}
#         detalle_asignacion = AsignacionDetalleActivo.objects.get(id = pk)
#         context['contexto_asignacion_activo_detalle'] = detalle_asignacion

#         data['table'] = render_to_string(
#             template,
#             context,
#             request=request
#         )
#         return JsonResponse(data)  


class AsignacionDetalleActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_asignacion_activo_detalle')
    model = AsignacionDetalleActivo
    template_name = "includes/formulario generico.html"
    form_class = AsignacionDetalleActivoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk': self.kwargs['asignacion_id']})

    def form_valid(self, form):
        form.instance.asignacion = AsignacionActivo.objects.get(id = self.kwargs['asignacion_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AsignacionDetalleActivoCreateView, self).get_context_data(**kwargs)
        context['accion']="Agregar Item"
        context['titulo']="Asignación de Activo"
        return context


class AsignacionDetalleActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.add_asignacion_activo_detalle')
    model = AsignacionDetalleActivo
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_asignacion_detalle_activo_eliminar' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk':self.object.asignacion.id})

    def get_context_data(self, **kwargs):
        context = super(AsignacionDetalleActivoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Item de Asignación"
        context['dar_baja'] = "True"
        context['item'] = self.object.activo.descripcion_corta
        return context


class ArchivoAsignacionActivoCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('activos.add_archivo_asignacion_activo')
    model = ArchivoAsignacionActivo
    template_name = "includes/formulario generico.html"
    form_class = ArchivoAsignacionActivoForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk': self.kwargs['asignacion_id']})

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.asignacion = AsignacionActivo.objects.get(id = self.kwargs['asignacion_id'])
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArchivoAsignacionActivoCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Documento"
        return context


class ArchivoAsignacionActivoDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('activos.delete_archivo_asignacion_activo')
    model = ArchivoAsignacionActivo
    template_name = "includes/eliminar generico.html"
    context_object_name = 'contexto_asignacion_activo_archivo' 

    def get_success_url(self, **kwargs):
        return reverse_lazy('activos_app:asignacion_activo_detalle_inicio', kwargs={'pk':self.object.asignacion.id})

    def get_context_data(self, **kwargs):
        context = super(ArchivoAsignacionActivoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Archivo de Asignación"
        context['dar_baja'] = "True"
        context['item'] = self.object.archivo
        return context


class AsignacionActivoPdfView(View):
    def get(self, request, *args, **kwargs):
        color = COLOR_DEFAULT
        titulo = 'Asignación de Activos'
        vertical = True
        logo = None
        pie_pagina = PIE_DE_PAGINA_DEFAULT

        obj = AsignacionActivo.objects.get(id=self.kwargs['pk'])

        fecha = datetime.strftime(obj.fecha_asignacion,'%d - %m - %Y')

        texto_1 = obj.titulo + '\n' +str(obj.colaborador) + '\n' + str(fecha) + '\n'
        texto_2 = ''' En la Ciudad de Lima, con fecha, %s , se recibe de parte del Ing. BASILIO ALVAREZ ZAPATA, identificado con DNI° 19924516, Representante Legal de la Empresa MULTICABLE PERU SAC, con domicilio fiscal en Av. Petit Thouars N°3629 Urb. Fundo Chacarilla - San Isidro, con RUC N°20522137465, el/los equipo(s) que se especifica(n) a continuación:''' %(str(fecha))
        texto_3 = ''' Al momento de recibir el/los equipo(s) especificados se realizaron pruebas, encontrándose en buen estado físico y de funcionamiento.\n
            De acuerdo a lo anterior se hace constar que el/los equipo(s) se encuentran en las condiciones adecuadas para recibirlo(s). '''
        
        Texto = []
        Texto.extend([texto_1, texto_2, texto_3])
        
        TablaEncabezado = [
            'Item', 
            'Descripción', 
            'Brand', 
            'Description', 
            'Unidad', 
            'Cantidad'
            ]

        detalle = obj.AsignacionDetalleActivo_asignacion
        activos = detalle.all()

        TablaDatos = []
        count = 1
        for activo in activos:
            # material.material = material.id_requerimiento_material_detalle.content_type.get_object_for_this_type(
            #     id = material.id_requerimiento_material_detalle.id_registro
            #     )
            # proveedor_material = ProveedorMaterial.objects.get(
            #     content_type = ContentType.objects.get_for_model(material.material),
            #     id_registro = material.material.id,
            #     proveedor = obj.proveedor,
            #     estado_alta_baja = 1,
            #     )
            fila = []
            fila.append(str(count))
            fila.append(activo.activo.descripcion_corta)
            fila.append(activo.activo.descripcion_corta)
            fila.append(activo.activo.descripcion_corta)
            fila.append(activo.activo.descripcion_corta)
            fila.append(activo.activo.descripcion_corta)
            TablaDatos.append(fila)
            count += 1


        tabla_firmas = [
            ['', '------------------------', '', '------------------------', ''],
            ['', 'Recibe el/los equipo(s)', '', 'Entrega el/los equipo(s)', ''],
            ['', str(obj.colaborador), '', 'ING. BASILIO ÁLVAREZ ZAPATA', '']
            ]
        

        buf = generarAsignacionActivos(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color, tabla_firmas)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        obj.estado = 2
        obj.save()

        return respuesta