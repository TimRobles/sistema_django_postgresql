function ConsultarRuc() {
    $ruc = $('#id_numero_documento')[0].value;
    $razon_social = $('#id_razon_social')[0];
    $nombre_comercial= $('#id_nombre_comercial')[0];
    $direccion_fiscal = $('#id_direccion_fiscal')[0];
    $ubigeo = $('#id_ubigeo')[0];
    $estado = $('#id_estado_sunat')[0];
    $condicion = $('#id_condicion_sunat')[0];
    $boton = $('#consultar-documento')[0];

    url = '/consulta-ruc/' + $ruc;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"').replace(/&amp;/g,'&'));

            $razon_social.value = $info['razon_social'];
            $direccion_fiscal.value = $info['direccion'];
            $ubigeo.value = $info['ubigeo'];
            setSelectedValueText($estado, $info['estado']);
            setSelectedValueText($condicion, $info['condicion']);
        }else{
            $respuesta = false;
            $razon_social.value = "";
            $nombre_comercial.value = "";
            $direccion_fiscal.value = "";
            $ubigeo.value = "";
            setSelectedValueText($estado, "---------");
            setSelectedValueText($condicion, "---------");
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
    $dni = $('#id_numero_documento')[0].value;
    $nombre = $('#id_razon_social')[0];
    $boton = $('#consultar-documento')[0];
    
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
    $tipo_documento = $('#id_tipo_documento')[0].value;
    $numero_documento = $('#id_numero_documento')[0];
    $boton = $('#consultar-documento')[0];
    $numero_documento.required = true;
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
        $numero_documento.required = false;
        $numero_documento.disabled = true;
    } else {
        $boton.hidden = true;
    };   
}

$('#id_tipo_documento').change(function (e) {
    console.log(e);
    habilitar();
});

habilitar();

$('#id_distrito').change(function (e) {
    $('#id_ubigeo')[0].value = e.target.value;
})