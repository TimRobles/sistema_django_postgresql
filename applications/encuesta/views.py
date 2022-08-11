from audioop import reverse
from applications.encuesta.forms import EncuestarForm, RespuestaClienteForm, RespuestaDetalleForm
from applications.encuesta.models import Alternativa, Encuesta, Pregunta, Respuesta, RespuestaDetalle
from applications.importaciones import *

# Create your views here.


class RespuestaListaView(ListView):
    model = Respuesta
    template_name = "encuesta/lista.html"
    context_object_name = 'respuestas'


class NuevaEncuestaView(ListView):
    model = Pregunta
    template_name = "encuesta/nuevo.html"
    context_object_name = 'preguntas'
    
    def get_context_data(self, **kwargs):
        context = super(NuevaEncuestaView, self).get_context_data(**kwargs)
        context['alternativas'] = Alternativa.objects.all()
        return context


class RespuestaClienteActualizar(UpdateView):
    template_name = "encuesta/encuesta cliente.html"
    model = Respuesta
    form_class = RespuestaClienteForm
    success_url = reverse_lazy('encuesta_app:respuesta_lista')

    def get_context_data(self, **kwargs):
        context = super(RespuestaClienteActualizar, self).get_context_data(**kwargs)
        context['accion'] = "Actualizar"
        context['titulo'] = "Encuestados"
        return context  

class RespuestaClienteCrear(CreateView):
    template_name = "encuesta/encuesta cliente.html"
    model = Respuesta
    form_class = RespuestaClienteForm
    success_url = reverse_lazy('encuesta_app:respuesta_lista')

    def get_context_data(self, **kwargs):
        context = super(RespuestaClienteCrear, self).get_context_data(**kwargs)
        context['accion'] = "Registrar"
        context['titulo'] = "Encuestados"
        return context  

def RespuestaDetalleCrear(request):
    if request.method=='POST':
        respuesta = request.POST.get('respuesta')
        pregunta = request.POST.get('pregunta')
        alternativa = request.POST.get('alternativa')
        texto = request.POST.get('texto')
        
        obj_respuesta = Respuesta.objects.get(id=respuesta)
        obj_pregunta = Pregunta.objects.get(id=pregunta)
        if alternativa != "":
            obj_alternativa = Alternativa.objects.get(id=alternativa)
        else:
            obj_alternativa = None
        print(obj_respuesta)
        print(obj_pregunta)
        print(obj_alternativa)

        print(respuesta, type(respuesta))
        print(pregunta, type(pregunta))
        print(alternativa, type(alternativa))
        print(texto, type(texto))
        RespuestaDetalle.objects.create(
            respuesta=obj_respuesta,
            pregunta=obj_pregunta,
            alternativa=obj_alternativa,
            texto=texto,
            created_by=request.user,
            updated_by=request.user,
        )
    if request.method=='GET':
        print('Hola desde GET')
        # Respuesta.objects.create(

        # )
    return HttpResponse('Hola desde View')




class Encuestar(FormView):
    template_name = "encuesta/encuestar.html"
    form_class = EncuestarForm
    success_url = reverse_lazy('encuesta_app:respuesta_lista')

    def form_valid(self, form):
        tipo_encuesta = form.cleaned_data['tipo_encuesta']
        return HttpResponseRedirect(
            reverse_lazy(
                'encuesta_app:encuestar_segunda_parte',
                kwargs={
                    'respuesta_id':self.kwargs['respuesta_id'],
                    'tipo_encuesta':tipo_encuesta.id,
                    }
                )
            )


class EncuestarSegundaParte(TemplateView):
    template_name = "encuesta/encuestar segunda parte.html"

    def get_context_data(self, **kwargs):
        encuesta = Encuesta.objects.get(id=self.kwargs['tipo_encuesta'])
        context = super(EncuestarSegundaParte, self).get_context_data(**kwargs)
        context['preguntas'] = Pregunta.objects.filter(encuesta=encuesta, mostrar=True)
        context['respuesta'] = self.kwargs['respuesta_id']
        context['url'] = reverse_lazy('encuesta_app:respuesta_detalle_crear')
        context['url2'] = reverse_lazy('encuesta_app:respuesta_lista')

        return context
    
    


class EncuestaDetalleVer(DetailView):
    
    model = Respuesta
    template_name = "encuesta/detalle.html"
    context_object_name = 'respuesta'

    def get_context_data(self, **kwargs):
        context = super(EncuestaDetalleVer, self).get_context_data(**kwargs)
        detalles = self.get_object().RespuestaDetalle_respuesta.all()
        preguntas = {}
        listaPreguntas=[]
        listaAlternativas=[]
        for detalle in detalles:
            pregunta = detalle.pregunta
            alternativa = detalle.alternativa
            texto = detalle.texto
            

            if pregunta in preguntas:
                preguntas[pregunta].append(alternativa)
            else:
                if texto != '':
                    preguntas[pregunta] = [texto,]
                else:
                    preguntas[pregunta] = [alternativa,]


        
        context['preguntas'] = preguntas

        return context

    


    