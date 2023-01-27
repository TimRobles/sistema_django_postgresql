from applications.logistica import models

def buscar_solicitud_prestamo_materiales(id_nota_salida):
    print("buscar_solicitud_prestamo_materiales")
    return models.NotaSalida.objects.solicitud_prestamo_materiales(id_nota_salida)

    #REFERENCIA CIRCULAR