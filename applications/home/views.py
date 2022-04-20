from applications.funciones import consulta_dni, consulta_ruc
from applications.importaciones import *

class HomePage(TemplateView):
    template_name = "home/home.html"

def ConsultaRucView(request, ruc):
    data = dict()
    if request.method == 'GET':
        if len(ruc.__str__()) == 11:
            datos_empresa = consulta_ruc(ruc)
            informacion = simplejson.dumps({
                                'razon_social' : datos_empresa['nombre'],
                                'direccion' : datos_empresa['direccion'],
                                'ubigeo' : datos_empresa['ubigeo'],
                                'estado' : datos_empresa['estado'],
                                'condicion' : datos_empresa['condicion'],
                                'distrito' : datos_empresa['distrito'],
                                'provincia' : datos_empresa['provincia'],
                                'departamento' : datos_empresa['departamento'],
                            })
        else:
            datos_persona = consulta_dni(ruc)
            informacion = simplejson.dumps({
                                'razon_social' : datos_persona['cliente'],
                            })

        data['info'] = render_to_string(
            'includes/info.html',
            {
                'informacion': informacion,
            },
            request=request
        )
        return JsonResponse(data)
