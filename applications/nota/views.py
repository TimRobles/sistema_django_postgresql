from applications.importaciones import *
from django.core.paginator import Paginator
from applications.nota.forms import NotaCreditoBuscarForm
from applications.nota.models import NotaCredito, NotaCreditoDetalle
from applications.funciones import numeroXn, registrar_excepcion


class NotaCreditoView(FormView):
    template_name = "notas/nota_credito/inicio.html"
    form_class = NotaCreditoBuscarForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        kwargs['filtro_numero_nota'] = self.request.GET.get('numero_nota')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_fecha'] = self.request.GET.get('fecha')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoView, self).get_context_data(**kwargs)
        notas_credito = NotaCredito.objects.all()

        filtro_cliente = self.request.GET.get('cliente')
        filtro_numero_nota = self.request.GET.get('numero_nota')
        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_fecha = self.request.GET.get('fecha')

        contexto_filtro = []

        if filtro_cliente:
            condicion = Q(cliente__razon_social__unaccent__icontains = filtro_cliente.split(" ")[0])
            for palabra in filtro_cliente.split(" ")[1:]:
                condicion &= Q(cliente__razon_social__unaccent__icontains = palabra)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("cliente=" + filtro_cliente)

        if filtro_numero_nota:
            condicion = Q(numero_nota__icontains = filtro_numero_nota)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("numero_nota=" + filtro_cliente)

        if filtro_fecha:
            condicion = Q(fecha_cotizacion = datetime.strptime(filtro_fecha, "%Y-%m-%d").date())
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("fecha=" + filtro_fecha)

        if filtro_sociedad:
            condicion = Q(sociedad__id = filtro_sociedad)
            notas_credito = notas_credito.filter(condicion)
            contexto_filtro.append("sociedad=" + filtro_sociedad)

        context['contexto_filtro'] = "&".join(contexto_filtro)

        context['pagina_filtro'] = ""
        if self.request.GET.get('page'):
            if context['contexto_filtro']:
                context['pagina_filtro'] = f'&page={self.request.GET.get("page")}'
            else:
                context['pagina_filtro'] = f'page={self.request.GET.get("page")}'
        context['contexto_filtro'] = '?' + context['contexto_filtro']

        objectsxpage =  10 # Show 10 objects per page.

        if len(notas_credito) > objectsxpage:
            paginator = Paginator(notas_credito, objectsxpage)
            page_number = self.request.GET.get('page')
            notas_credito = paginator.get_page(page_number)
   
        context['contexto_pagina'] = notas_credito
        context['contexto_nota_credito'] = notas_credito
        
        return context 

class NotaCreditoDetailView(DetailView):
    model = NotaCredito
    template_name = "notas/nota_credito/detalle.html"
    context_object_name = 'contexto_nota_credito'

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoDetailView, self).get_context_data(**kwargs)
        context['materiales'] = NotaCredito.objects.ver_detalle(self.get_object().id)
        return context
    


def NotaCreditoDetailTabla(request, id):
    data = dict()
    if request.method == 'GET':
        template = 'notas/nota_credito/detalle_tabla.html'
        context = {}
        nota_credito = NotaCredito.objects.get(id = id)
        context['contexto_nota_credito'] = nota_credito
        # context['materiales'] = NotaCreditoDetalle.objects.ver_detalle(id)


        data['table'] = render_to_string(
            template,
            context,
            request=request
        )
        return JsonResponse(data)
