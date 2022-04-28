function ConsultarDni() {
    $dni = $('#id_numero_documento')[0].value;
    $nombre = $('#id_nombre')[0];
    
    url = '/consulta-dni/' + $dni;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"'));

            $nombre.value = $info['nombre_completo'];
        }else{
            $respuesta = false;
            console.log("Error")
        }
    }
    xhr.send();
}

function habilitar() {
    $tipo_documento = $('#id_tipo_documento')[0].value;
    $boton = $('#consultar-dni')[0];
    if ($tipo_documento == 1) {
        $boton.hidden = false;
    } else {
        $boton.hidden = true;
    }
}

$('#id_tipo_documento').change(function (e) {
    console.log(e);
    habilitar();
});

$(document).unbind().on('click', '#consultar-dni', function (e) {
    ConsultarDni();
});
habilitar();