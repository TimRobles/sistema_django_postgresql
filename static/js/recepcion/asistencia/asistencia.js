function CambioSede(elemento) {
    $id_sede = elemento.value;
    longitud = $('#id_longitud')[0].value;
    latitud = $('#id_latitud')[0].value;
    url = '/distancia-geolocalizacion/' + longitud + "/" + latitud + "/" + $id_sede;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $('#confirmar')[0].innerHTML = xhr.responseText;
        }
    }
    xhr.send();
}

$('#id_sede').on('change', function (e) {
    CambioSede(e.target);
})

function Ubicacion() {
    function success(position) {
        $('#id_longitud')[0].value = position.coords.longitude;
        $('#id_latitud')[0].value = position.coords.latitude;
    }
    
    function error() {
        $('#id_longitud')[0].value = 0;
        $('#id_latitud')[0].value = 0;
    }
    
    if(!navigator.geolocation) {
        $('#id_longitud')[0].value = 0;
        $('#id_latitud')[0].value = 0;
    } else {
        navigator.geolocation.getCurrentPosition(success, error);
    }
}

Ubicacion();
setTimeout(() => {
    CambioSede($('#id_sede')[0]);
}, 100);