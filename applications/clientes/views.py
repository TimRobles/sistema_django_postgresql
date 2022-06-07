from django.shortcuts import render
from applications.importaciones import *
from .forms import (
    ClienteForm,
    CorreoClienteDarBajaForm,
    CorreoClienteForm, 
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
    CorreoCliente,
    InterlocutorCliente,
    ClienteInterlocutor,
    RepresentanteLegalCliente,
    TelefonoInterlocutorCliente,
    CorreoInterlocutorCliente,
    )

class ClienteListView(PermissionRequiredMixin, ListView):
    permission_required = ('clientes.view_cliente')

    model = Cliente
    template_name = "clientes/cliente/inicio.html"
    context_object_name = 'contexto_clientes'

def ClienteTabla(request):
    data = dict()
    if request.method == 'GET':
        template = 'clientes/cliente/inicio_tabla.html'
        context = {}
        context['contexto_clientes'] = Cliente.objects.all()

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

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context['accion']="Registrar"
        context['titulo']="Cliente"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class ClienteUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = ('clientes.change_cliente')

    model = Cliente
    template_name = "clientes/cliente/form.html"
    form_class = ClienteForm
    success_url = reverse_lazy('clientes_app:cliente_inicio')

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Cliente"
        return context

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        registro_guardar(form.instance, self.request)
        
        return super().form_valid(form)

class ClienteDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_cliente')

    model = Cliente
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy('clientes_app:cliente_inicio')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_sunat = 7
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado_sunat = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
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
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.kwargs['cliente_id']})

    def form_valid(self, form):
        tipo_documento = form.cleaned_data['tipo_documento']
        numero_documento = form.cleaned_data['numero_documento']
        nombre_completo = form.cleaned_data['nombre_completo']
        tipo_interlocutor = form.cleaned_data['tipo_interlocutor']
        cliente = Cliente.objects.get(id = self.kwargs['cliente_id'])

        interlocutor, existe = InterlocutorCliente.objects.get_or_create(
            tipo_documento = tipo_documento,
            numero_documento = numero_documento,
            nombre_completo = nombre_completo,
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('home_app:home')

    def get_context_data(self, **kwargs):
        context = super(InterlocutorClienteUpdateView, self).get_context_data(**kwargs)
        context['accion']="Actualizar"
        context['titulo']="Interlocutor"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        cliente_interlocutor = form.instance.ClienteInterlocutor_interlocutor.all()[0]
        cliente_interlocutor.tipo_interlocutor = form.cleaned_data['tipo_interlocutor']
        cliente_interlocutor.save()
        registro_guardar(form.instance, self.request)

        return super().form_valid(form)

class InterlocutorClienteDarBajaView(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = ('clientes.change_clienteinterlocutor')

    model = ClienteInterlocutor
    template_name = "includes/eliminar generico.html"
    success_url = reverse_lazy()

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 2
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_BAJA)
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 1
        registro_guardar(self.object, self.request)
        self.object.save()
        messages.success(request, MENSAJE_DAR_ALTA)
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

class CorreoClienteCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = ('clientes.add_correocliente')

    model = CorreoCliente
    template_name = "includes/formulario generico.html"
    form_class = CorreoClienteForm
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.kwargs['cliente_id']})

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

    def get_success_url(self, **kwargs):
        return reverse_lazy('clientes_app:cliente_detalle', kwargs={'pk':self.object.cliente.id})

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

    def form_valid(self, form):
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