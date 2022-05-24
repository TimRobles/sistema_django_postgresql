function seleccionar_segmento(id_segmento) {
    $familia = $('#id_familia_sunat')[0];
    
    url = '/material/familia-sunat/' + id_segmento + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $familia.innerHTML = xmlDoc.getElementById('id_familia').innerHTML;

            seleccionar_familia($familia);
        }
    }
    xhr.send();
}

$('#id_segmento_sunat').on('change', function (e) {
    seleccionar_segmento(e.target.value);
})

function seleccionar_familia(id_familia) {
    $clase = $('#id_clase_sunat')[0];
    
    url = '/material/clase-sunat/' + id_familia + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $clase.innerHTML = xmlDoc.getElementById('id_clase').innerHTML;
        }else{
            $clase.innerHTML = '<option value="" selected="">---------</option>';
        }
        seleccionar_clase($clase);
    }
    xhr.send();
}

$('#id_familia_sunat').on('change', function (e) {
    seleccionar_familia(e.target.value);
})

function seleccionar_clase(id_clase) {
    $producto = $('#id_producto_sunat')[0];
    
    url = '/material/producto-sunat/' + id_clase + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $producto.innerHTML = xmlDoc.getElementById('id_producto').innerHTML;
        }else{
            $producto.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_clase_sunat').on('change', function (e) {
    seleccionar_clase(e.target.value);
})