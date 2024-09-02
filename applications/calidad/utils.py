def actualizar_serie_almacen(serie):
    guardar = False
    if serie.almacen != serie.almacen_latest:
        serie.almacen = serie.almacen_latest
        guardar = True
    if serie.tipo_stock != serie.tipo_stock_latest:
        serie.tipo_stock = serie.tipo_stock_latest
        guardar = True
        
    if guardar:
        serie.save()