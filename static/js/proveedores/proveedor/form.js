function ConsultarRuc() {
    $ruc = $('#id_ruc')[0].value;
    $razon_social = $('#id_nombre')[0];
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

$(document).unbind().on('click', '#consultar-documento', function (e) {
    e.target.innerHTML = spinnerText;
    e.target.disabled = true;
    ConsultarRuc();
});