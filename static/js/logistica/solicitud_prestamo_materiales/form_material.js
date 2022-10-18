function seleccionar_material(id_material) {
    $stock = $('#id_stock')[0];
    id_sociedad = $('#id_sociedad')[0].innerHTML;

    url = '/material/stock/' + id_material + '/' + id_sociedad + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $stock.value = xhr.responseText;
        }else{
            $stock.value = 0;
        }
    }
    xhr.send();
}

$(document).on('change', '#id_material', function (e) {
    if (e.target.value) {
        seleccionar_material(e.target.value);
    }else{
        $('#id_stock')[0].value = 0;
    }
})

if ($('#id_material')[0].value) {
    seleccionar_material($('#id_material')[0].value);
}

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