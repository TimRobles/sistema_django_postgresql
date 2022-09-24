from decimal import Decimal


def convertir_moneda(tipo_cambio, moneda_destino, moneda_inicial):
    print("**********************************")
    print(moneda_inicial)
    print(moneda_inicial.principal)
    print(moneda_inicial.secundario)
    print(moneda_destino)
    print(moneda_destino.principal)
    print(moneda_destino.secundario)
    print("**********************************")
    if moneda_inicial == moneda_destino:
        return Decimal('1')
        
    return Decimal('0')