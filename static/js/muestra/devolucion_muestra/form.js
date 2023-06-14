function ver_stock() {
    producto = $('#id_producto')[0].value;
    sede = $('#sede')[0].innerHTML;
    tipo_stock = $('#tipo_stock')[0].innerHTML;
    stock_disponible = $('#id_stock_disponible')[0];
    if (producto && sede) {
        sociedad = $('#sociedad')[0].innerHTML;
        url_stock = '/material/stock/sede/' + producto.split('|')[1] + '/' + sociedad + '/' + sede + '/' + tipo_stock + '/';
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

function ver_stock_almacen() {
    producto = $('#id_producto')[0].value;
    almacen = $('#id_almacen')[0].value;
    tipo_stock = $('#tipo_stock')[0].innerHTML;
    if (!almacen) {
        ver_stock();
    } else {
        stock_disponible = $('#id_stock_disponible')[0];
        if (producto && almacen) {
            sociedad = $('#sociedad')[0].innerHTML;
            url_stock_almacen = '/material/stock/tipo_stock/' + producto.split('|')[1] + '/' + sociedad + '/' + almacen + '/' + tipo_stock + '/';
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url_stock_almacen);
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

$('#id_producto').unbind().on('change', function (e) {
    ver_stock();
})

$('#id_almacen').unbind().on('change', function () {
    ver_stock_almacen();
})

ver_stock_almacen();

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