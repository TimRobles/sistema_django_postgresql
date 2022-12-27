function ConsultarRuc() {
    $ruc = $('#id_conductor_numero_documento')[0].value;
    $razon_social = $('#id_conductor_denominacion')[0];
    $boton = $('#consultar-documento')[0];

    url = '/consulta-ruc/' + $ruc;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"').replace(/&amp;/g,'&'));

            $razon_social.value = $info['razon_social'];
        }else{
            $respuesta = false;
            $razon_social.value = "";
            console.log("Error")
            Swal.fire({
                title: "¡RUC inválido!",
                text: "Ingrese un número de RUC correcto",
                icon: "warning",
              });
        }
        $boton.innerHTML = 'Consultar Ruc';
        $boton.disabled = false;
    }
    xhr.send();
}

function ConsultarDni() {
    $dni = $('#id_conductor_numero_documento')[0].value;
    $nombre = $('#id_conductor_nombre')[0];
    $apellidos = $('#id_conductor_apellidos')[0];
    $boton = $('#consultar-documento')[0];
    
    url = '/consulta-dni/' + $dni;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"').replace(/&amp;/g,'&'));

            $nombre.value = $info['nombre'];
            $apellidos.value = $info['apellidos'];
        }else{
            $respuesta = false;
            $nombre.value = "";
            $apellidos.value = "";
            console.log("Error")
            Swal.fire({
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
    $tipo_documento = $('#id_conductor_tipo_documento')[0].value;
    $numero_documento = $('#id_conductor_numero_documento')[0];
    $boton = $('#consultar-documento')[0];
    $numero_documento.disabled = false;
    if ($tipo_documento == 6 ) {
        $boton.hidden = false;
        $(document).unbind().on('click', '#consultar-documento', function (e) {
            e.target.innerHTML = spinnerText;
            e.target.disabled = true;
            ConsultarRuc();
        });
    } else if ($tipo_documento == 1 ) {
        $boton.hidden = false;
        $(document).unbind().on('click', '#consultar-documento', function (e) {
            e.target.innerHTML = spinnerText;
            e.target.disabled = true;
            ConsultarDni();
        });
    } else if ($tipo_documento == '-' ) {
        $boton.hidden = true;
        $numero_documento.disabled = true;
    } else {
        $boton.hidden = true;
    };   
}

$('#id_conductor_tipo_documento').change(function (e) {
    console.log(e);
    habilitar();
});

habilitar();