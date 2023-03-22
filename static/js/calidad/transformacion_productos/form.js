function cambiar_sede(id_sede) {
    almacen = $('#id_almacen')[0]
    url_sede = $('#url_sede')[0].innerHTML + id_sede;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url_sede);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            almacen.innerHTML = $respuesta['info'];
        }else{
            $almacen.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_sede').unbind().on('change', function (e) {
    if (e.target.value) {
        cambiar_sede(e.target.value);
    } else {
        $('#id_almacen')[0].innerHTML = '<option value="" selected="">---------</option>';
    }
})



function ver_stock() {
    material = $('#id_material')[0].value;
    almacen = $('#id_almacen')[0].value;
    stock = $('#id_stock')[0].value;
    if (material && almacen_origen) {
        sociedad = $('#sociedad')[0].innerHTML;
        url_stock = $('#url_stock')[0].innerHTML + material + '/' + sociedad + '/' + almacen + '/';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url_stock);
        xhr.onload = function(){
            if (this.status === 200) {
                $respuesta = xhr.responseText;
            }else{
                $respuesta = '0.00';
            }
            stock.value = $respuesta;
        }
        xhr.send();
    }
}

function ver_stock_tipo_stock() {
    material = $('#id_material')[0].value;
    almacen = $('#id_almacen')[0].value;
    tipo_stock = $('#id_tipo_stock')[0].value;
    if (!tipo_stock) {
        ver_stock();
    } else {
        stock = $('#id_stock')[0];
        if (material && almacen) {
            sociedad = $('#sociedad')[0].innerHTML;
            url_stock_tipo_stock = $('#url_stock')[0].innerHTML + 'tipo_stock/' + material + '/' + sociedad + '/' + almacen + '/' + tipo_stock + '/';
            console.log(url_stock_tipo_stock)
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url_stock_tipo_stock);
            xhr.onload = function(){
                if (this.status === 200) {
                    $respuesta = xhr.responseText;
                }else{
                    $respuesta = '0.00';
                }
                console.log($respuesta);
                stock.value = $respuesta;
            }
            xhr.send();
        }
    }
}


$('#id_material').unbind().on('change', function () {
    ver_stock_tipo_stock();
})

$('#id_almacen').unbind().on('change', function () {
    ver_stock_tipo_stock();
})

$('#id_tipo_stock').unbind().on('change', function () {
    ver_stock_tipo_stock();
})

ver_stock_tipo_stock();