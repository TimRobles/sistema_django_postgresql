function ver_stock() {
    material = $('#id_material')[0].value;
    almacen_origen = $('#id_almacen')[0].value;
    stock_disponible = $('#id_stock_disponible')[0];
    if (material && almacen_origen) {
        sociedad = $('#sociedad')[0].innerHTML;
        url_stock = $('#url_stock')[0].innerHTML + material + '/' + sociedad + '/' + almacen_origen + '/';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url_stock);
        xhr.onload = function(){
            if (this.status === 200) {
                $respuesta = xhr.responseText;
            }else{
                $respuesta = '0.00';
            }
            stock_disponible.value = $respuesta;
        }
        xhr.send();
    }
}

function ver_stock_tipo_stock() {
    material = $('#id_material')[0].value;
    almacen_origen = $('#id_almacen')[0].value;
    tipo_stock = $('#id_tipo_stock')[0].value;
    if (!tipo_stock) {
        ver_stock();
    } else {
        stock_disponible = $('#id_stock_disponible')[0];
        if (material && almacen_origen) {
            sociedad = $('#sociedad')[0].innerHTML;
            url_stock_tipo_stock = $('#url_stock')[0].innerHTML + 'tipo_stock/' + material + '/' + sociedad + '/' + almacen_origen + '/' + tipo_stock + '/';
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url_stock_tipo_stock);
            xhr.onload = function(){
                if (this.status === 200) {
                    $respuesta = xhr.responseText;
                }else{
                    $respuesta = '0.00';
                }
                console.log($respuesta);
                stock_disponible.value = $respuesta;
            }
            xhr.send();
        }
    }
}

$('#id_material').unbind().on('change', function (e) {
    ver_stock();
})

$('#id_almacen').unbind().on('change', function () {
    ver_stock_tipo_stock();
})

$('#id_tipo_stock').unbind().on('change', function () {
    ver_stock_tipo_stock();
})

ver_stock_tipo_stock();

function select_form() {
    combos = document.getElementsByClassName('select2');
    for (let index = 0; index < combos.length; index++) {
        const element = combos[index];
        element.className = element.className.replace('select2-container--default select2-container--focus', 'form-control');
        element.className = element.className.replace('select2-container--default', 'form-control');
        element.className = element.className.replace('select2-container--focus', '');
        element.className = element.className.replace('select2-selection--single', '');
    }
}

setTimeout(() => {
    select_form();
}, 500);