from django import forms
from applications.importaciones import*
from applications.funciones import registrar_excepcion, numeroXn

from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.sociedad.models import Sociedad


from .models import(
    IngresoReclamoGarantia,
    IngresoReclamoGarantiaDetalle,
    ControlCalidadReclamoGarantia,
    ControlCalidadReclamoGarantiaDetalle,
    SalidaReclamoGarantia,
    SalidaReclamoGarantiaDetalle,
)
from .forms import(
    IngresoReclamoGarantiaBuscarForm,
    IngresoReclamoGarantiaClienteForm,
    IngresoReclamoGarantiaEncargadoForm,
    IngresoReclamoGarantiaSociedadForm,
    IngresoReclamoGarantiaObservacionForm,
    IngresoReclamoGarantiaMaterialForm,
    IngresoReclamoGarantiaMaterialUpdateForm,
    ControlCalidadReclamoGarantiaBuscarForm,
    ControlCalidadReclamoGarantiaEncargadoForm,
    ControlCalidadReclamoGarantiaObservacionForm,
    SalidaReclamoGarantiaBuscarForm,
    SalidaReclamoGarantiaEncargadoForm,
    SalidaReclamoGarantiaObservacionForm,
)


class IngresoReclamoGarantiaListView(FormView):
    template_name = 'garantia/ingreso_garantia/inicio.html'
    form_class = IngresoReclamoGarantiaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(IngresoReclamoGarantiaListView, self).get_form_kwargs()
        kwargs['filtro_fecha_ingreso'] = self.request.GET.get('fecha_ingreso')
        kwargs['filtro_nro_ingreso_garantia'] = self.request.GET.get('nro_ingreso_garantia')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaListView, self).get_context_data(**kwargs)
        ingreso_garantia = IngresoReclamoGarantia.objects.all()

        filtro_fecha_ingreso = self.request.GET.get('fecha_ingreso')
        filtro_nro_ingreso_garantia = self.request.GET.get('nro_ingreso_garantia')
        filtro_cliente = self.request.GET.get('cliente')
        filtro_sociedad = self.request.GET.get('sociedad')

        contexto_filtro = []
        if filtro_fecha_ingreso:
            condicion = Q(fecha_ingreso = datetime.strptime(filtro_fecha_ingreso, "%Y-%m-%d").date())
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("fecha_ingreso=" + filtro_fecha_ingreso)

        if filtro_nro_ingreso_garantia:
            condicion = Q(numero_nota__icontains = filtro_nro_ingreso_garantia)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("nro_ingreso_garantia=" + filtro_nro_ingreso_garantia)

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_sociedad:
            condicion = Q(sociedad__id = filtro_sociedad)
            ingreso_garantia = ingreso_garantia.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['contexto_ingreso_garantia'] = ingreso_garantia
        return context
    
def IngresoReclamoGarantiaCreateView(request):
    obj = IngresoReclamoGarantia.objects.create(
        encargado = request.user,
        created_by = request.user,
        updated_by = request.user,
    )
    obj.save()

    return HttpResponseRedirect(reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':obj.id}))

class IngresoReclamoGarantiaVerView(TemplateView):
    template_name = "garantia/ingreso_garantia/detalle.html"

    def get_context_data(self, **kwargs):
        obj = IngresoReclamoGarantia.objects.get(id = kwargs['id_ingreso'])
    
        materiales = None
        try:
            materiales = obj.IngresoReclamoGarantiaDetalle_ingreso_garantia.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)

        except:
            pass
        
        sociedades = Sociedad.objects.filter(estado_sunat=1)

        context = super(IngresoReclamoGarantiaVerView, self).get_context_data(**kwargs)
        context['ingreso'] = obj
        context['materiales'] = materiales
        context['sociedades'] = sociedades

        return context

def IngresoReclamoGarantiaVerTabla(request, id_ingreso):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/ingreso_garantia/detalle_tabla.html'
        obj = IngresoReclamoGarantia.objects.get(id=id_ingreso)

        materiales = None
        try:
            materiales = obj.IngresoReclamoGarantiaDetalle_ingreso_garantia.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
    
        except:
            pass

        sociedades = Sociedad.objects.filter(estado_sunat=1)

        context = {}
        context['ingreso'] = obj
        context['materiales'] = materiales
        context['sociedades'] = sociedades

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class IngresoReclamoGarantiaDeleteView(BSModalDeleteView):
    model = IngresoReclamoGarantia
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('garantia_app:ingreso_garantia_inicio')

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Ingreso Reclamo"
        context['item'] = "Garantia - %s" % (self.object.cliente)
        return context


class IngresoReclamoGarantiaClienteView(BSModalUpdateView):
    model = IngresoReclamoGarantia
    template_name = "garantia/ingreso_garantia/form_cliente.html"
    form_class = IngresoReclamoGarantiaClienteForm
    success_url = reverse_lazy('garantia_app:ingreso_garantia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        ingreso = kwargs['instance']
        lista = []
        relaciones = ClienteInterlocutor.objects.filter(cliente = ingreso.cliente)
        for relacion in relaciones:
            lista.append(relacion.interlocutor.id)

        kwargs['interlocutor_queryset'] = InterlocutorCliente.objects.filter(id__in = lista)
        kwargs['interlocutor'] = ingreso.cliente_interlocutor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaClienteView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Cliente"
        return context

class IngresoReclamoGarantiaEncargadoView(BSModalUpdateView):
    model = IngresoReclamoGarantia
    template_name = "garantia/ingreso_garantia/form_cliente.html"
    form_class = IngresoReclamoGarantiaEncargadoForm
    success_url = reverse_lazy('garantia_app:ingreso_garantia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaEncargadoView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Encargado"
        return context

class IngresoReclamoGarantiaSociedadView(BSModalUpdateView):
    model = IngresoReclamoGarantia
    template_name = "garantia/ingreso_garantia/form_cliente.html"
    form_class = IngresoReclamoGarantiaSociedadForm
    success_url = reverse_lazy('garantia_app:ingreso_garantia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaSociedadView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Sociedad"
        return context

class IngresoReclamoGarantiaObservacionUpdateView(BSModalUpdateView):
    model = IngresoReclamoGarantia
    template_name = "includes/formulario generico.html"
    form_class = IngresoReclamoGarantiaObservacionForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaObservacionUpdateView, self).get_context_data(**kwargs)
        
        context['titulo'] = "Actualizar Observaciones"
        context['observaciones'] = self.object.observacion
        context['id_ingreso'] = self.object.id
        return context


class IngresoReclamoGarantiaMaterialView(BSModalFormView):
    template_name = "garantia/ingreso_garantia/form_material.html"
    form_class = IngresoReclamoGarantiaMaterialForm
    success_url = reverse_lazy('garantia_app:ingreso_garantia_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                ingreso = IngresoReclamoGarantia.objects.get(id = self.kwargs['id_ingreso'])
                item = len(IngresoReclamoGarantiaDetalle.objects.filter(ingreso_garantia = ingreso))

                material = form.cleaned_data.get('material')
                cantidad = form.cleaned_data.get('cantidad')

                obj, created = IngresoReclamoGarantiaDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    ingreso_garantia = ingreso,
                )

                if created:
                    obj.item = item + 1
                    obj.cantidad = cantidad  

                registro_guardar(obj, self.request)
                obj.save()

                self.request.session['primero'] = False
            return super().form_valid(form)

        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(IngresoReclamoGarantiaMaterialView, self).get_context_data(**kwargs)
        context['titulo'] = 'Material'
        context['accion'] = 'Agregar'
        return context

class IngresoReclamoGarantiaMaterialUpdateView(BSModalUpdateView):
    model = IngresoReclamoGarantiaDetalle
    template_name = "garantia/ingreso_garantia/actualizar.html"
    form_class = IngresoReclamoGarantiaMaterialUpdateForm
    success_url = '.'

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            registro_guardar(form.instance, self.request)

            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaMaterialUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Material"
        context['material'] = self.object.content_type.get_object_for_this_type(id = self.object.id_registro)
        return context

class IngresoReclamoGarantiaMaterialDeleteView(BSModalDeleteView):
    model = IngresoReclamoGarantiaDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.get_object().ingreso_garantia.id})



    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        return context



class IngresoReclamoGarantiaGuardarView(BSModalDeleteView):
    model = IngresoReclamoGarantia
    template_name = "garantia/ingreso_garantia/form_guardar.html"
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            nro_ingreso_garantia = IngresoReclamoGarantia.objects.all().aggregate(Count('nro_ingreso_garantia'))['nro_ingreso_garantia__count'] + 1
            self.object.nro_ingreso_garantia = nro_ingreso_garantia
            self.object.fecha_ingreso = datetime. now()

            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_INGRESO_RECLAMO_GARANTIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaGuardarView, self).get_context_data(**kwargs)
        context['accion'] = "Guardar"
        context['titulo'] = "Ingreso Garantia"
        context['guardar'] = "true"
        context['item'] = self.object.cliente
        return context

class IngresoControlCalidadView(BSModalDeleteView):
    model = IngresoReclamoGarantia
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            detalles = self.object.IngresoReclamoGarantiaDetalle_ingreso_garantia.all()
   
            calidad_garantia = ControlCalidadReclamoGarantia.objects.create(
                ingreso_garantia = self.object,
                cliente = self.object.cliente,
                sociedad = self.object.sociedad,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            for detalle in detalles:
                ControlCalidadReclamoGarantiaDetalle.objects.create(
                    item = detalle.item,
                    content_type = detalle.content_type,
                    id_registro = detalle.id_registro,
                    cantidad = detalle.cantidad,
                    calidad_garantia = calidad_garantia,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_CONTROL_RECLAMO_GARANTIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(IngresoControlCalidadView, self).get_context_data(**kwargs)
        context['accion'] = "Control"
        context['titulo'] = "Calidad"
        context['texto'] = "¿Está seguro de generar el Control de Calidad?"
        # context['item'] = "Control %s - %s" % (numeroXn(self.object.nro_calidad_garantia, 6), self.object.cliente)
        return context


######################### CONTROL RECLAMO GARANTÍA ##############################################


class ControlCalidadReclamoGarantiaListView(FormView):
    template_name = 'garantia/control_calidad_garantia/inicio.html'
    form_class = ControlCalidadReclamoGarantiaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ControlCalidadReclamoGarantiaListView, self).get_form_kwargs()
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadReclamoGarantiaListView, self).get_context_data(**kwargs)
        contexto_control_garantia = ControlCalidadReclamoGarantia.objects.exclude(estado=3)
        try:
            contexto_control_garantia = contexto_control_garantia.filter(control_garantia__id = self.kwargs['id_control'])
        except:
            pass
        
        filtro_estado = self.request.GET.get('estado')
        filtro_cliente = self.request.GET.get('cliente')

        context['contexto_control_garantia'] = contexto_control_garantia
        return context

class ControlCalidadReclamoGarantiaVerView(TemplateView):
    template_name = "garantia/control_calidad_garantia/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = ControlCalidadReclamoGarantia.objects.get(id = kwargs['id_control'])

        materiales = None
        try:
            materiales = obj.ControlCalidadReclamoGarantiaDetalle_calidad_garantia.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass


        context = super(ControlCalidadReclamoGarantiaVerView, self).get_context_data(**kwargs)
        context['control'] = obj
        context['ingreso'] = obj.ingreso_garantia
        context['materiales'] = materiales
    
        return context

def ControlCalidadReclamoGarantiaVerTabla(request, id_control):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/control_calidad_garantia/detalle_tabla.html'
        obj = ControlCalidadReclamoGarantia.objects.get(id=id_control)

        materiales = None
        try:
            materiales = obj.ControlCalidadReclamoGarantiaDetalle_calidad_garantia.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = {}
        context['control'] = obj
        context['ingreso'] = obj.ingreso_garantia
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ControlCalidadReclamoGarantiaDeleteView(BSModalDeleteView):
    model = ControlCalidadReclamoGarantia
    template_name = "includes/eliminar generico.html"
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadReclamoGarantiaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Control Calidad Reclamo"
        context['item'] = "Garantia - %s" % (self.object.cliente)
        return context


class ControlCalidadReclamoGarantiaEncargadoView(BSModalUpdateView):
    model = ControlCalidadReclamoGarantia
    template_name = "garantia/control_calidad_garantia/form_cliente.html"
    form_class = ControlCalidadReclamoGarantiaEncargadoForm
    success_url = '.'

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadReclamoGarantiaEncargadoView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Encargado"
        return context

class ControlCalidadReclamoGarantiaObservacionUpdateView(BSModalUpdateView):
    model = ControlCalidadReclamoGarantia
    template_name = "includes/formulario generico.html"
    form_class = ControlCalidadReclamoGarantiaObservacionForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadReclamoGarantiaObservacionUpdateView, self).get_context_data(**kwargs)
        
        context['titulo'] = "Actualizar Observaciones"
        context['observaciones'] = self.object.observacion
        context['id_control'] = self.object.id
        return context


class ControlSalidaGarantiaView(BSModalDeleteView):
    model = ControlCalidadReclamoGarantia
    template_name = "includes/form generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:control_garantia_ver', kwargs={'id_control':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()

        try:
            self.object = self.get_object()
            detalles = self.object.ControlCalidadReclamoGarantiaDetalle_calidad_garantia.all()

            salida_garantia = SalidaReclamoGarantia.objects.create(
                control_garantia = self.object,
                cliente = self.object.cliente,
                sociedad = self.object.sociedad,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            for detalle in detalles:
                SalidaReclamoGarantiaDetalle.objects.create(
                    item = detalle.item,
                    content_type = detalle.content_type,
                    id_registro = detalle.id_registro,
                    cantidad = detalle.cantidad,
                    salida_garantia = salida_garantia,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_SALIDA_RECLAMO_GARANTIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ControlSalidaGarantiaView, self).get_context_data(**kwargs)
        context['accion'] = "Salida"
        context['titulo'] = "Garantia"
        context['texto'] = "¿Está seguro de generar la Salida de Garantia?"
        # context['item'] = "Control %s - %s" % (numeroXn(self.object.nro_calidad_garantia, 6), self.object.cliente)
        return context




######################### SALIDA RECLAMO GARANTÍA ##############################################


class SalidaReclamoGarantiaListView(FormView):
    template_name = 'garantia/salida_garantia/inicio.html'
    form_class = SalidaReclamoGarantiaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(SalidaReclamoGarantiaListView, self).get_form_kwargs()
        kwargs['filtro_estado'] = self.request.GET.get('estado')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SalidaReclamoGarantiaListView, self).get_context_data(**kwargs)
        contexto_salida_garantia = SalidaReclamoGarantia.objects.exclude(estado=3)
        try:
            contexto_salida_garantia = contexto_salida_garantia.filter(salida_garantia__id = self.kwargs['id_salida'])
        except:
            pass
        
        filtro_estado = self.request.GET.get('estado')
        filtro_cliente = self.request.GET.get('cliente')

        context['contexto_salida_garantia'] = contexto_salida_garantia
        return context

class SalidaReclamoGarantiaVerView(TemplateView):
    template_name = "garantia/salida_garantia/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = SalidaReclamoGarantia.objects.get(id = kwargs['id_salida'])

        materiales = None
        try:
            materiales = obj.SalidaReclamoGarantiaDetalle_salida_garantia.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass


        context = super(SalidaReclamoGarantiaVerView, self).get_context_data(**kwargs)
        context['salida'] = obj
        context['control'] = obj.control_garantia
        context['materiales'] = materiales
    
        return context

def SalidaReclamoGarantiaVerTabla(request, id_salida):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/salida_garantia/detalle_tabla.html'
        obj = SalidaReclamoGarantia.objects.get(id=id_salida)

        materiales = None
        try:
            materiales = obj.SalidaReclamoGarantiaDetalle_salida_garantia.all()

            for material in materiales:
                material.material = material.content_type.get_object_for_this_type(id = material.id_registro)
        except:
            pass

        context = {}
        context['salida'] = obj
        context['control'] = obj.control_garantia
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class SalidadReclamoGarantiaDeleteView(BSModalDeleteView):
    model = SalidaReclamoGarantia
    template_name = "includes/eliminar generico.html"
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(SalidadReclamoGarantiaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Salida Reclamo"
        context['item'] = "Garantia - %s" % (self.object.cliente)
        return context


class SalidaReclamoGarantiaEncargadoView(BSModalUpdateView):
    model = SalidaReclamoGarantia
    template_name = "garantia/salida_garantia/form_cliente.html"
    form_class = SalidaReclamoGarantiaEncargadoForm
    success_url = '.'

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SalidaReclamoGarantiaEncargadoView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Encargado"
        return context

class SalidaReclamoGarantiaObservacionUpdateView(BSModalUpdateView):
    model = SalidaReclamoGarantia
    template_name = "includes/formulario generico.html"
    form_class = SalidaReclamoGarantiaObservacionForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(SalidaReclamoGarantiaObservacionUpdateView, self).get_context_data(**kwargs)
        
        context['titulo'] = "Actualizar Observaciones"
        context['observaciones'] = self.object.observacion
        context['id_control'] = self.object.id
        return context
