$id_sociedad = $('#id_sociedad')[0].innerHTML;
$id_material = $('#id_material')[0].value;
// var material_selected = document.getElementById('id_material'); // ¿es necesario?
// $id_material = material_selected.value;                         // ¿es necesario?
$url_stock = $('#url_stock')[0].innerHTML;

url = $url_stock + $id_material + '/' + $id_sociedad + '/';
console.log(url);

var xhr = new XMLHttpRequest();
xhr.open('GET', url);
xhr.onload = function(){
    if (this.status === 200) {
        console.log(xhr.responseText);
        $stock = xhr.responseText;
    }else{
        $stock = 0;
    console.log($stock);
    }
}
xhr.send();


function seleccionar_sede(id_sede) {
    $almacen = $('#id_almacen')[0];
    
    url = '/logistica/almacen/' + id_sede + '/';
    // url = '/calidad/almacen_solicitud_consumo_detalle/' + id_sede + '/';
    // console.log(url)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            // console.log(info)
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $almacen.innerHTML = xmlDoc.getElementById('id_almacen').innerHTML;
        }else {
            $almacen.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();

    $id_stock = $('#id_stock')[0];
    url = $url_stock + 'sede/' + $id_material + '/' + $id_sociedad + '/' + id_sede + '/';
    
    var xhr2 = new XMLHttpRequest();
    xhr2.open('GET', url);
    xhr2.onload = function(){
        if (this.status === 200) {
            $id_stock.value = xhr2.responseText;
        }else {
            $id_stock.value = 0;
        }
    }
    xhr2.send();
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
    url = $url_stock + $id_material + '/' + $id_sociedad + '/' + id_almacen + '/';
    
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


function seleccionar_material(id_material) {
    $unidad = $('#id_unidad')[0];
    
    url = '/calidad/solicitud-consumo-interno/material-unidad/' + id_material + '/';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $unidad.innerHTML = xmlDoc.getElementById('id_unidad').innerHTML;
        }else {
            $unidad.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();

    // var material_selected = document.getElementById('id_material'); // ¿es necesario?
    // $id_material = material_selected.value;                         // ¿es necesario?
    $id_material = $('#id_material')[0].value;
    $id_stock = $('#id_stock')[0];
    url = $url_stock + $id_material + '/' + $id_sociedad + '/';
    
    var xhr2 = new XMLHttpRequest();
    xhr2.open('GET', url);
    xhr2.onload = function(){
        if (this.status === 200) {
            $id_stock.value = xhr2.responseText;
        }else {
            $id_stock.value = 0;
        }
    }
    xhr2.send();
}

$('#id_material').on('change', function (e) {
    if (e.target.value) {
        seleccionar_material(e.target.value);
    } else {
        $('#id_stock')[0].value = $stock;
    }
})
