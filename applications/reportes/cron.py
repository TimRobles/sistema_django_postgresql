import json
from datetime import datetime
def funcion_iterativa():
    with open("/home/tim/Documents/github/sistema_django_postgresql/applications/reportes/diccionario.json", "r") as infile:
        diccionario = json.load(infile)
        ahora = f"{datetime.now()}"
        diccionario[len(diccionario)+1] = ahora
        with open("/home/tim/Documents/github/sistema_django_postgresql/applications/reportes/diccionario.json", "w") as outfile:
            json.dump(diccionario, outfile, indent=4)