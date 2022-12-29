from decimal import Decimal
from django.core.paginator import Paginator
from datetime import timedelta
from reportlab.lib import colors
from applications.clientes.models import Cliente
from applications.cobranza.funciones import movimientos_bancarios
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda, TipoCambio
from applications.funciones import registrar_excepcion, tipo_de_cambio
from applications.importaciones import *
from .models import(
    Deuda,
    Ingreso,
    LineaCredito,
    Pago,
    Redondeo,
)

from .forms import(
    CuentaBancariaEfectivoIngresoForm,
    CuentaBancariaIngresoCambiarForm,
    CuentaBancariaIngresoForm,
    CuentaBancariaIngresoPagarForm,
    DepositosBuscarForm,
    DeudaPagarForm,
    LineaCreditoForm,
    ClienteBuscarForm,
)

class LineaCreditoView(ListView):
    model = LineaCredito
    template_name = 'cobranza/linea_credito/inicio.html'
    context_object_name = 'contexto_linea_credito'

def LineaCreditoTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'cobranza/linea_credito/inicio_tabla.html'
        context = {}
        context['contexto_linea_credito'] = LineaCredito.objects.all()

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class LineaCreditoCreateView(BSModalCreateView):
    model = LineaCredito
    template_name = "cobranza/linea_credito/form.html"
    form_class = LineaCreditoForm
    success_url = reverse_lazy('cobranza_app:linea_credito_inicio')

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(LineaCreditoCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Linea de Crédito"
        return context


class DeudoresView(FormView): 
    template_name = "cobranza/deudas/inicio.html"
    form_class = ClienteBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(DeudoresView, self).get_form_kwargs()
        kwargs['filtro_razon_social'] = self.request.GET.get('razon_social')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(DeudoresView, self).get_context_data(**kwargs)
        context['moneda'] = Moneda.objects.get(principal=True)

        clientes = Cliente.objects.all()
        filtro_razon_social = self.request.GET.get('razon_social')

        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            clientes = clientes.filter(condicion)
            context['contexto_filtro'] = "?razon_social=" + filtro_razon_social

        objectsxpage =  10 # Show 10 objects per page.

        if len(clientes) > objectsxpage:
            paginator = Paginator(clientes, objectsxpage)
            page_number = self.request.GET.get('page')
            clientes = paginator.get_page(page_number)

        context['contexto_cliente'] = clientes
        context['contexto_pagina'] = clientes

        return context
    

class DeudaView(TemplateView):
    template_name = "cobranza/deudas/detalle.html"
    
    def get_context_data(self, **kwargs):
        context = super(DeudaView, self).get_context_data(**kwargs)
        deudas = Deuda.objects.filter(cliente__id=self.kwargs['id_cliente'])    
        objectsxpage =  10 # Show 10 objects per page.

        if len(deudas) > objectsxpage:
            paginator = Paginator(deudas, objectsxpage)
            page_number = self.request.GET.get('page')
            deudas = paginator.get_page(page_number)

        context['contexto_deuda'] = deudas
        context['contexto_pagina'] = deudas
        context['id_cliente'] = self.kwargs['id_cliente']
        return context


def DeudaTabla(request, id_cliente):
    data = dict()
    if request.method == 'GET':
        template = "cobranza/deudas/detalle tabla.html"
        context = {}
        deudas = Deuda.objects.filter(cliente__id=id_cliente)    
        objectsxpage =  10 # Show 10 objects per page.

        if len(deudas) > objectsxpage:
            paginator = Paginator(deudas, objectsxpage)
            page_number = request.GET.get('page')
            deudas = paginator.get_page(page_number)

        context['contexto_deuda'] = deudas
        context['contexto_pagina'] = deudas
        context['id_cliente'] = id_cliente

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


def DeudaJsonView(request, sociedad_id):
    if request.is_ajax():
        term = request.GET.get('term')
        data = []
        buscar = Deuda.objects.filter(
            sociedad__id=sociedad_id,
            ).filter(
                Q(cliente__razon_social__icontains=term)
            )
        for deuda in buscar:
            if deuda.saldo > 0:
                data.append({
                    'id' : deuda.id,
                    'nombre' : deuda.__str__(),
                    })
        return JsonResponse(data, safe=False)
    

class DeudaPagarCreateView(BSModalFormView):
    template_name = "cobranza/deudas/form pagar.html"
    form_class = DeudaPagarForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:deudores_detalle', kwargs={'id_cliente':self.kwargs['id_cliente']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                deuda = Deuda.objects.get(id=self.kwargs['id_deuda'])
                monto = form.cleaned_data.get('monto')
                tipo_cambio = form.cleaned_data.get('tipo_cambio')
                ingresos = form.cleaned_data.get('ingresos')
                content_type = ContentType.objects.get_for_model(ingresos)
                id_registro = ingresos.id
                obj, created = Pago.objects.get_or_create(
                    deuda = deuda,
                    content_type = content_type,
                    id_registro = id_registro,
                )
                if created:
                    obj.monto = monto
                else:
                    obj.monto = obj.monto + monto
                obj.tipo_cambio = tipo_cambio
                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        deuda = Deuda.objects.get(id=self.kwargs['id_deuda'])
        lista_ingresos = []
        for ingreso in Ingreso.objects.all():
            if ingreso.saldo > 0:
                lista_ingresos.append(ingreso.id)

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio_ingreso = TipoCambio.objects.tipo_cambio_venta(deuda.fecha_deuda)
        tipo_cambio = tipo_de_cambio(tipo_cambio_ingreso, tipo_cambio_hoy)
        kwargs['tipo_cambio'] = tipo_cambio
        kwargs['lista_ingresos'] = lista_ingresos
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        deuda = Deuda.objects.get(id=self.kwargs['id_deuda'])
        context = super(DeudaPagarCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Pagar'
        context['titulo'] = 'Deuda'
        context['deuda'] = deuda
        return context


class DeudaPagarUpdateView(BSModalUpdateView):
    model = Pago
    template_name = "cobranza/deudas/form pagar.html"
    form_class = DeudaPagarForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:deudores_detalle', kwargs={'id_cliente':self.kwargs['id_cliente']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        deuda = Deuda.objects.get(id=self.kwargs['id_deuda'])
        lista_ingresos = []
        for ingreso in Ingreso.objects.all():
            if ingreso.saldo > 0:
                lista_ingresos.append(ingreso.id)
        lista_ingresos.append(self.object.id_registro)
        
        # lista_notas = []
        # for nota in Nota.objects.all():
        #     if nota.saldo > 0:
        #         lista_notas.append(nota.id)
        # if self.object.content_type == ContentType.objects.get_for_model(Ingreso):
        #    lista_ingresos.append(self.object.id_registro)
        # else:
        # lista_notas.append(self.object.id_registro)

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio_ingreso = TipoCambio.objects.tipo_cambio_venta(deuda.fecha_deuda)
        tipo_cambio = tipo_de_cambio(tipo_cambio_ingreso, tipo_cambio_hoy)
        kwargs['tipo_cambio'] = tipo_cambio
        kwargs['lista_ingresos'] = lista_ingresos
        # kwargs['lista_notas'] = lista_notas
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        deuda = Deuda.objects.get(id=self.kwargs['id_deuda'])
        context = super(DeudaPagarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Pago'
        context['deuda'] = deuda
        return context


class DeudaPagarDeleteView(BSModalDeleteView):
    model = Pago
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:deudores_detalle', kwargs={'id_cliente':self.kwargs['id_cliente']})

    def get_context_data(self, **kwargs):
        context = super(DeudaPagarDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Pago'
        context['item'] = self.get_object()
        return context
    

class DeudaCancelarView(BSModalDeleteView):
    model = Deuda
    template_name = "includes/form generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:deudores_detalle', kwargs={'id_cliente':self.kwargs['id_cliente']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                deuda = self.get_object()
                fecha = date.today()
                monto = deuda.saldo
                moneda = deuda.moneda
                tipo_cambio = deuda.tipo_cambio
                Redondeo.objects.create(
                    deuda=deuda,
                    fecha=fecha,
                    monto=monto,
                    moneda=moneda,
                    tipo_cambio=tipo_cambio,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(DeudaCancelarView, self).get_context_data(**kwargs)
        context['accion'] = 'Cancelar'
        context['titulo'] = 'Deuda'
        context['texto'] = '¿Está seguro de Cancelar la deuda?'
        context['item'] = self.get_object()
        return context


class CuentaBancariaView(TemplateView):
    template_name = "bancos/cuenta bancaria/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaView, self).get_context_data(**kwargs)
        context['contexto_cuenta_bancaria'] = CuentaBancariaSociedad.objects.filter(estado=1)
        return context


class CuentaBancariaDetalleView(DetailView):
    model = CuentaBancariaSociedad
    template_name = "bancos/cuenta bancaria/detalle.html"
    context_object_name = 'cuenta_bancaria'

    # def get_context_data(self, **kwargs):
    #     context = super(CuentaBancariaDetalleView, self).get_context_data(**kwargs)
    #     context['movimientos'] = movimientos_bancarios(self.object.id)
    #     return context

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaDetalleView, self).get_context_data(**kwargs)
        movimientos = movimientos_bancarios(self.object.id)
        
        objectsxpage = 25 # Show 25 objects per page.

        if len(movimientos) > objectsxpage:
            paginator = Paginator(movimientos, objectsxpage)
            page_number = self.request.GET.get('page')
            movimientos = paginator.get_page(page_number)
   
        context['contexto_pagina'] = movimientos
        return context


def CuentaBancariaDetalleTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = "bancos/cuenta bancaria/detalle tabla.html"
        context = {}
        # context['cuenta_bancaria'] = CuentaBancariaSociedad.objects.get(id=pk)
        # context['movimientos'] = movimientos_bancarios(pk)

        # data['table'] = render_to_string(
        #     template,
        #     context,
        #     request=request
        # )
        # return JsonResponse(data)

        context['cuenta_bancaria'] = CuentaBancariaSociedad.objects.get(id=pk)
        movimientos = movimientos_bancarios(pk)

        objectsxpage = 25 # Show 25 objects per page.

        if len(movimientos) > objectsxpage:
            paginator = Paginator(movimientos, objectsxpage)
            page_number = request.GET.get('page')
            movimientos = paginator.get_page(page_number)
            
        context['contexto_pagina'] = movimientos

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
    

class CuentaBancariaIngresoPagarCreateView(BSModalFormView):
    template_name = "bancos/cuenta bancaria/form pagar.html"
    form_class = CuentaBancariaIngresoPagarForm

    def get_success_url(self):
        if self.kwargs['opcion']==1:
            return reverse_lazy('cobranza_app:cuenta_bancaria_depositos_tabla')
        else:
            return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                deuda = form.cleaned_data.get('deuda')
                monto = form.cleaned_data.get('monto')
                tipo_cambio = form.cleaned_data.get('tipo_cambio')
                content_type = ContentType.objects.get_for_model(Ingreso)
                id_registro = self.kwargs['id_ingreso']
                obj, created = Pago.objects.get_or_create(
                    deuda = deuda,
                    content_type = content_type,
                    id_registro = id_registro,
                )
                if created:
                    obj.monto = monto
                else:
                    obj.monto = obj.monto + monto
                obj.tipo_cambio = tipo_cambio
                registro_guardar(obj, self.request)
                obj.save()
                self.request.session['primero'] = False
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #Modificar con Select2 con búsqueda de 4 caracteres
        #********************************************
        kwargs = super().get_form_kwargs()
        ingreso = Ingreso.objects.get(id=self.kwargs['id_ingreso'])
        
        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio_ingreso = TipoCambio.objects.tipo_cambio_venta(ingreso.fecha)
        tipo_cambio = tipo_de_cambio(tipo_cambio_ingreso, tipo_cambio_hoy)
        kwargs['tipo_cambio'] = tipo_cambio
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        ingreso = Ingreso.objects.get(id=self.kwargs['id_ingreso'])
        context = super(CuentaBancariaIngresoPagarCreateView, self).get_context_data(**kwargs)
        context['accion'] = 'Pagar'
        context['titulo'] = 'Deuda'
        context['ingreso'] = ingreso
        return context
    

class CuentaBancariaIngresoPagarUpdateView(BSModalUpdateView):
    model = Pago
    template_name = "bancos/cuenta bancaria/form pagar.html"
    form_class = CuentaBancariaIngresoPagarForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        ingreso = Ingreso.objects.get(id=self.kwargs['id_ingreso'])
        lista_deudas = []
        for deuda in Deuda.objects.filter(sociedad=ingreso.cuenta_bancaria.sociedad):
            if deuda.saldo > 0:
                lista_deudas.append(deuda.id)
        lista_deudas.append(self.object.deuda.id)

        tipo_cambio_hoy = TipoCambio.objects.tipo_cambio_venta(date.today())
        tipo_cambio_ingreso = TipoCambio.objects.tipo_cambio_venta(ingreso.fecha)
        tipo_cambio = tipo_de_cambio(tipo_cambio_ingreso, tipo_cambio_hoy)
        kwargs['tipo_cambio'] = tipo_cambio
        kwargs['lista_deudas'] = lista_deudas
        return kwargs

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        ingreso = Ingreso.objects.get(id=self.kwargs['id_ingreso'])
        context = super(CuentaBancariaIngresoPagarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Pago'
        context['ingreso'] = ingreso
        return context


class CuentaBancariaIngresoPagarDeleteView(BSModalDeleteView):
    model = Pago
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaIngresoPagarDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Pago'
        context['item'] = self.get_object()
        return context
    

class CuentaBancariaIngresoView(BSModalCreateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaIngresoForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            cuenta_bancaria = CuentaBancariaSociedad.objects.get(id=self.kwargs['id_cuenta_bancaria'])
            form.instance.cuenta_bancaria = cuenta_bancaria
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaIngresoView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaEfectivoIngresoView(BSModalCreateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaEfectivoIngresoForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            cuenta_bancaria = CuentaBancariaSociedad.objects.get(id=self.kwargs['id_cuenta_bancaria'])
            form.instance.cuenta_bancaria = cuenta_bancaria
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaEfectivoIngresoView, self).get_context_data(**kwargs)
        context['accion'] = 'Agregar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaIngresoCambiarUpdateView(BSModalUpdateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaIngresoCambiarForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaIngresoCambiarUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaIngresoUpdateView(BSModalUpdateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaIngresoForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaIngresoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaEfectivoIngresoUpdateView(BSModalUpdateView):
    model = Ingreso
    template_name = "includes/formulario generico.html"
    form_class = CuentaBancariaEfectivoIngresoForm

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def form_valid(self, form):
        if self.request.session['primero']:
            registro_guardar(form.instance, self.request)
            self.request.session['primero'] = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaEfectivoIngresoUpdateView, self).get_context_data(**kwargs)
        context['accion'] = 'Actualizar'
        context['titulo'] = 'Ingreso'
        return context
    

class CuentaBancariaIngresoDeleteView(BSModalDeleteView):
    model = Ingreso
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaIngresoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Ingreso'
        context['item'] = self.get_object()
        return context


class CuentaBancariaIngresoVerVoucherView(BSModalReadView):
    model = Ingreso
    template_name = "bancos/cuenta bancaria/ver voucher.html"
    context_object_name = 'cuenta_bancaria'

    def get_context_data(self, **kwargs):
        context = super(CuentaBancariaIngresoVerVoucherView, self).get_context_data(**kwargs)
        context['titulo'] = 'Ver Voucher'
        return context
    

class CuentaBancariaIngresoCancelarView(BSModalDeleteView):
    model = Deuda
    template_name = "includes/form generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_detalle', kwargs={'pk':self.kwargs['id_cuenta_bancaria']})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                deuda = self.get_object()
                fecha = date.today()
                monto = deuda.saldo
                moneda = deuda.moneda
                tipo_cambio = deuda.tipo_cambio
                Redondeo.objects.create(
                    deuda=deuda,
                    fecha=fecha,
                    monto=monto,
                    moneda=moneda,
                    tipo_cambio=tipo_cambio,
                    created_by=self.request.user,
                    updated_by=self.request.user,
                )
                self.request.session['primero'] = False
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(CuentaBancariaIngresoCancelarView, self).get_context_data(**kwargs)
        context['accion'] = 'Cancelar'
        context['titulo'] = 'Deuda'
        context['texto'] = '¿Está seguro de Cancelar la deuda?'
        context['item'] = self.get_object()
        return context


class RedondeoDeleteView(BSModalDeleteView):
    model = Redondeo
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:deudores_detalle', kwargs={'id_cliente':self.kwargs['id_cliente']})

    def get_context_data(self, **kwargs):
        context = super(RedondeoDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Redondeo'
        context['item'] = self.get_object()
        return context


class DepositosView(FormView):
    template_name = "bancos/cuenta bancaria/depositos.html"
    form_class = DepositosBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(DepositosView, self).get_form_kwargs()
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        kwargs['filtro_monto'] = self.request.GET.get('monto')
        kwargs['filtro_moneda'] = self.request.GET.get('moneda')
        kwargs['filtro_cuenta_bancaria'] = self.request.GET.get('cuenta_bancaria')
        kwargs['filtro_numero_operacion'] = self.request.GET.get('numero_operacion')
        kwargs['filtro_comentario'] = self.request.GET.get('comentario')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(DepositosView, self).get_context_data(**kwargs)
        ingresos = Ingreso.objects.all()
        filtro_fecha = self.request.GET.get('fecha')
        filtro_monto = self.request.GET.get('monto')
        filtro_moneda = self.request.GET.get('moneda')
        filtro_cuenta_bancaria = self.request.GET.get('cuenta_bancaria')
        filtro_numero_operacion = self.request.GET.get('numero_operacion')
        filtro_comentario = self.request.GET.get('comentario')
        if filtro_fecha:
            condicion = Q(fecha = filtro_fecha)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?fecha=" + filtro_fecha
        if filtro_monto:
            condicion = Q(monto = filtro_monto)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?monto=" + filtro_monto
        if filtro_moneda:
            condicion = Q(cuenta_bancaria__moneda = filtro_moneda)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?moneda=" + filtro_moneda
        if filtro_cuenta_bancaria:
            condicion = Q(cuenta_bancaria = filtro_cuenta_bancaria)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?cuenta_bancaria=" + filtro_cuenta_bancaria
        if filtro_numero_operacion:
            condicion = Q(numero_operacion__unaccent__icontains = filtro_numero_operacion.split(" ")[0])
            for palabra in filtro_numero_operacion.split(" ")[1:]:
                condicion &= Q(numero_operacion__unaccent__icontains = palabra)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?numero_operacion=" + filtro_numero_operacion
        if filtro_comentario:
            condicion = Q(comentario__unaccent__icontains = filtro_comentario.split(" ")[0])
            for palabra in filtro_comentario.split(" ")[1:]:
                condicion &= Q(comentario__unaccent__icontains = palabra)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?comentario=" + filtro_comentario

        objectsxpage =  10 # Show 10 objects per page.

        if len(ingresos) > objectsxpage:
            paginator = Paginator(ingresos, objectsxpage)
            page_number = self.request.GET.get('page')
            ingresos = paginator.get_page(page_number)

        context['movimientos'] = ingresos
        context['contexto_pagina'] = ingresos
        return context


def DepositosTabla(request):
    data = dict()
    if request.method == 'GET':
        template = "bancos/cuenta bancaria/depositos tabla.html"
        context = {}
        ingresos = Ingreso.objects.all()
        filtro_fecha = request.GET.get('fecha')
        filtro_monto = request.GET.get('monto')
        filtro_moneda = request.GET.get('moneda')
        filtro_cuenta_bancaria = request.GET.get('cuenta_bancaria')
        filtro_numero_operacion = request.GET.get('numero_operacion')
        filtro_comentario = request.GET.get('comentario')
        if filtro_fecha:
            condicion = Q(fecha = filtro_fecha)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?fecha=" + filtro_fecha
        if filtro_monto:
            condicion = Q(monto = filtro_monto)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?monto=" + filtro_monto
        if filtro_moneda:
            condicion = Q(cuenta_bancaria__moneda = filtro_moneda)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?moneda=" + filtro_moneda
        if filtro_cuenta_bancaria:
            condicion = Q(cuenta_bancaria = filtro_cuenta_bancaria)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?cuenta_bancaria=" + filtro_cuenta_bancaria
        if filtro_numero_operacion:
            condicion = Q(numero_operacion__unaccent__icontains = filtro_numero_operacion.split(" ")[0])
            for palabra in filtro_numero_operacion.split(" ")[1:]:
                condicion &= Q(numero_operacion__unaccent__icontains = palabra)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?numero_operacion=" + filtro_numero_operacion
        if filtro_comentario:
            condicion = Q(comentario__unaccent__icontains = filtro_comentario.split(" ")[0])
            for palabra in filtro_comentario.split(" ")[1:]:
                condicion &= Q(comentario__unaccent__icontains = palabra)
            ingresos = ingresos.filter(condicion)
            context['contexto_filtro'] = "?comentario=" + filtro_comentario

        objectsxpage =  10 # Show 10 objects per page.

        if len(ingresos) > objectsxpage:
            paginator = Paginator(ingresos, objectsxpage)
            page_number = request.GET.get('page')
            ingresos = paginator.get_page(page_number)

        context['movimientos'] = ingresos
        context['contexto_pagina'] = ingresos

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class DepositosPagarDeleteView(BSModalDeleteView):
    model = Pago
    template_name = "includes/eliminar generico.html"

    def get_success_url(self):
        return reverse_lazy('cobranza_app:cuenta_bancaria_depositos_inicio')

    def get_context_data(self, **kwargs):
        context = super(DepositosPagarDeleteView, self).get_context_data(**kwargs)
        context['accion'] = 'Eliminar'
        context['titulo'] = 'Pago'
        context['item'] = self.get_object()
        return context