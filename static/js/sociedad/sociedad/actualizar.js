function ConsultarRuc() {
    $ruc = $('#ruc')[0].value;
    $razon_social = $('#id_razon_social')[0];
    $direccion = $('#id_direccion_legal')[0];
    $ubigeo = $('#id_ubigeo')[0];
    $estado = $('#id_estado_sunat')[0];
    $condicion = $('#id_condicion_sunat')[0];
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
            console.log("Error")
        }
    }
    xhr.send();
}

$(document).unbind().on('click', '#consultar-ruc', function (e) {
    ConsultarRuc();
});

