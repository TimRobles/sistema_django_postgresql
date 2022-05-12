function ConsultarDepartamento(id_departamento) {
    $provincia = $('#id_provincia_buscar')[0];
    
    url = '/datos_globales/provincia/' + id_departamento + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            console.log(xhr.responseText);
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
            $provincia.innerHTML = xmlDoc.getElementById('id_provincia').innerHTML;

            ConsultarProvincia($provincia.value);
        }
    }
    xhr.send();
}

function ConsultarProvincia(id_provincia) {
    $distrito = $('#id_distrito_buscar')[0];
    
    url = '/datos_globales/distrito/' + id_provincia + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhr.responseText, "text/xml");
            $distrito.innerHTML = xmlDoc.getElementById('id_distrito').innerHTML;
            
            MostrarUbigeo($distrito);
        }
    }
    xhr.send();
}

function MostrarUbigeo(e) {
    $ubigeo = $('#id_ubigeo')[0];
    $ubigeo.value = e.value;
}

$('#id_departamento_buscar').on('change', function (e) {
    ConsultarDepartamento(e.target.value);
})

$('#id_provincia_buscar').on('change', function (e) {
    ConsultarProvincia(e.target.value);
})

$('#id_distrito_buscar').on('change', function (e) {
    MostrarUbigeo(e.target);
})