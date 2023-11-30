function ver_stock() {
    merchandising = $('#id_merchandising')[0].value;
    stock_disponible = $('#id_stock_disponible')[0];
    if (merchandising) {
        url_stock = $('#url_stock')[0].innerHTML + merchandising + '/';
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

$('#id_merchandising').unbind().on('change', function (e) {
    ver_stock();
})

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