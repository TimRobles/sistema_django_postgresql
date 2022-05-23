function seleccionar_familia(id_familia) {
    $subfamilia = $('#id_subfamilia')[0];
    
    url = '/material/subfamilia/' + id_familia + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
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
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
            $unidad.innerHTML = xmlDoc.getElementById('id_unidad').innerHTML;
        }else if (this.status === 404) {
            console.log("No encontrado")
            $unidad.innerHTML = "";
        }
    }
    xhr.send();
}

$('#id_subfamilia').on('change', function (e) {
    seleccionar_subfamilia(e.target.value);
})