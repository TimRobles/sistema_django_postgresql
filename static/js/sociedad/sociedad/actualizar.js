function ConsultarRuc() {
    $ruc = $('#id_ruc')[0].value;
    $razon_social = $('#id_razon_social')[0];
    $nombre_comercial= $('#id_nombre_comercial')[0];
    $direccion = $('#id_direccion_legal')[0];
    $ubigeo = $('#id_ubigeo')[0];
    $estado = $('#id_estado_sunat')[0];
    $condicion = $('#id_condicion_sunat')[0];
    $boton = $('#consultar-ruc')[0];

    url = '/consulta-ruc/' + $ruc;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            $info = JSON.parse($respuesta['info'].replace(/&quot;/g,'"'));

            $razon_social.value = $info['razon_social'];
            $direccion.value = $info['direccion'];
            $ubigeo.value = $info['ubigeo'];
            setSelectedValueText($estado, $info['estado']);
            setSelectedValueText($condicion, $info['condicion']);
        }else{
            $respuesta = false;
            $razon_social.value = "";
            $nombre_comercial.value = "";
            $direccion.value = "";
            $ubigeo.value = "";
            setSelectedValueText($estado, "---------");
            setSelectedValueText($condicion, "---------");
            console.log("Error")
            swal({
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

$(document).unbind().on('click', '#consultar-ruc', function (e) {
    e.target.innerHTML = spinnerText;
    e.target.disabled = true;
    ConsultarRuc();
});

