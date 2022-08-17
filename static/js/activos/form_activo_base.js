function seleccionar_familia(id_familia) {
    $subfamilia = $('#id_sub_familia')[0];
    
    url = '/activos/subfamilia_activo/' + id_familia + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $subfamilia.innerHTML = xmlDoc.getElementById('id_sub_familia').innerHTML;
            seleccionar_subfamilia($subfamilia.value);
        }
    }
    xhr.send();
}

$('#id_familia').on('change', function (e) {
    seleccionar_familia(e.target.value);
})
