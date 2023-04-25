from decimal import Decimal
from django import forms
from django.core.paginator import Paginator
from applications.calidad.models import EstadoSerie, HistorialEstadoSerie, Serie, SerieConsulta, SolucionMaterial
from applications.comprobante_venta.models import BoletaVenta, BoletaVentaDetalle, FacturaVenta, FacturaVentaDetalle
from applications.garantia.pdf import generarIngresoReclamoGarantia, generarSalidaReclamoGarantia
from applications.importaciones import*
from applications.funciones import fecha_en_letras, registrar_excepcion, numeroXn

from applications.clientes.models import ClienteInterlocutor, InterlocutorCliente
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoMovimiento
from applications.sociedad.models import Sociedad


from .models import(
    CondicionesGarantia,
    IngresoReclamoGarantia,
    IngresoReclamoGarantiaDetalle,
    ControlCalidadReclamoGarantia,
    ControlCalidadReclamoGarantiaDetalle,
    SalidaReclamoGarantia,
    SerieIngresoReclamoGarantiaDetalle,
    SerieReclamoHistorial,
)
from .forms import(
    IngresoReclamoGarantiaAlmacenForm,
    IngresoReclamoGarantiaBuscarForm,
    IngresoReclamoGarantiaClienteForm,
    IngresoReclamoGarantiaEncargadoForm,
    IngresoReclamoGarantiaSociedadForm,
    IngresoReclamoGarantiaObservacionForm,
    IngresoReclamoGarantiaMaterialForm,
    IngresoReclamoGarantiaMaterialUpdateForm,
    ControlCalidadReclamoGarantiaBuscarForm,
    ControlCalidadReclamoGarantiaObservacionForm,
    RegistrarCambiarCreateForm,
    RegistrarCambiarSinSerieCreateForm,
    RegistrarCambiarSinSerieUpdateForm,
    RegistrarCambiarUpdateForm,
    RegistrarDevolucionCreateForm,
    RegistrarDevolucionUpdateForm,
    RegistrarFallaCreateForm,
    RegistrarFallaUpdateForm,
    RegistrarSolucionCreateForm,
    RegistrarSolucionUpdateForm,
    SalidaReclamoGarantiaBuscarForm,
    SalidaReclamoGarantiaEncargadoForm,
    SalidaReclamoGarantiaObservacionForm,
    SerieIngresoReclamoGarantiaComentarioForm,
    SerieIngresoReclamoGarantiaDetalleForm,
    SerieIngresoReclamoGarantiaDocumentoForm,
)

CONDICIONES_GARANTIA = []
for condicion in list(CondicionesGarantia.objects.values_list('condicion')):
    CONDICIONES_GARANTIA.append(condicion[0])


class IngresoReclamoGarantiaListView(FormView):
    template_name = 'garantia/ingreso_garantia/inicio.html'
    form_class = IngresoReclamoGarantiaBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(IngresoReclamoGarantiaListView, self).get_form_kwargs()
        kwargs['filtro_fecha_ingreso'] = self.request.GET.get('fecha_ingreso')
        kwargs['filtro_nro_ingreso_reclamo_garantia'] = self.request.GET.get('nro_ingreso_reclamo_garantia')
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaListView, self).get_context_data(**kwargs)
        ingreso_reclamo_garantia = IngresoReclamoGarantia.objects.all()

        filtro_fecha_ingreso = self.request.GET.get('fecha_ingreso')
        filtro_nro_ingreso_reclamo_garantia = self.request.GET.get('nro_ingreso_reclamo_garantia')
        filtro_cliente = self.request.GET.get('cliente')
        filtro_sociedad = self.request.GET.get('sociedad')

        contexto_filtro = []
        if filtro_fecha_ingreso:
            condicion = Q(fecha_ingreso = datetime.strptime(filtro_fecha_ingreso, "%Y-%m-%d").date())
            ingreso_reclamo_garantia = ingreso_reclamo_garantia.filter(condicion)
            contexto_filtro.append("fecha_ingreso=" + filtro_fecha_ingreso)

        if filtro_nro_ingreso_reclamo_garantia:
            condicion = Q(numero_nota__icontains = filtro_nro_ingreso_reclamo_garantia)
            ingreso_reclamo_garantia = ingreso_reclamo_garantia.filter(condicion)
            contexto_filtro.append("nro_ingreso_reclamo_garantia=" + filtro_nro_ingreso_reclamo_garantia)

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            ingreso_reclamo_garantia = ingreso_reclamo_garantia.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_sociedad:
            condicion = Q(sociedad__id = filtro_sociedad)
            ingreso_reclamo_garantia = ingreso_reclamo_garantia.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['contexto_ingreso_garantia'] = ingreso_reclamo_garantia
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
    
        materiales = IngresoReclamoGarantia.objects.ver_detalle(kwargs['id_ingreso'])

        context = super(IngresoReclamoGarantiaVerView, self).get_context_data(**kwargs)
        context['ingreso'] = obj
        context['materiales'] = materiales

        return context

def IngresoReclamoGarantiaVerTabla(request, id_ingreso):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/ingreso_garantia/detalle_tabla.html'
        obj = IngresoReclamoGarantia.objects.get(id=id_ingreso)

        materiales = IngresoReclamoGarantia.objects.ver_detalle(id_ingreso)

        context = {}
        context['ingreso'] = obj
        context['materiales'] = materiales

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
    template_name = "includes/formulario generico.html"
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

class IngresoReclamoGarantiaAlmacenView(BSModalUpdateView):
    model = IngresoReclamoGarantia
    template_name = "includes/formulario generico.html"
    form_class = IngresoReclamoGarantiaAlmacenForm
    success_url = reverse_lazy('garantia_app:ingreso_garantia_inicio')

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaAlmacenView, self).get_context_data(**kwargs)
        context['accion'] = "Elegir"
        context['titulo'] = "Almacen"
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
                item = len(IngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia = ingreso))

                material = form.cleaned_data.get('material')
                cantidad = form.cleaned_data.get('cantidad')

                obj, created = IngresoReclamoGarantiaDetalle.objects.get_or_create(
                    content_type = ContentType.objects.get_for_model(material),
                    id_registro = material.id,
                    ingreso_reclamo_garantia = ingreso,
                )

                if created:
                    obj.item = item + 1
                    obj.cantidad = cantidad
                else:
                    obj.cantidad = obj.cantidad + cantidad  

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
        return reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.get_object().ingreso_reclamo_garantia.id})

    def get_context_data(self, **kwargs):
        context = super(IngresoReclamoGarantiaMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object().content_type.get_object_for_this_type(id = self.get_object().id_registro)
        return context

class IngresoReclamoGarantiaGuardarView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('garantia.change_ingresoreclamogarantia')
    model = IngresoReclamoGarantia
    template_name = "garantia/ingreso_garantia/form_guardar.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        ingreso_reclamo_garantia = self.get_object()
        error_cliente = True
        error_sociedad = True
        error_almacen = True
        error_series = False
        context['titulo'] = 'Error de guardar'
        if ingreso_reclamo_garantia.cliente and ingreso_reclamo_garantia.cliente_interlocutor:
            error_cliente = False
        if ingreso_reclamo_garantia.sociedad:
            error_sociedad = False
        if ingreso_reclamo_garantia.almacen:
            error_almacen = False
        for detalle in ingreso_reclamo_garantia.detalles:
            if detalle.cantidad != detalle.series:
                error_series = True
        
        if error_cliente:
            context['texto'] = 'Elegir un cliente.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_sociedad:
            context['texto'] = 'Elegir una sociedad.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_almacen:
            context['texto'] = 'Elegir un almacen.'
            return render(request, 'includes/modal sin permiso.html', context)
        if error_series:
            context['texto'] = 'Registrar las series.'
            return render(request, 'includes/modal sin permiso.html', context)

        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super(IngresoReclamoGarantiaGuardarView, self).dispatch(request, *args, **kwargs)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.get_object().id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            ingreso_reclamo_garantia = self.get_object()
            ingreso_reclamo_garantia.estado = 2
            nro_ingreso_reclamo_garantia = IngresoReclamoGarantia.objects.all().aggregate(Count('nro_ingreso_reclamo_garantia'))['nro_ingreso_reclamo_garantia__count'] + 1
            ingreso_reclamo_garantia.nro_ingreso_reclamo_garantia = nro_ingreso_reclamo_garantia
            ingreso_reclamo_garantia.fecha_ingreso = datetime. now()
            registro_guardar(ingreso_reclamo_garantia, self.request)
            ingreso_reclamo_garantia.save()

            #Movimiento de Despachado a reclamo garantía
            movimiento_final = TipoMovimiento.objects.get(codigo=128) #Ingreso por reclamo de garantía
            estado_serie = EstadoSerie.objects.get(numero_estado=6) #DEVUELTO
            for detalle in ingreso_reclamo_garantia.detalles:
                #Movimiento de Estado
                for serie in detalle.SerieIngresoReclamoGarantiaDetalle_ingreso_reclamo_garantia_detalle.all():
                    almacen = None
                    if serie.serie.almacen:
                        almacen = serie.serie.almacen
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(ingreso_reclamo_garantia),
                        id_registro_documento_proceso=ingreso_reclamo_garantia.id,
                        almacen=almacen,
                        sociedad=ingreso_reclamo_garantia.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=detalle.content_type,
                        id_registro_producto=detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(ingreso_reclamo_garantia),
                        id_registro_documento_proceso=ingreso_reclamo_garantia.id,
                        almacen=ingreso_reclamo_garantia.almacen,
                        sociedad=ingreso_reclamo_garantia.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    HistorialEstadoSerie.objects.create(
                        serie=serie.serie,
                        estado_serie=estado_serie,
                        falla_material=None,
                        solucion=None,
                        observacion=serie.comentario,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    serie.serie.serie_movimiento_almacen.add(movimiento_uno)
                    serie.serie.serie_movimiento_almacen.add(movimiento_dos)
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
        return reverse_lazy('garantia_app:control_garantia_ver', kwargs={'id_control':self.kwargs['id_control']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            
            control_calidad_garantia = ControlCalidadReclamoGarantia.objects.create(
                ingreso_reclamo_garantia = self.object,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            self.object.estado = 3
            registro_guardar(self.object, self.request)
            self.object.save()
            self.kwargs['id_control'] = control_calidad_garantia.id

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
        return context


class SerieIngresoReclamoGarantiaView(PermissionRequiredMixin, FormView):
    permission_required = ('garantia.change_ingresoreclamogarantia')
    template_name = 'garantia/ingreso_garantia/serie.html'
    form_class = SerieIngresoReclamoGarantiaDetalleForm
    success_url = '.'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, '403.html')
        return super(SerieIngresoReclamoGarantiaView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SerieIngresoReclamoGarantiaView, self).get_form_kwargs()
        if self.serie_encontrada == "Serie encontrada":
            kwargs['filtro_serie_base'] = None
        else:
            kwargs['filtro_serie_base'] = self.request.GET.get('serie_base')
        return kwargs
    
    def get(self, request, *args, **kwargs):
        serie_base = self.request.GET.get('serie_base')
        ingreso_reclamo_garantia = IngresoReclamoGarantia.objects.get(id=self.kwargs['id_ingreso'])
        self.serie_encontrada = ""
        if serie_base:
            try:
                serie = Serie.objects.get(serie_base=serie_base)
                print("************************************")
                print(serie)
                item = len(IngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia = ingreso_reclamo_garantia))
                ingreso_reclamo_garantia_detalle, created = IngresoReclamoGarantiaDetalle.objects.get_or_create(
                    content_type = serie.content_type,
                    id_registro = serie.id_registro,
                    ingreso_reclamo_garantia = ingreso_reclamo_garantia,
                )

                if not ingreso_reclamo_garantia.cliente:
                    ingreso_reclamo_garantia.cliente = serie.cliente
                    ingreso_reclamo_garantia.save()
                if not ingreso_reclamo_garantia.sociedad:
                    ingreso_reclamo_garantia.sociedad = serie.sociedad
                    ingreso_reclamo_garantia.save()

                if created:
                    ingreso_reclamo_garantia_detalle.item = item + 1
                    ingreso_reclamo_garantia_detalle.cantidad = 1
                else:
                    if ingreso_reclamo_garantia_detalle.cantidad == ingreso_reclamo_garantia_detalle.series:
                        ingreso_reclamo_garantia_detalle.cantidad = ingreso_reclamo_garantia_detalle.cantidad + 1
                registro_guardar(ingreso_reclamo_garantia_detalle, self.request)
                ingreso_reclamo_garantia_detalle.save()

                print(serie.documento)
                if hasattr(serie.documento, 'nota_salida'):
                    documento = serie.documento.nota_salida.documentos_venta_objeto[-1]
                else:
                    documento = serie.documento

                buscar = SerieIngresoReclamoGarantiaDetalle.objects.filter(
                            ingreso_reclamo_garantia_detalle=ingreso_reclamo_garantia_detalle,
                            serie=serie,
                            content_type_documento=ContentType.objects.get_for_model(documento),
                            id_registro_documento=documento.id,
                        )
                print(buscar)
                print("************************************")
                if len(buscar)>0:
                    self.serie_encontrada = "La serie ya está registrada"
                elif ingreso_reclamo_garantia.cliente == serie.cliente:
                    if ingreso_reclamo_garantia.sociedad == serie.sociedad:
                        SerieIngresoReclamoGarantiaDetalle.objects.create(
                            ingreso_reclamo_garantia_detalle=ingreso_reclamo_garantia_detalle,
                            serie=serie,
                            content_type_documento=ContentType.objects.get_for_model(documento),
                            id_registro_documento=documento.id,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                        self.serie_encontrada = "Serie encontrada"
                    else:
                        self.serie_encontrada = "La serie pertenece a otra SOCIEDAD"
                else:
                    self.serie_encontrada = "La serie pertenece a otro CLIENTE"

            except:
                if len(Serie.objects.filter(serie_base=serie_base)) > 1:
                    self.serie_encontrada = "Serie en más de 1 producto"
                else:
                    try:
                        serie = SerieConsulta.objects.get(serie_base=serie_base)
                        self.serie_encontrada = "Serie antigua"
                    except:
                        self.serie_encontrada = "No se encontró la serie"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SerieIngresoReclamoGarantiaView, self).get_context_data(**kwargs)
        series = SerieIngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia_detalle__ingreso_reclamo_garantia__id=self.kwargs['id_ingreso'])
        context['serie_encontrada'] = self.serie_encontrada
        context['cantidad_series'] = len(series)
        context['series'] = series
        context['regresar'] = reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.kwargs['id_ingreso']})
        context['url_tabla'] = reverse_lazy('garantia_app:serie_ingreso_garantia_tabla', kwargs={'id_ingreso':self.kwargs['id_ingreso']})
        return context


class SerieIngresoReclamoGarantiaDetalleView(PermissionRequiredMixin, FormView):
    permission_required = ('garantia.change_ingresoreclamogarantia')
    template_name = 'garantia/ingreso_garantia/serie.html'
    form_class = SerieIngresoReclamoGarantiaDetalleForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        context = {}
        ingreso_reclamo_garantia = IngresoReclamoGarantia.objects.get(id=self.kwargs['id_ingreso'])
        error_cliente = True
        error_sociedad = True
        context['titulo'] = 'Error de guardar'
        if ingreso_reclamo_garantia.cliente:
            error_cliente = False
        if ingreso_reclamo_garantia.sociedad:
            error_sociedad = False
        
        if error_cliente:
            context['texto'] = 'Elegir un cliente.'
            return render(request, '403.html', context)
        if error_sociedad:
            context['texto'] = 'Elegir una sociedad.'
            return render(request, '403.html', context)

        if not self.has_permission():
            return render(request, '403.html')
        return super(SerieIngresoReclamoGarantiaDetalleView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SerieIngresoReclamoGarantiaDetalleView, self).get_form_kwargs()
        if self.serie_encontrada == "Serie ENCONTRADA" or self.serie_encontrada == "Serie CREADA":
            kwargs['filtro_serie_base'] = None
        else:
            kwargs['filtro_serie_base'] = self.request.GET.get('serie_base')
        return kwargs
    
    def get(self, request, *args, **kwargs):
        serie_base = self.request.GET.get('serie_base')
        ingreso_reclamo_garantia = IngresoReclamoGarantia.objects.get(id=self.kwargs['id_ingreso'])
        ingreso_reclamo_garantia_detalle = IngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
        self.serie_encontrada = ""
        if serie_base:
            try:
                if ingreso_reclamo_garantia_detalle.producto.control_serie:
                    print(serie_base)
                    print(ingreso_reclamo_garantia_detalle.content_type)
                    print(ingreso_reclamo_garantia_detalle.id_registro)
                    serie = Serie.objects.get(
                        serie_base=serie_base,
                        content_type=ingreso_reclamo_garantia_detalle.content_type,
                        id_registro=ingreso_reclamo_garantia_detalle.id_registro,
                        )
                        
                    print(serie.documento)
                    if hasattr(serie.documento, 'nota_salida'):
                        documento = serie.documento.nota_salida.documentos_venta_objeto[-1]
                    else:
                        documento = serie.documento

                    content_type_documento = ContentType.objects.get_for_model(documento)
                    id_registro_documento = documento.id
                    cliente = serie.cliente
                else:
                    serie = Serie.objects.create(
                        serie_base=serie_base,
                        content_type=ingreso_reclamo_garantia_detalle.content_type,
                        id_registro=ingreso_reclamo_garantia_detalle.id_registro,
                        sociedad=ingreso_reclamo_garantia.sociedad,
                        created_by=self.request.user,
                        updated_by=self.request.user,                        
                        )
                    content_type_documento = None
                    id_registro_documento = None
                    cliente = ingreso_reclamo_garantia.cliente
                if ingreso_reclamo_garantia_detalle.producto == serie.producto:
                    if ingreso_reclamo_garantia_detalle.cantidad == ingreso_reclamo_garantia_detalle.series:
                        ingreso_reclamo_garantia_detalle.cantidad = ingreso_reclamo_garantia_detalle.cantidad + 1
                        registro_guardar(ingreso_reclamo_garantia_detalle, self.request)
                        ingreso_reclamo_garantia_detalle.save()

                    if ingreso_reclamo_garantia.cliente == cliente:
                        if ingreso_reclamo_garantia.sociedad == serie.sociedad:
                            SerieIngresoReclamoGarantiaDetalle.objects.create(
                                ingreso_reclamo_garantia_detalle=ingreso_reclamo_garantia_detalle,
                                serie=serie,
                                content_type_documento=content_type_documento,
                                id_registro_documento=id_registro_documento,
                                created_by=self.request.user,
                                updated_by=self.request.user,
                            )
                            if content_type_documento:
                                self.serie_encontrada = "Serie ENCONTRADA"
                            else:
                                self.serie_encontrada = "Serie CREADA"
                        else:
                            self.serie_encontrada = "La serie pertenece a otra SOCIEDAD"
                    else:
                        self.serie_encontrada = "La serie pertenece a otro CLIENTE"
                else:
                    self.serie_encontrada = "La serie pertenece a otro PRODUCTO"

            except Exception as e:
                print(e)
                self.serie_encontrada = "No se encontró la serie"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SerieIngresoReclamoGarantiaDetalleView, self).get_context_data(**kwargs)
        context['ingreso_reclamo_garantia_detalle'] = IngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
        context['serie_encontrada'] = self.serie_encontrada
        context['series'] = SerieIngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia_detalle__id=self.kwargs['id_ingreso_detalle'])
        context['regresar'] = reverse_lazy('garantia_app:ingreso_garantia_ver', kwargs={'id_ingreso':self.kwargs['id_ingreso']})
        return context


def SerieIngresoReclamoGarantiaTabla(request, **kwargs):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/ingreso_garantia/serie_tabla.html'
        context = {}
        if 'id_ingreso_detalle' in kwargs:
            context['series'] = SerieIngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia_detalle__id=kwargs['id_ingreso_detalle'])
        elif 'id_ingreso' in kwargs:
            context['series'] = SerieIngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia_detalle__ingreso_reclamo_garantia__id=kwargs['id_ingreso'])

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class SerieIngresoReclamoGarantiaDetalleUpdateView(BSModalUpdateView):
    model = SerieIngresoReclamoGarantiaDetalle
    template_name = "includes/formulario generico.html"
    form_class = SerieIngresoReclamoGarantiaComentarioForm
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
        context = super(SerieIngresoReclamoGarantiaDetalleUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Comentario"
        return context


class SerieIngresoReclamoGarantiaDetalleDocumentoUpdateView(BSModalUpdateView):
    model = SerieIngresoReclamoGarantiaDetalle
    template_name = "includes/formulario generico.html"
    form_class = SerieIngresoReclamoGarantiaDocumentoForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        serie_ingreso_reclamo_garantia_detalle = self.get_object()
        lista_facturas = []
        for factura in FacturaVentaDetalle.objects.filter(
            content_type=serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
            id_registro=serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
            factura_venta__cliente=serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.cliente,
            ):
            lista_facturas.append(factura.factura_venta.id)
        lista_boletas = []
        for boleta in BoletaVentaDetalle.objects.filter(
            content_type=serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
            id_registro=serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
            boleta_venta__cliente=serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.cliente,
            ):
            lista_boletas.append(boleta.boleta_venta.id)
        kwargs['facturas'] = FacturaVenta.objects.filter(id__in=lista_facturas)
        kwargs['boletas'] = BoletaVenta.objects.filter(id__in=lista_boletas)
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            factura = form.cleaned_data.get('factura')
            boleta = form.cleaned_data.get('boleta')
            print(factura)
            print(boleta)
            if factura:
                form.instance.content_type_documento = ContentType.objects.get_for_model(factura)
                form.instance.id_registro_documento = factura.id
            elif boleta:
                form.instance.content_type_documento = ContentType.objects.get_for_model(boleta)
                form.instance.id_registro_documento = boleta.id
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SerieIngresoReclamoGarantiaDetalleDocumentoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Documento"
        return context
    

class SerieIngresoReclamoGarantiaMaterialDeleteView(BSModalDeleteView):
    model = SerieIngresoReclamoGarantiaDetalle
    template_name = "includes/eliminar generico.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:serie_ingreso_garantia_ver', kwargs={'id_ingreso':self.get_object().ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.id})

    def delete(self, request, *args, **kwargs):
        serie_ingreso_reclamo_garantia_detalle = self.get_object()
        if not serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.producto.control_serie:
            id = serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.id
            serie = serie_ingreso_reclamo_garantia_detalle.serie
            serie.delete()
            return HttpResponseRedirect(reverse_lazy('garantia_app:serie_ingreso_garantia_ver', kwargs={'id_ingreso':id}))
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SerieIngresoReclamoGarantiaMaterialDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Material"
        context['item'] = self.get_object()
        return context
    

class IngresoReclamoGarantiaPdfView(View):
    def get(self, request, *args, **kwargs):
        ingreso_reclamo_garantia = IngresoReclamoGarantia.objects.get(id=self.kwargs['id_ingreso'])
        sociedad = ingreso_reclamo_garantia.sociedad
        color = sociedad.color
        vertical = True
        if request.GET.get('vertical'):
            vertical = False
        alinear = 'right'
        logo = [[sociedad.logo.url, alinear]]
        pie_pagina = sociedad.pie_pagina
        fuenteBase = "ComicNeue"

        titulo = 'Ingreso por Reclamo de Garantía %s%s %s' % (sociedad.abreviatura, numeroXn(ingreso_reclamo_garantia.nro_ingreso_reclamo_garantia, 6), str(ingreso_reclamo_garantia.cliente.razon_social))

        Cabecera = {}
        Cabecera['nro_ingreso_reclamo_garantia'] = '%s%s' % (sociedad.abreviatura, numeroXn(ingreso_reclamo_garantia.nro_ingreso_reclamo_garantia, 6))
        Cabecera['fecha_ingreso'] = fecha_en_letras(ingreso_reclamo_garantia.fecha_ingreso)
        Cabecera['razon_social'] = str(ingreso_reclamo_garantia.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[ingreso_reclamo_garantia.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(ingreso_reclamo_garantia.cliente.numero_documento)
        Cabecera['direccion'] = str(ingreso_reclamo_garantia.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(ingreso_reclamo_garantia.cliente_interlocutor)
        Cabecera['observacion'] = ingreso_reclamo_garantia.observacion

        TablaDatos = {}
        for detalle in ingreso_reclamo_garantia.detalles:
            TablaDatos[detalle.producto] = []
            for serie in detalle.series_ingreso:
                TablaDatos[detalle.producto].append(serie)

        condiciones = CONDICIONES_GARANTIA

        buf = generarIngresoReclamoGarantia(titulo, vertical, logo, pie_pagina, Cabecera, TablaDatos, condiciones, color, fuenteBase)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta


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
        contexto_control_garantia = ControlCalidadReclamoGarantia.objects.all()

        filtro_estado = self.request.GET.get('estado')
        filtro_cliente = self.request.GET.get('cliente')

        contexto_filtro = []

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            contexto_control_garantia = contexto_control_garantia.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            contexto_control_garantia = contexto_control_garantia.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(contexto_control_garantia) > objectsxpage:
            paginator = Paginator(contexto_control_garantia, objectsxpage)
            page_number = self.request.GET.get('page')
            contexto_control_garantia = paginator.get_page(page_number)

        context['contexto_control_garantia'] = contexto_control_garantia
        context['contexto_pagina'] = contexto_control_garantia

        return context

class ControlCalidadReclamoGarantiaVerView(TemplateView):
    template_name = "garantia/control_calidad_garantia/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = ControlCalidadReclamoGarantia.objects.get(id = kwargs['id_control'])

        materiales = IngresoReclamoGarantia.objects.ver_detalle(obj.ingreso_reclamo_garantia.id)

        context = super(ControlCalidadReclamoGarantiaVerView, self).get_context_data(**kwargs)
        context['control'] = obj
        context['ingreso'] = obj.ingreso_reclamo_garantia
        context['materiales'] = materiales
    
        return context

def ControlCalidadReclamoGarantiaVerTabla(request, id_control):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/control_calidad_garantia/detalle_tabla.html'
        obj = ControlCalidadReclamoGarantia.objects.get(id=id_control)

        materiales = IngresoReclamoGarantia.objects.ver_detalle(obj.ingreso_reclamo_garantia.id)

        context = {}
        context['control'] = obj
        context['ingreso'] = obj.ingreso_reclamo_garantia
        context['materiales'] = materiales

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class ControlCalidadReclamoGarantiaObservacionUpdateView(BSModalUpdateView):
    model = ControlCalidadReclamoGarantia
    template_name = "includes/formulario generico.html"
    form_class = ControlCalidadReclamoGarantiaObservacionForm
    success_url = '.'

    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadReclamoGarantiaObservacionUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Observaciones"
        return context


class SerieControlCalidadReclamoGarantiaDetalleView(PermissionRequiredMixin, TemplateView):
    permission_required = ('garantia.change_controlcalidadreclamogarantia')
    template_name = 'garantia/control_calidad_garantia/serie.html'

    def get_context_data(self, **kwargs):
        context = super(SerieControlCalidadReclamoGarantiaDetalleView, self).get_context_data(**kwargs)
        series = SerieIngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia_detalle__id=self.kwargs['id_ingreso_detalle'])
        ingreso_reclamo_garantia_detalle = series[0].ingreso_reclamo_garantia_detalle
        context['series'] = series
        context['ingreso_reclamo_garantia_detalle'] = ingreso_reclamo_garantia_detalle
        context['regresar'] = reverse_lazy('garantia_app:control_garantia_ver', kwargs={'id_control':ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia.id})
        return context


def SerieControlCalidadReclamoGarantiaTabla(request, **kwargs):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/control_calidad_garantia/serie_tabla.html'
        context = {}
        series = SerieIngresoReclamoGarantiaDetalle.objects.filter(ingreso_reclamo_garantia_detalle__id=kwargs['id_ingreso_detalle'])
        ingreso_reclamo_garantia_detalle = series[0].ingreso_reclamo_garantia_detalle
        context['series'] = series
        context['ingreso_reclamo_garantia_detalle'] = ingreso_reclamo_garantia_detalle
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class RegistrarFallaCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_historialestadoserie')
    template_name = "includes/formulario generico.html"
    form_class = RegistrarFallaCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
        kwargs = super().get_form_kwargs()
        kwargs['fallas'] = serie.serie.producto.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs
    
    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
                estado_serie = EstadoSerie.objects.get(numero_estado=6) #DEVUELTO
                falla_material = form.cleaned_data.get('falla_material')
                observacion = form.cleaned_data.get('observacion')
                historial_estado_serie = HistorialEstadoSerie.objects.create(
                    estado_serie = estado_serie,
                    serie = serie.serie,
                    falla_material=falla_material,
                    observacion=observacion,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                SerieReclamoHistorial.objects.create(
                    serie_ingreso_reclamo_garantia_detalle = serie,
                    historia_estado_serie = historial_estado_serie,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarFallaCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Falla"
        return context


class RegistrarFallaUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_historialestadoserie')
    model = HistorialEstadoSerie
    template_name = "includes/formulario generico.html"
    form_class = RegistrarFallaUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['fallas'] = self.get_object().serie.producto.subfamilia.FallaMaterial_sub_familia.filter(visible=True)
        return kwargs
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        self.request.session['primero'] = False
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarFallaUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Falla"
        return context


class RegistrarFallaDeleteView(BSModalDeleteView):
    model = HistorialEstadoSerie
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self) -> str:
        return reverse_lazy('garantia_app:serie_contro_ingreso_garantia_ver', kwargs={'id_ingreso_detalle':self.kwargs['id_ingreso_detalle']})

    def get_context_data(self, **kwargs):
        context = super(RegistrarFallaDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Falla"
        context['item'] = self.get_object()
        return context


class RegistrarSolucionCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_historialestadoserie')
    template_name = "includes/formulario generico.html"
    form_class = RegistrarSolucionCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
        kwargs = super().get_form_kwargs()
        fallas = []
        for falla in serie.serie.producto.subfamilia.FallaMaterial_sub_familia.filter(visible=True):
            fallas.append(falla.id)
        kwargs['soluciones'] = SolucionMaterial.objects.filter(falla_material__id__in=fallas, visible=True)
        return kwargs
    
    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
                estado_serie = EstadoSerie.objects.get(numero_estado=5) #REPARADO
                solucion = form.cleaned_data.get('solucion')
                observacion = form.cleaned_data.get('observacion')
                comentario = form.cleaned_data.get('comentario')
                ControlCalidadReclamoGarantiaDetalle.objects.create(
                    control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                    serie_ingreso_reclamo_garantia_detalle=serie,
                    serie_cambio=None,
                    tipo_analisis=1, #Solucionado
                    comentario=comentario,
                )
                historial_estado_serie = HistorialEstadoSerie.objects.create(
                    estado_serie = estado_serie,
                    serie = serie.serie,
                    solucion=solucion,
                    observacion=observacion,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                SerieReclamoHistorial.objects.create(
                    serie_ingreso_reclamo_garantia_detalle = serie,
                    historia_estado_serie = historial_estado_serie,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarSolucionCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Solucion"
        return context


class RegistrarSolucionUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_historialestadoserie')
    model = HistorialEstadoSerie
    template_name = "includes/formulario generico.html"
    form_class = RegistrarSolucionUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        fallas = []
        for falla in self.get_object().serie.producto.subfamilia.FallaMaterial_sub_familia.filter(visible=True):
            fallas.append(falla.id)
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        kwargs['soluciones'] = SolucionMaterial.objects.filter(falla_material__id__in=fallas, visible=True)
        kwargs['comentario'] = control.comentario
        return kwargs
    
    def form_valid(self, form):
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        comentario = form.cleaned_data.get('comentario')
        control.comentario = comentario
        control.save()
        registro_guardar(form.instance, self.request)
        self.request.session['primero'] = False
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarSolucionUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Solucion"
        return context


class RegistrarSolucionDeleteView(BSModalDeleteView):
    model = HistorialEstadoSerie
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self) -> str:
        return reverse_lazy('garantia_app:serie_contro_ingreso_garantia_ver', kwargs={'id_ingreso_detalle':self.kwargs['id_ingreso_detalle']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
            control = ControlCalidadReclamoGarantiaDetalle.objects.get(
                control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                serie_ingreso_reclamo_garantia_detalle=serie,
            )
            control.serie_cambio.ultimo_estado.delete()
            control.delete()
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RegistrarSolucionDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Solucion"
        context['item'] = self.get_object()
        return context


class RegistrarCambiarCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_historialestadoserie')
    template_name = "includes/formulario generico.html"
    form_class = RegistrarCambiarCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
                estado_serie = EstadoSerie.objects.get(numero_estado=14) #POR CAMBIAR
                estado_reservar_serie = EstadoSerie.objects.get(numero_estado=13) #RESERVADO POR CAMBIO
                serie_buscar = form.cleaned_data.get('serie_cambio')
                observacion = form.cleaned_data.get('observacion')
                comentario = form.cleaned_data.get('comentario')
                try:
                    serie_cambio = Serie.objects.get(
                        serie_base = serie_buscar,
                        content_type = serie.serie.content_type,
                        id_registro = serie.serie.id_registro,
                        sociedad = serie.serie.sociedad,
                    )
                    print(serie_cambio)
                except:
                    form.add_error('serie_cambio', 'Serie no encontrada')
                    return super().form_invalid(form)

                ControlCalidadReclamoGarantiaDetalle.objects.create(
                    control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                    serie_ingreso_reclamo_garantia_detalle=serie,
                    serie_cambio=serie_cambio,
                    tipo_analisis=2, #Cambio
                    comentario=comentario,
                )

                reservar_serie = HistorialEstadoSerie.objects.create(
                    estado_serie = estado_reservar_serie,
                    serie = serie_cambio,
                    solucion=None,
                    observacion=None,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                historial_estado_serie = HistorialEstadoSerie.objects.create(
                    estado_serie = estado_serie,
                    serie = serie.serie,
                    solucion=None,
                    observacion=observacion,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                SerieReclamoHistorial.objects.create(
                    serie_ingreso_reclamo_garantia_detalle = serie,
                    historia_estado_serie = historial_estado_serie,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarCambiarCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Cambio"
        return context


class RegistrarCambiarUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_historialestadoserie')
    model = HistorialEstadoSerie
    template_name = "includes/formulario generico.html"
    form_class = RegistrarCambiarUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        kwargs['serie_cambio'] = control.serie_cambio
        kwargs['comentario'] = control.comentario
        return kwargs
    
    def form_valid(self, form):
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        comentario = form.cleaned_data.get('comentario')
        control.comentario = comentario
        control.save()
        registro_guardar(form.instance, self.request)
        self.request.session['primero'] = False
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarCambiarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cambio"
        return context


class RegistrarCambiarDeleteView(BSModalDeleteView):
    model = HistorialEstadoSerie
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self) -> str:
        return reverse_lazy('garantia_app:serie_contro_ingreso_garantia_ver', kwargs={'id_ingreso_detalle':self.kwargs['id_ingreso_detalle']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
            estado_reservar_serie = EstadoSerie.objects.get(numero_estado=13) #RESERVADO POR CAMBIO
            control = ControlCalidadReclamoGarantiaDetalle.objects.get(
                control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                serie_ingreso_reclamo_garantia_detalle=serie,
            )
            reservar_serie = HistorialEstadoSerie.objects.filter(
                    estado_serie = estado_reservar_serie,
                    serie = control.serie_cambio,
                    solucion=None,
                    observacion=None,
                ).latest('id')
            control.delete()
            reservar_serie.delete()
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RegistrarCambiarDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cambio"
        context['item'] = self.get_object()
        return context

class RegistrarCambiarSinSerieCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_historialestadoserie')
    template_name = "includes/formulario generico.html"
    form_class = RegistrarCambiarSinSerieCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
                estado_serie = EstadoSerie.objects.get(numero_estado=14) #POR CAMBIAR
                observacion = form.cleaned_data.get('observacion')
                comentario = form.cleaned_data.get('comentario')
                almacen = form.cleaned_data.get('almacen')
                
                ControlCalidadReclamoGarantiaDetalle.objects.create(
                    control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                    serie_ingreso_reclamo_garantia_detalle=serie,
                    serie_cambio=None,
                    tipo_analisis=2, #Cambio
                    comentario=comentario,
                    almacen=almacen,
                )
                historial_estado_serie = HistorialEstadoSerie.objects.create(
                    serie = serie.serie,
                    estado_serie = estado_serie,
                    observacion=observacion,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                SerieReclamoHistorial.objects.create(
                    serie_ingreso_reclamo_garantia_detalle = serie,
                    historia_estado_serie = historial_estado_serie,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarCambiarSinSerieCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Cambio"
        return context


class RegistrarCambiarSinSerieUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_historialestadoserie')
    model = HistorialEstadoSerie
    template_name = "includes/formulario generico.html"
    form_class = RegistrarCambiarSinSerieUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        kwargs['serie_cambio'] = control.serie_cambio
        kwargs['comentario'] = control.comentario
        kwargs['almacen'] = control.almacen
        return kwargs
    
    def form_valid(self, form):
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        comentario = form.cleaned_data.get('comentario')
        almacen = form.cleaned_data.get('almacen')
        control.comentario = comentario
        control.almacen = almacen
        control.save()
        registro_guardar(form.instance, self.request)
        self.request.session['primero'] = False
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarCambiarSinSerieUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cambio"
        return context


class RegistrarCambiarSinSerieDeleteView(BSModalDeleteView):
    model = HistorialEstadoSerie
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self) -> str:
        return reverse_lazy('garantia_app:serie_contro_ingreso_garantia_ver', kwargs={'id_ingreso_detalle':self.kwargs['id_ingreso_detalle']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
            control = ControlCalidadReclamoGarantiaDetalle.objects.get(
                control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                serie_ingreso_reclamo_garantia_detalle=serie,
            )
            control.delete()
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RegistrarCambiarSinSerieDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cambio"
        context['item'] = self.get_object()
        return context


class RegistrarDevolucionCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('calidad.add_historialestadoserie')
    template_name = "includes/formulario generico.html"
    form_class = RegistrarDevolucionCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_ingreso_detalle'])
                estado_serie = EstadoSerie.objects.get(numero_estado=12) #POR DEVOLVER
                observacion = form.cleaned_data.get('observacion')
                comentario = form.cleaned_data.get('comentario')
                
                ControlCalidadReclamoGarantiaDetalle.objects.create(
                    control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                    serie_ingreso_reclamo_garantia_detalle=serie,
                    serie_cambio=None,
                    tipo_analisis=3, #Devolución
                    comentario=comentario,
                )
                historial_estado_serie = HistorialEstadoSerie.objects.create(
                    serie = serie.serie,
                    estado_serie = estado_serie,
                    observacion=observacion,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                SerieReclamoHistorial.objects.create(
                    serie_ingreso_reclamo_garantia_detalle = serie,
                    historia_estado_serie = historial_estado_serie,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )

                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarDevolucionCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Cambio"
        return context


class RegistrarDevolucionUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('calidad.change_historialestadoserie')
    model = HistorialEstadoSerie
    template_name = "includes/formulario generico.html"
    form_class = RegistrarDevolucionUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('garantia_app:control_garantia_inicio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
        control = ControlCalidadReclamoGarantiaDetalle.objects.get(
            control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
            serie_ingreso_reclamo_garantia_detalle=serie,
        )
        kwargs['serie_cambio'] = control.serie_cambio
        kwargs['comentario'] = control.comentario
        return kwargs
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        self.request.session['primero'] = False
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(RegistrarDevolucionUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cambio"
        return context


class RegistrarDevolucionDeleteView(BSModalDeleteView):
    model = HistorialEstadoSerie
    template_name = "includes/eliminar generico.html"
    
    def get_success_url(self) -> str:
        return reverse_lazy('garantia_app:serie_contro_ingreso_garantia_ver', kwargs={'id_ingreso_detalle':self.kwargs['id_ingreso_detalle']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            serie = SerieIngresoReclamoGarantiaDetalle.objects.get(id=self.kwargs['id_serie_ingreso_detalle'])
            control = ControlCalidadReclamoGarantiaDetalle.objects.get(
                control_calidad_reclamo_garantia=serie.ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia.ControlCalidadReclamoGarantia_ingreso_reclamo_garantia,
                serie_ingreso_reclamo_garantia_detalle=serie,
            )
            control.delete()
            return super().delete(request, *args, **kwargs)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RegistrarDevolucionDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Cambio"
        context['item'] = self.get_object()
        return context


class ControlSalidaGarantiaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('garantia.change_controlcalidadreclamogarantia')
    model = ControlCalidadReclamoGarantia
    template_name = "includes/form generico.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        error_solucionado = False
        context['titulo'] = 'Error de guardar'
        for detalle in self.get_object().ingreso_reclamo_garantia.detalles:
            if detalle.revisados != detalle.cantidad:
                error_solucionado = True
        
        if error_solucionado:
            context['texto'] = 'Falta solucionar algunos productos.'
            return render(request, 'includes/modal sin permiso.html', context)
        
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super(ControlSalidaGarantiaView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:control_garantia_ver', kwargs={'id_control':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()

        try:
            self.object = self.get_object()

            #Generar salidas
            for control in self.object.ControlCalidadReclamoGarantiaDetalle_control_calidad_reclamo_garantia.all():
                if control.tipo_analisis == 2: #CAMBIO
                    if control.serie_cambio:
                        almacen = control.serie_cambio.almacen
                    else:
                        almacen = control.almacen
                    movimiento_final_cambio = TipoMovimiento.objects.get(codigo=115) #Garantía, equipo de cambio
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final_cambio,
                        tipo_stock=movimiento_final_cambio.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=almacen,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final_cambio,
                        tipo_stock=movimiento_final_cambio.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=almacen,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_uno)
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_dos)

            salida_garantia = SalidaReclamoGarantia.objects.create(
                control_calidad_reclamo_garantia = self.object,
                created_by = self.request.user,
                updated_by = self.request.user,
            )

            self.object.estado = 5
            self.object.ingreso_reclamo_garantia.estado = 5
            registro_guardar(self.object.ingreso_reclamo_garantia, self.request)
            self.object.ingreso_reclamo_garantia.save()
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
        contexto_salida_garantia = SalidaReclamoGarantia.objects.all()
        try:
            contexto_salida_garantia = contexto_salida_garantia.filter(salida_garantia__id = self.kwargs['id_salida'])
        except:
            pass
        
        filtro_estado = self.request.GET.get('estado')
        filtro_cliente = self.request.GET.get('cliente')

        contexto_filtro = []

        if filtro_estado:
            condicion = Q(estado = filtro_estado)
            contexto_salida_garantia = contexto_salida_garantia.filter(condicion)
            contexto_filtro.append("estado=" + filtro_estado)
        if filtro_cliente:
            condicion = Q(cliente = filtro_cliente)
            contexto_salida_garantia = contexto_salida_garantia.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)
        
        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(contexto_salida_garantia) > objectsxpage:
            paginator = Paginator(contexto_salida_garantia, objectsxpage)
            page_number = self.request.GET.get('page')
            contexto_salida_garantia = paginator.get_page(page_number)

        context['contexto_salida_garantia'] = contexto_salida_garantia
        context['contexto_pagina'] = contexto_salida_garantia
        return context

class SalidaReclamoGarantiaVerView(TemplateView):
    template_name = "garantia/salida_garantia/detalle.html"
    
    def get_context_data(self, **kwargs):
        obj = SalidaReclamoGarantia.objects.get(id = kwargs['id_salida'])

        materiales = IngresoReclamoGarantia.objects.ver_detalle(obj.control_calidad_reclamo_garantia.ingreso_reclamo_garantia.id)

        context = super(SalidaReclamoGarantiaVerView, self).get_context_data(**kwargs)
        context['salida'] = obj
        context['control'] = obj.control_calidad_reclamo_garantia
        context['materiales'] = materiales
    
        return context

def SalidaReclamoGarantiaVerTabla(request, id_salida):
    data = dict()
    if request.method == 'GET':
        template = 'garantia/salida_garantia/detalle_tabla.html'
        obj = SalidaReclamoGarantia.objects.get(id=id_salida)

        materiales = IngresoReclamoGarantia.objects.ver_detalle(obj.control_calidad_reclamo_garantia.ingreso_reclamo_garantia.id)

        context = {}
        context['salida'] = obj
        context['control'] = obj.control_calidad_reclamo_garantia
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


class SalidaReclamoGarantiaObservacionUpdateView(BSModalUpdateView):
    model = SalidaReclamoGarantia
    template_name = "includes/formulario generico.html"
    form_class = SalidaReclamoGarantiaObservacionForm
    success_url = '.'
    
    def form_valid(self, form):
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SalidaReclamoGarantiaObservacionUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Observaciones"
        context['observaciones'] = self.object.observacion
        context['id_control'] = self.object.id
        return context

class SalidadReclamoGarantiaEntregarView(BSModalDeleteView):
    model = SalidaReclamoGarantia
    template_name = "includes/eliminar generico.html"
    success_url = '.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('garantia_app:salida_garantia_ver', kwargs={'id_salida':self.object.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()

        try:
            self.object = self.get_object()
            self.object.fecha_salida = date.today()

            #Generar salidas
            for control in self.object.control_calidad_reclamo_garantia.ControlCalidadReclamoGarantiaDetalle_control_calidad_reclamo_garantia.all():
                if control.tipo_analisis == 1: #SOLUCIONADO
                    estado_serie = EstadoSerie.objects.get(numero_estado=3) #Vendido
                    movimiento_final = TipoMovimiento.objects.get(codigo=123) #Garantía, equipo revisado, reparado
                    HistorialEstadoSerie.objects.create(
                        serie=control.serie_ingreso_reclamo_garantia_detalle.serie,
                        estado_serie=estado_serie,
                        falla_material=None,
                        solucion=None,
                        observacion=None,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_uno)
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_dos)
                elif control.tipo_analisis == 2: #CAMBIO
                    estado_serie = EstadoSerie.objects.get(numero_estado=2) #Con Problemas
                    movimiento_final = TipoMovimiento.objects.get(codigo=124) #Garantía, equipo revisado, malogrado
                    HistorialEstadoSerie.objects.create(
                        serie=control.serie_ingreso_reclamo_garantia_detalle.serie,
                        estado_serie=estado_serie,
                        falla_material=None,
                        solucion=None,
                        observacion=None,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_uno)
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_dos)

                    estado_serie_cambio = EstadoSerie.objects.get(numero_estado=3) #Vendido
                    movimiento_final_cambio = TipoMovimiento.objects.get(codigo=116) #Garantía, entrega del equipo
                    if control.serie_cambio:
                        HistorialEstadoSerie.objects.create(
                            serie=control.serie_cambio,
                            estado_serie=estado_serie_cambio,
                            falla_material=None,
                            solucion=None,
                            observacion=None,
                            created_by=self.request.user,
                            updated_by=self.request.user,
                        )
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final_cambio,
                        tipo_stock=movimiento_final_cambio.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final_cambio,
                        tipo_stock=movimiento_final_cambio.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    if control.serie_cambio:
                        control.serie_cambio.serie_movimiento_almacen.add(movimiento_uno)
                        control.serie_cambio.serie_movimiento_almacen.add(movimiento_dos)

                elif control.tipo_analisis == 3: #DEVOLUCION
                    estado_serie = EstadoSerie.objects.get(numero_estado=3) #Vendido
                    movimiento_final = TipoMovimiento.objects.get(codigo=125) #Garantía, equipo devuelto
                    HistorialEstadoSerie.objects.create(
                        serie=control.serie_ingreso_reclamo_garantia_detalle.serie,
                        estado_serie=estado_serie,
                        falla_material=None,
                        solucion=None,
                        observacion=None,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_uno = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_inicial,
                        signo_factor_multiplicador=-1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=None,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    movimiento_dos = MovimientosAlmacen.objects.create(
                        content_type_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.content_type,
                        id_registro_producto=control.serie_ingreso_reclamo_garantia_detalle.ingreso_reclamo_garantia_detalle.id_registro,
                        cantidad=1,
                        tipo_movimiento=movimiento_final,
                        tipo_stock=movimiento_final.tipo_stock_final,
                        signo_factor_multiplicador=+1,
                        content_type_documento_proceso=ContentType.objects.get_for_model(self.object),
                        id_registro_documento_proceso=self.object.id,
                        almacen=None,
                        sociedad=self.object.sociedad,
                        movimiento_anterior=movimiento_uno,
                        movimiento_reversion=False,
                        transformacion=False,
                        created_by=self.request.user,
                        updated_by=self.request.user,
                    )
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_uno)
                    control.serie_ingreso_reclamo_garantia_detalle.serie.serie_movimiento_almacen.add(movimiento_dos)

            self.object.estado = 6
            self.object.control_calidad_reclamo_garantia.estado = 6
            registro_guardar(self.object.control_calidad_reclamo_garantia, self.request)
            self.object.control_calidad_reclamo_garantia.save()
            self.object.control_calidad_reclamo_garantia.ingreso_reclamo_garantia.estado = 6
            registro_guardar(self.object.control_calidad_reclamo_garantia.ingreso_reclamo_garantia, self.request)
            self.object.control_calidad_reclamo_garantia.ingreso_reclamo_garantia.save()
            registro_guardar(self.object, self.request)
            self.object.save()

            messages.success(request, MENSAJE_SALIDA_RECLAMO_GARANTIA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SalidadReclamoGarantiaEntregarView, self).get_context_data(**kwargs)
        context['accion'] = "Entregar"
        context['titulo'] = "Salida Reclamo"
        context['item'] = "Garantia - %s" % (self.object.cliente)
        return context


class SalidaReclamoGarantiaPdfView(View):
    def get(self, request, *args, **kwargs):
        salida_reclamo_garantia = SalidaReclamoGarantia.objects.get(id=self.kwargs['id_salida'])
        sociedad = salida_reclamo_garantia.sociedad
        color = sociedad.color
        vertical = True
        if request.GET.get('vertical'):
            vertical = False
        alinear = 'right'
        logo = [[sociedad.logo.url, alinear]]
        pie_pagina = sociedad.pie_pagina
        fuenteBase = "ComicNeue"

        titulo = 'Salida por Reclamo de Garantía %s%s %s' % (sociedad.abreviatura, numeroXn(salida_reclamo_garantia.nro_salida_garantia, 6), str(salida_reclamo_garantia.cliente.razon_social))

        Cabecera = {}
        Cabecera['nro_salida_garantia'] = '%s%s' % (sociedad.abreviatura, numeroXn(salida_reclamo_garantia.nro_salida_garantia, 6))
        Cabecera['fecha_salida'] = fecha_en_letras(salida_reclamo_garantia.fecha_salida)
        Cabecera['razon_social'] = str(salida_reclamo_garantia.cliente)
        Cabecera['tipo_documento'] = DICCIONARIO_TIPO_DOCUMENTO_SUNAT[salida_reclamo_garantia.cliente.tipo_documento]
        Cabecera['nro_documento'] = str(salida_reclamo_garantia.cliente.numero_documento)
        Cabecera['direccion'] = str(salida_reclamo_garantia.cliente.direccion_fiscal)
        Cabecera['interlocutor'] = str(salida_reclamo_garantia.cliente_interlocutor)
        Cabecera['observacion'] = salida_reclamo_garantia.observacion

        TablaDatos = {}
        for detalle in salida_reclamo_garantia.control_calidad_reclamo_garantia.ingreso_reclamo_garantia.detalles:
            TablaDatos[detalle.producto] = []
            for serie in detalle.series_control:
                TablaDatos[detalle.producto].append(serie)

        condiciones = CONDICIONES_GARANTIA

        buf = generarSalidaReclamoGarantia(titulo, vertical, logo, pie_pagina, Cabecera, TablaDatos, condiciones, color, fuenteBase)

        respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
        respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

        return respuesta