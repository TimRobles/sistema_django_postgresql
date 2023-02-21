from django import forms
from applications.importaciones import*
from applications.funciones import registrar_excepcion

from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.sociedad.models import Sociedad


from .models import(
    IngresoReclamoGarantia,
    IngresoReclamoGarantiaDetalle,
    ControlCalidadReclamoGarantia,
    SalidaReclamoGarantia,
)
from .forms import(
    IngresoReclamoGarantiaBuscarForm,
    IngresoReclamoGarantiaClienteForm,
    IngresoReclamoGarantiaEncargadoForm,
    IngresoReclamoGarantiaSociedadForm,
    IngresoReclamoGarantiaObservacionForm,
    IngresoReclamoGarantiaMaterialForm,
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

                print(material, material.id, cantidad, item, item + 1)

                obj, created = IngresoReclamoGarantiaDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    estado = 1,
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




