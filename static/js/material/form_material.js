function seleccionar_familia(id_familia) {
    $subfamilia = $('#id_subfamilia')[0];
    
    url = '/material/subfamilia/' + id_familia + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $subfamilia.innerHTML = xmlDoc.getElementById('id_subfamilia').innerHTML;
            seleccionar_subfamilia($subfamilia.value);
        }
    }
    xhr.send();
}

$('#id_familia').on('change', function (e) {
    seleccionar_familia(e.target.value);
})

function seleccionar_subfamilia(id_subfamilia) {
    $unidad = $('#id_unidad_base')[0];
    
    url = '/material/unidad/' + id_subfamilia + '/';

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

$('#id_subfamilia').on('change', function (e) {
    seleccionar_subfamilia(e.target.value);
})

function seleccionar_marca(id_marca) {
    $modelo = $('#id_modelo')[0];
    
    url = '/material/modelo/' + id_marca + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $modelo.innerHTML = xmlDoc.getElementById('id_modelo').innerHTML;
        }else {
            $modelo.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_marca').on('change', function (e) {
    seleccionar_marca(e.target.value);
})