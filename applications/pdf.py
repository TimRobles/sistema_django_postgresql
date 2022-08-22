import os, io

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, Frame, PageTemplate, BaseDocTemplate, PageBreak, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import *
from functools import partial

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

rutaBase=os.getcwd()

fuentes = [
    'ComicNeue-Bold',
    'ComicNeue-BoldItalic',
    'ComicNeue-Italic',
    'ComicNeue-Light',
    'ComicNeue-LightItalic',
    'ComicNeue-Regular',
    'CourierPrime-Regular',
    'CourierPrime-Bold',
]
tamanoFuente = [6, 7, 8, 9, 10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20]

styleSheet = getSampleStyleSheet()
for fuente in fuentes:
    pdfmetrics.registerFont(TTFont(fuente, rutaBase + '/fonts/%s.ttf' % fuente))
    for i in tamanoFuente:
        styleSheet.add(ParagraphStyle(name=fuente + '-' + str(i), fontName=fuente, fontSize=i, leading=i+1))

def cmToPx(cm):
    return float(float(10)*float(cm)*float(A4[0])/float(210))

def parrafoIzquierda(texto, fuente, tamaño=8, tipo="Regular", color='black'):
    try:
        texto = texto.replace("\n", "<br/>")
    except:
        pass
    
    return Paragraph('''<para color=%s align=left>%s</para>''' % (color, texto), styleSheet[fuente + '-' + tipo + '-' + str(tamaño)])

def parrafoIzquierdaTabla(texto, tabla, fuente, tamaño=8, tipo="Regular", color='black'):
    try:
        texto = texto.replace("\n", "<br/>")
    except:
        pass
    
    return [Paragraph('''<para spaceAfter=10 color=%s align=left>%s</para>''' % (color, texto), styleSheet[fuente + '-' + tipo + '-' + str(tamaño)]), tabla]

def parrafoCentro(texto, fuente, tamaño=8, tipo="Regular", color='black'):
    try:
        texto = texto.replace("\n", "<br/>")
    except:
        pass
    
    return Paragraph('''<para color=%s align=center>%s</para>''' % (color, texto), styleSheet[fuente + '-' + tipo + '-' + str(tamaño)])

def parrafoDerecha(texto, fuente, tamaño=8, tipo="Regular", color='black'):
    try:
        texto = texto.replace("\n", "<br/>")
    except:
        pass
    
    return Paragraph('''<para color=%s align=right>%s</para>''' % (color, texto), styleSheet[fuente + '-' + tipo + '-' + str(tamaño)])

def parrafoJustificado(texto, fuente, tamaño=8, tipo="Regular", color='black'):
    try:
        texto = texto.replace("\n", "<br/>")
    except:
        pass
    
    return Paragraph('''<para color=%s align=justify>%s</para>''' % (color, texto), styleSheet[fuente + '-' + tipo + '-' + str(tamaño)])

def vacio(factor=1):
    return Spacer(10, factor*10)

def listaViñeta(texto, fuente, tamaño=8, tipo="Regular", color='black'):
    filas = texto.splitlines()
    lista = []
    for fila in filas:
        lista.append(ListItem(
            parrafoIzquierda(fila, fuente, tamaño, tipo, color),
            bulletColor='black',
            ))
    return ListFlowable(
        lista,
        bulletType='bullet',
        )

def listaNumero(texto, fuente, tamaño=8, tipo="Regular", color='black'):
    filas = texto.splitlines()
    lista = []
    for fila in filas:
        lista.append(
            ListItem(parrafoIzquierda(fila, fuente, tamaño, tipo, color),)
        )
    return ListFlowable(
        lista,
        )

def hipervinculo(ruta, texto):
    return '<a href="%s" color="blue"><u>%s</u></a>' % (ruta, texto)

def insertarImagen(ruta, ancho, alto):
    return '<img src="%s" width="%s" height="%s" valign="top"/>' % (ruta, str(cmToPx(ancho)), str(cmToPx(alto)))
    
def insertarImagenGrande(ruta, ancho=0, alto=0):
    I = Image(ruta)
    if ancho > 0 and alto > 0:
        I.drawHeight = cmToPx(alto)
        I.drawWidth = cmToPx(ancho)
    elif ancho > 0:
        maximo_alto = cmToPx(15)
        if cmToPx(ancho) * I.drawHeight / I.drawWidth > maximo_alto:
            ancho = 15 * I.drawWidth / I.drawHeight
        I.drawHeight = cmToPx(ancho) * I.drawHeight / I.drawWidth
        I.drawWidth = cmToPx(ancho)
    return I


def header_content(logo):
    if logo:
        cabecera = insertarImagen(logo, 5, 1)
        return parrafoCentro(cabecera, "CourierPrime", 7, "Regular")
    else:
        return parrafoCentro('', "CourierPrime", 7, "Regular")


def footer_content(texto):
    piedepagina = texto
    return parrafoCentro(piedepagina, "CourierPrime", 6, "Regular")


def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(cmToPx(19), cmToPx(1)) # width, topMargin
    content.drawOn(canvas, cmToPx(1), cmToPx(28.7)) #leftMargin, height
    canvas.restoreState()

def header_Lands(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(cmToPx(28.7), cmToPx(1)) # width, topMargin
    content.drawOn(canvas, cmToPx(1), cmToPx(20)) #leftMargin, height
    canvas.restoreState()

def footer(canvas, doc, texto):
    canvas.saveState()
    P = footer_content(texto)
    w, h = P.wrap(cmToPx(19), cmToPx(1))
    P.drawOn(canvas, cmToPx(1), cmToPx(1))
    canvas.restoreState()

def footer_Lands(canvas, doc, texto):
    canvas.saveState()
    P = footer_content(texto)
    w, h = P.wrap(cmToPx(28.7), cmToPx(1))
    P.drawOn(canvas, cmToPx(1), cmToPx(0.5))
    canvas.restoreState()

A4Portrait = Frame(cmToPx(1), cmToPx(2.5), cmToPx(19), cmToPx(24.7), id='normal') #leftMargin, bottomMargin, width, height
A4Landscape = Frame(cmToPx(1), cmToPx(2.45), cmToPx(27.65), cmToPx(17), id='normal') #leftMargin, bottomMargin, width, height

def generarPDF(titulo, elementos, orientacion_vertical=True, logo=rutaBase + '/logos/logo header.png', texto='Probando Pie de página'):
    # container for the 'Flowable' objects

    buf = io.BytesIO()

    if orientacion_vertical:
        print('************')
        print(logo)
        print('************')
        frame = A4Portrait
        template = PageTemplate(id='test', frames=frame, onPage=partial(header, content=header_content(logo)), onPageEnd=partial(footer, texto=texto))
        doc = BaseDocTemplate(buf, title=titulo, pagesize=A4, pageTemplates=[template], showBoundary=0, leftMargin=cmToPx(0.3), rightMargin=cmToPx(0.3), topMargin=cmToPx(0.3), bottomMargin=cmToPx(0.3))
    else:
        frame = A4Landscape
        template = PageTemplate(id='test', frames=frame, onPage=partial(header_Lands, content=header_content(logo)), onPageEnd=partial(footer_Lands, texto=texto))
        doc = BaseDocTemplate(buf, title=titulo, pagesize=(A4[1],A4[0]), pageTemplates=[template], showBoundary=0, leftMargin=cmToPx(0.3), rightMargin=cmToPx(0.3), topMargin=cmToPx(0.3), bottomMargin=cmToPx(0.3))

    # write the document to disk
    doc.build(elementos)
    buf.seek(0)
    return buf

#############################################################

def generarElemento(texto, data):
    elementos = []
    for fuente in fuentes:
        for i in tamanoFuente:
            text = parrafoIzquierda(texto, fuente.split('-')[0], i, fuente.split('-')[1])
            elementos.append(text)
        elementos.append(parrafoCentro("-", fuente.split('-')[0], 8, fuente.split('-')[1]))

    t=Table(data, style=[('GRID',(0,0),(-1,-1),1,colors.black),
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    elementos.append(t)
    return elementos