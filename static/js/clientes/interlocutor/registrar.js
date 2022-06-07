function ConsultarDni() {
    $dni = $('#id_numero_documento')[0].value;
    $nombre = $('#id_nombre_completo')[0];
    $boton = $('#consultar-dni')[0];
    
    url = '/consulta-dni/' + $dni;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"').replace(/&amp;/g,'&'));

            $nombre.value = $info['nombre_completo'];
        }else{
            $respuesta = false;
            $nombre.value = "";
            console.log("Error")
            swal({
                title: "¡DNI inválido!",
                text: "Ingrese un número de DNI correcto",
                icon: "warning",
              });
        }
        $boton.innerHTML = 'Consultar DNI';
        $boton.disabled = false;
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
    e.target.innerHTML = spinnerText;
    e.target.disabled = true;
    ConsultarDni();
});
habilitar();