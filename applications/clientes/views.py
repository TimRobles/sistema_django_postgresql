from django.core.paginator import Paginator
from django.shortcuts import render
from applications.datos_globales.models import Distrito
from applications.funciones import registrar_excepcion
from applications.importaciones import *
from .forms import (
    ClienteAnexoDarBajaForm,
    ClienteAnexoForm,
    ClienteBuscarForm,
    ClienteForm,
    ClienteInterlocutorCreateForm,
    ClienteInterlocutorUpdateForm,
    CorreoClienteDarBajaForm,
    CorreoClienteForm,
    InterlocutorBuscarForm, 
    InterlocutorClienteForm,
    InterlocutorClienteUpdateForm,
    RepresentanteLegalClienteDarBajaForm,
    RepresentanteLegalClienteForm,
    TelefonoInterlocutorForm,
    TelefonoInterlocutorDarBajaForm,
    CorreoInterlocutorForm,
    CorreoInterlocutorDarBajaForm,
    )
from .models import (
    Cliente,
    ClienteAnexo,
    CorreoCliente,
    InterlocutorCliente,
    ClienteInterlocutor,
    RepresentanteLegalCliente,
    TelefonoInterlocutorCliente,
    CorreoInterlocutorCliente,
    )

class ClienteListView(PermissionRequiredMixin, FormView):
    permission_required = ('clientes.view_cliente')
    template_name = "clientes/cliente/inicio.html"
    form_class = ClienteBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ClienteListView, self).get_form_kwargs()
        kwargs['filtro_razon_social'] = self.request.GET.get('razon_social')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClienteListView,self).get_context_data(**kwargs)
        clientes = Cliente.objects.all()
        
        filtro_razon_social = self.request.GET.get('razon_social')
        
        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            clientes = clientes.filter(condicion)
            contexto_filtro.append(f"razon_social={filtro_razon_social}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(clientes) > objectsxpage:
            paginator = Paginator(clientes, objectsxpage)
            page_number = self.request.GET.get('page')
            clientes = paginator.get_page(page_number)
   
        context['contexto_pagina'] = clientes
        return context

def ClienteTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'clientes/cliente/inicio_tabla.html'
        context = {}
        clientes = Cliente.objects.all()

        filtro_razon_social = request.GET.get('razon_social')

        contexto_filtro = []

        if filtro_razon_social:
            condicion = Q(razon_social__unaccent__icontains = filtro_razon_social.split(" ")[0])
            for palabra in filtro_razon_social.split(" ")[1:]:
                condicion &= Q(razon_social__unaccent__icontains = palabra)
            clientes = clientes.filter(condicion)
            contexto_filtro.append(f"razon_social={filtro_razon_social}")

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(clientes) > objectsxpage:
            paginator = Paginator(clientes, objectsxpage)
            page_number = request.GET.get('page')
            clientes = paginator.get_page(page_number)
   
        context['contexto_pagina'] = clientes

        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class ClienteCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('clientes.add_cliente')
    model = Cliente
    template_name = "clientes/cliente/form.html"
    form_class = ClienteForm
    success_url = reverse_lazy('clientes_app:cliente_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Cliente"
        return context


class ClienteUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_cliente')
    model = Cliente
    template_name = "clientes/cliente/form.html"
    form_class = ClienteForm
    success_url = reverse_lazy('clientes_app:cliente_inicio')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cliente"
        return context


class ClienteDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_cliente')
    model = Cliente
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('clientes_app:cliente_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_sunat = 7
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ClienteDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Cliente"
        context['dar_baja'] = "true"
        context['item'] = self.object.razon_social
        return context

class ClienteDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_cliente')
    model = Cliente
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('clientes_app:cliente_inicio')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado_sunat = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ClienteDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Cliente"
        context['dar_baja'] = "true"
        context['item'] = self.object.razon_social
        return context

class ClienteDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('clientes.view_clienteinterlocutor')

    model = Cliente
    template_name = "clientes/cliente/detalle.html"
    context_object_name = 'contexto_clientes'

    def get_context_data(self, **kwargs):
        cliente = Cliente.objects.get(id = self.kwargs['pk'])
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['interlocutores'] = ClienteInterlocutor.objects.filter(cliente = cliente)
        context['correos'] = CorreoCliente.objects.filter(cliente = cliente)
        context['representantes_legales'] = RepresentanteLegalCliente.objects.filter(cliente = cliente)
        context['anexos'] = cliente.ClienteAnexo_cliente.all()
        return context

def ClienteDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'clientes/cliente/detalle_tabla.html'
        context = {}
        cliente = Cliente.objects.get(id = pk)
        context['contexto_clientes'] = cliente
        context['interlocutores'] = ClienteInterlocutor.objects.filter(cliente = cliente)
        context['correos'] = CorreoCliente.objects.filter(cliente = cliente)
        context['representantes_legales'] = RepresentanteLegalCliente.objects.filter(cliente = cliente)
        context['anexos'] = cliente.ClienteAnexo_cliente.all()
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)

class InterlocutorClienteCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('clientes.add_interlocutorcliente')
    template_name = "clientes/interlocutor/form.html"
    form_class = InterlocutorClienteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.kwargs['cliente_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            tipo_documento = form.cleaned_data['tipo_documento']
            numero_documento = form.cleaned_data['numero_documento']
            nombre_completo = form.cleaned_data['nombre_completo']
            tipo_interlocutor = form.cleaned_data['tipo_interlocutor']
            cliente = Cliente.objects.get(id = self.kwargs['cliente_id'])

            interlocutor, existe = InterlocutorCliente.objects.get_or_create(
                tipo_documento = tipo_documento,
                numero_documento = numero_documento,
                nombre_completo = nombre_completo.upper(),
            )
            if not existe:
                interlocutor.created_by = self.request.user
                interlocutor.updated_by = self.request.user
                interlocutor.save()

            relacion, existe = ClienteInterlocutor.objects.get_or_create(
                tipo_interlocutor = tipo_interlocutor,
                interlocutor = interlocutor,
                cliente = cliente,
            )

            if not existe:
                relacion.created_by = self.request.user
                relacion.updated_by = self.request.user
                relacion.save()

            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url()) 

    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Interlocutor Cliente"
        return context

class InterlocutorClienteUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_interlocutorcliente')
    model = InterlocutorCliente
    template_name = "clientes/interlocutor/form.html"
    form_class = InterlocutorClienteUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('home_app:home')
    
    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.instance.usuario = self.request.user
            cliente_interlocutor = form.instance.ClienteInterlocutor_interlocutor.all()[0]
            cliente_interlocutor.tipo_interlocutor = form.cleaned_data['tipo_interlocutor']
            cliente_interlocutor.save()
            registro_guardar(form.instance, self.request)

            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Interlocutor"
        return context

class InterlocutorClienteDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_clienteinterlocutor')
    model = ClienteInterlocutor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy()
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 2
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_BAJA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteDarBajaView, self).get_context_data(**kwargs)
        context['accion'] = "Dar Baja"
        context['titulo'] = "Interlocutor"
        context['dar_baja'] = "true"
        context['item'] = self.object.interlocutor
        return context

class InterlocutorClienteDarAltaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_clienteinterlocutor')
    model = ClienteInterlocutor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy()
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            self.object.estado = 1
            registro_guardar(self.object, self.request)
            self.object.save()
            messages.success(request, MENSAJE_DAR_ALTA)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteDarAltaView, self).get_context_data(**kwargs)
        context['accion']="Dar Alta"
        context['titulo'] = "Interlocutor"
        context['dar_baja'] = "true"
        context['item'] = self.object.interlocutor
        return context

class InterlocutorClienteDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('clientes.view_interlocutorcliente')
    model = InterlocutorCliente
    template_name = "clientes/interlocutor/detalle.html"
    context_object_name = 'contexto_interlocutores'

    def get_context_data(self, **kwargs):
        interlocutor = InterlocutorCliente.objects.get(id = self.kwargs['pk'])
        context = super(InterlocutorClienteDetailView, self).get_context_data(**kwargs)
        context['telefonos'] = TelefonoInterlocutorCliente.objects.filter(interlocutor = interlocutor)
        context['correos'] = CorreoInterlocutorCliente.objects.filter(interlocutor = interlocutor)
        return context

def InterlocutorClienteDetailTabla(request, pk):
    data = dict()
    if request.method == 'GET':
        template = 'clientes/interlocutor/detalle_tabla.html'
        context = {}
        interlocutor = InterlocutorCliente.objects.get(id = pk)
        context['contexto_interlocutores'] = interlocutor
        context['telefonos'] = TelefonoInterlocutorCliente.objects.filter(interlocutor = interlocutor)
        context['correos'] = CorreoInterlocutorCliente.objects.filter(interlocutor = interlocutor)
        
        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)


class InterlocutorClienteDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.delete_interlocutorcliente')
    model = InterlocutorCliente
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_lista')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            self.object = self.get_object()
            for telefono in self.object.TelefonoInterlocutorCliente_interlocutor.all():
                telefono.delete()
            for correo in self.object.CorreoInterlocutorCliente_interlocutor.all():
                correo.delete()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Interlocutor"
        context['item'] = self.get_object()
        return context


class InterlocutorClienteListaView(PermissionRequiredMixin, FormView):
    permission_required = ('clientes.view_interlocutorcliente')
    template_name = "clientes/interlocutor/inicio.html"
    form_class = InterlocutorBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(InterlocutorClienteListaView, self).get_form_kwargs()
        kwargs['filtro_tipo_documento'] = self.request.GET.get('tipo_documento')
        kwargs['filtro_numero_documento'] = self.request.GET.get('numero_documento')
        kwargs['filtro_nombre_completo'] = self.request.GET.get('nombre_completo')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteListaView, self).get_context_data(**kwargs)
        interlocutores = InterlocutorCliente.objects.all()

        filtro_tipo_documento = self.request.GET.get('tipo_documento')
        filtro_numero_documento = self.request.GET.get('numero_documento')
        filtro_nombre_completo = self.request.GET.get('nombre_completo')
        
        contexto_filtro = []

        if filtro_tipo_documento:
            condicion = Q(tipo_documento = filtro_tipo_documento)
            interlocutores = interlocutores.filter(condicion)
            contexto_filtro.append("tipo_documento=" + filtro_tipo_documento)

        if filtro_numero_documento:
            condicion = Q(numero_documento = filtro_numero_documento)
            interlocutores = interlocutores.filter(condicion)
            contexto_filtro.append("numero_documento=" + filtro_numero_documento)

        if filtro_nombre_completo:
            condicion = Q(nombre_completo__unaccent__icontains = filtro_nombre_completo.split(" ")[0])
            for palabra in filtro_nombre_completo.split(" ")[1:]:
                condicion &= Q(nombre_completo__unaccent__icontains = palabra)
            interlocutores = interlocutores.filter(condicion)
            contexto_filtro.append("nombre_completo=" + filtro_nombre_completo)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  15 # Show 10 objects per page.

        if len(interlocutores) > objectsxpage:
            paginator = Paginator(interlocutores, objectsxpage)
            page_number = self.request.GET.get('page')
            interlocutores = paginator.get_page(page_number)
   
        context['contexto_pagina'] = interlocutores
        context['interlocutores'] = interlocutores
        return context


class ClienteInterlocutorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_clienteinterlocutor')
    model = ClienteInterlocutor
    template_name = "includes/formulario generico.html"
    form_class = ClienteInterlocutorUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('home_app:home')
    
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
        context = super(ClienteInterlocutorUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Tipo de Interlocutor"
        return context


class ClienteInterlocutorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('clientes.add_clienteinterlocutor')
    model = ClienteInterlocutor
    template_name = "clientes/interlocutor/form agregar relacion.html"
    form_class = ClienteInterlocutorCreateForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('home_app:home')
    
    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            interlocutor_cliente = InterlocutorCliente.objects.get(id=self.kwargs['interlocutor_cliente_id'])
            form.instance.interlocutor = interlocutor_cliente
            registro_guardar(form.instance, self.request)
            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ClienteInterlocutorCreateView, self).get_context_data(**kwargs)
        context['accion'] = "Agregar"
        context['titulo'] = "Relación"
        return context


class ClienteInterlocutorDeleteView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.delete_clienteinterlocutor')
    model = ClienteInterlocutor
    template_name = "includes/eliminar generico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.kwargs['interlocutor_cliente_id']})
    
    def get_context_data(self, **kwargs):
        context = super(ClienteInterlocutorDeleteView, self).get_context_data(**kwargs)
        context['accion'] = "Eliminar"
        context['titulo'] = "Relación"
        context['item'] = self.get_object()
        return context


class CorreoClienteCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('clientes.add_correocliente')

    model = CorreoCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoClienteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.kwargs['cliente_id']})

    def get_form_kwargs(self, *args, **kwargs):
        correos = CorreoCliente.objects.filter(cliente__id = self.kwargs['cliente_id'], estado = 1)
        lista_correos = []
        for correo in correos:
            lista_correos.append(correo.id)
        kwargs = super(CorreoClienteCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['correos'] = CorreoCliente.objects.filter(id__in = lista_correos)
        kwargs['cliente_id'] = self.kwargs['cliente_id']
        return kwargs

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(id = self.kwargs['cliente_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CorreoClienteCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Correo"
        return context

class CorreoClienteUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_correocliente')
    model = CorreoCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoClienteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    def get_form_kwargs(self, *args, **kwargs):
        correos = CorreoCliente.objects.filter(cliente__id = self.object.cliente.id, estado = 1)
        lista_correos = []
        for correo in correos:
            lista_correos.append(correo.id)
        kwargs = super(CorreoClienteUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['correos'] = lista_correos
        kwargs['cliente_id'] = self.object.cliente.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CorreoClienteUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Correo"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class CorreoClienteDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_correocliente')
    model = CorreoCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoClienteDarBajaForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CorreoClienteDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Correo"
        return context

class TelefonoInterlocutorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('clientes.add_telefonointerlocutorcliente')
    model = TelefonoInterlocutorCliente
    template_name = "includes/formulario generico.html"
    form_class = TelefonoInterlocutorForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.kwargs['interlocutor_id']})

    def form_valid(self, form):
        form.instance.interlocutor = InterlocutorCliente.objects.get(id = self.kwargs['interlocutor_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TelefonoInterlocutorCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Teléfono"
        return context

class TelefonoInterlocutorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_telefonointerlocutorcliente')
    model = TelefonoInterlocutorCliente
    template_name = "includes/formulario generico.html"
    form_class = TelefonoInterlocutorForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def get_context_data(self, **kwargs):
        context = super(TelefonoInterlocutorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Teléfono"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class TelefonoInterlocutorDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_telefonointerlocutorcliente')
    model = TelefonoInterlocutorCliente
    template_name = "includes/formulario generico.html"
    form_class = TelefonoInterlocutorDarBajaForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TelefonoInterlocutorDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Teléfono"
        return context

class CorreoInterlocutorCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('clientes.add_correointerlocutorcliente')
    model = CorreoInterlocutorCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoInterlocutorForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.kwargs['interlocutor_id']})

    def form_valid(self, form):
        form.instance.interlocutor = InterlocutorCliente.objects.get(id = self.kwargs['interlocutor_id'])

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Correo"
        return context

class CorreoInterlocutorUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_correointerlocutorcliente')
    model = CorreoInterlocutorCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoInterlocutorForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Correo"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class CorreoInterlocutorDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_correointerlocutorcliente')
    model = CorreoInterlocutorCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoInterlocutorDarBajaForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:interlocutor_detalle', kwargs={'pk':self.object.interlocutor.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CorreoInterlocutorDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Correo"
        return context

class RepresentanteLegalClienteCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('clientes.add_interlocutorcliente')
    template_name = "clientes/interlocutor/form.html"
    form_class = RepresentanteLegalClienteForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.kwargs['cliente_id']})

    def get_form_kwargs(self, *args, **kwargs):
        interlocutores = ClienteInterlocutor.objects.filter(cliente__id = self.kwargs['cliente_id'], estado = 1)
        lista_interlocutores = []
        for interlocutor in interlocutores:
            lista_interlocutores.append(interlocutor.interlocutor.id)
        kwargs = super(RepresentanteLegalClienteCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['interlocutores'] = InterlocutorCliente.objects.filter(id__in = lista_interlocutores)
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            interlocutor = form.cleaned_data['interlocutor']
            tipo_representante_legal = form.cleaned_data['tipo_representante_legal']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            cliente = Cliente.objects.get(id = self.kwargs['cliente_id'])

            representante, existe = RepresentanteLegalCliente.objects.get_or_create(
                cliente = cliente,
                interlocutor = interlocutor,
                tipo_representante_legal = tipo_representante_legal,
                fecha_inicio = fecha_inicio,
            )
            if not existe:
                representante.created_by = self.request.user
                representante.updated_by = self.request.user
                representante.save()

            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(RepresentanteLegalClienteCreateView, self).get_context_data(**kwargs)
        context['accion']="Asignar"
        context['titulo']="Representante Legal Cliente"
        return context

class RepresentanteLegalClienteDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_correointerlocutorcliente')
    model = RepresentanteLegalCliente
    template_name = "includes/formulario generico.html"
    form_class = RepresentanteLegalClienteDarBajaForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RepresentanteLegalClienteDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Representante Legal"
        return context


class ClienteAnexoCreateView(PermissionRequiredMixin, BSModalFormView):
    permission_required = ('clientes.add_clienteanexo')
    template_name = "clientes/cliente/form anexo.html"
    form_class = ClienteAnexoForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.kwargs['cliente_id']})

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            if self.request.session['primero']:
                direccion = form.cleaned_data['direccion']
                ubigeo = form.cleaned_data['ubigeo']
                cliente = Cliente.objects.get(id = self.kwargs['cliente_id'])
                distrito = Distrito.objects.get(codigo=ubigeo.codigo)

                anexo = ClienteAnexo.objects.create(
                    cliente = cliente,
                    direccion = direccion,
                    distrito = distrito,
                    created_by = self.request.user,
                    updated_by = self.request.user,
                )
                self.request.session['primero'] = False

            return super().form_valid(form)
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            registrar_excepcion(self, ex, __file__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.request.session['primero'] = True
        context = super(ClienteAnexoCreateView, self).get_context_data(**kwargs)
        context['accion']="Crear"
        context['titulo']="Anexo"
        return context

class ClienteAnexoDarBajaView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_clienteanexo')
    model = ClienteAnexo
    template_name = "includes/formulario generico.html"
    form_class = ClienteAnexoDarBajaForm
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return render(request, 'includes/modal sin permiso.html')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    def form_valid(self, form):
        form.instance.estado = 2
        registro_guardar(form.instance, self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteAnexoDarBajaView, self).get_context_data(**kwargs)
        context['accion']="Dar Baja"
        context['titulo']="Anexo"
        return context