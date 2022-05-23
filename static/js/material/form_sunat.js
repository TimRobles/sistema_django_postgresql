function seleccionar_segmento(id_segmento) {
    $familia = $('#id_familia_sunat')[0];
    
    url = '/material/familia-sunat/' + id_segmento + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
            $familia.innerHTML = xmlDoc.getElementById('id_familia').innerHTML;
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
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
            $clase.innerHTML = xmlDoc.getElementById('id_clase').innerHTML;
        }
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
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
            $producto.innerHTML = xmlDoc.getElementById('id_producto').innerHTML;
        }
    }
    xhr.send();
}

$('#id_clase_sunat').on('change', function (e) {
    seleccionar_clase(e.target.value);
})