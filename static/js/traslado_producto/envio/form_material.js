function ver_stock() {
    material = $('#id_material')[0].value;
    almacen_origen = $('#id_almacen_origen')[0].value;
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

function cambiar_unidad(id_material) {
    unidad = $('#id_unidad')[0];
    url_unidad = $('#url_unidad')[0].innerHTML + material;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url_unidad);
    xhr.onload = function(){
        if (this.status === 200) {
            console.log(xhr.responseText)
            $respuesta = JSON.parse(xhr.responseText)['info'];
        }else{
            $respuesta = '---------';
        }
        unidad.innerHTML = $respuesta;
    }
    xhr.send();
}

$('#id_material').unbind().on('change', function (e) {
    ver_stock();
    cambiar_unidad(e.target.value);
})

$('#id_almacen_origen').unbind().on('change', function () {
    ver_stock();
})

ver_stock();

function select_form() {
    combos = document.getElementsByClassName('select2');
    for (let index = 0; index < combos.length; index++) {
        const element = combos[index];
        element.className = element.className.replace('select2-container--default select2-container--focus', 'form-control');
        element.className = element.className.replace('select2-container--default', 'form-control');
    }
}

$('.btn-primary').unbind().on('click', function () {
    setTimeout(() => {
        select_form();
    }, 500);
})

setTimeout(() => {
    select_form();
}, 500);