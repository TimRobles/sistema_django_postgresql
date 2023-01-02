function seleccionar_material(id_material) {
    $precio_lista= $('#id_precio_lista')[0];
    $stock= $('#id_stock')[0];
    
    url = '/material/precio-lista/' + id_material + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = xhr.responseText;
            $precio_lista.value = info;
            console.log(info)
        }else{
            console.log('error')
            $precio_lista.value = '';
        }
    }
    xhr.send();
    
    url = '/material/stock/' + id_material + '/';

    var xhr2 = new XMLHttpRequest();
    xhr2.open('GET', url);
    xhr2.onload = function(){
        if (this.status === 200) {
            info = xhr2.responseText;
            $stock.value = info;
            console.log(info)
        }else{
            console.log('error');
            $stock.value = '';
        }
    }
    xhr2.send();
}

$(document).unbind().on('change', '#id_material', function (e) {
    seleccionar_material(e.target.value);
})

$('#id_precio_lista')[0].disabled = true;

$('.btn-primary-submit').unbind().on('click', function () {
    $precio_lista = $('#id_precio_lista')[0];
    console.log($precio_lista);
    $precio_lista.disabled = false;
})

function select_form() {
    combos = document.getElementsByClassName('select2');
    for (let index = 0; index < combos.length; index++) {
        const element = combos[index];
        element.className = element.className.replace('select2-container--default select2-container--focus', 'form-control');
        element.className = element.className.replace('select2-container--default', 'form-control');
    }
}

setTimeout(() => {
    console.log('select_form prueb<')
    select_form();
}, 500);