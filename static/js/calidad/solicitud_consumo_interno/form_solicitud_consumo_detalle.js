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
}

$('#id_sede').on('change', function (e) {
    seleccionar_sede(e.target.value);
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
}

$('#id_material').on('change', function (e) {
    seleccionar_material(e.target.value);
})