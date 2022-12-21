$id_sociedad = $('#id_sociedad')[0].innerHTML;
$id_material = $('#id_material')[0].innerHTML;

url = '/material/stock/' + $id_material + '/' + $id_sociedad + '/';

var xhr = new XMLHttpRequest();
xhr.open('GET', url);
xhr.onload = function(){
    if (this.status === 200) {
        $stock = xhr.responseText;
    }else{
        $stock = 0;
    }
}
xhr.send();

function seleccionar_sede(id_sede) {
    $almacen = $('#id_almacen')[0];
    url = '/logistica/almacen/' + id_sede + '/';
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $almacen.innerHTML = xmlDoc.getElementById('id_almacen').innerHTML;
        }else {
            $almacen.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_sede').on('change', function (e) {
    if (e.target.value) {
        seleccionar_sede(e.target.value);
    } else {
        $('#id_stock')[0].value = $stock;
        $('#id_almacen')[0].innerHTML = '<option value="" selected="">---------</option>';
    }
})

function seleccionar_almacen(id_almacen) {
    $id_stock = $('#id_stock')[0];
    url = '/material/stock/' + $id_material + '/' + $id_sociedad + '/' + id_almacen + '/';
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $id_stock.value = xhr.responseText;
        }else {
            $id_stock.value = 0;
        }
    }
    xhr.send();
}

$('#id_almacen').on('change', function (e) {
    if (e.target.value) {
        seleccionar_almacen(e.target.value);
    } else {
        $('#id_stock')[0].value = $stock;
    }
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
    select_form();
}, 500);