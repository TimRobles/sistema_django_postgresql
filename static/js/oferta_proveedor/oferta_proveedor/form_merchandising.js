function elegir_merchandising(merchandising) {
    url = $('#url_merchandising')[0].innerHTML;
    unidad = $('#id_unidad')[0];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url + merchandising);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            if ($respuesta['unidad']) {
                unidad.value = $respuesta['unidad']
            } else {
                unidad.value = $respuesta['producto-info']['unidad_base']
            }
        }else{
            $respuesta = false;
        }
    }
    xhr.send();
}

$('#id_merchandising').unbind().on('change', function (e) {
    console.log(e.target.value);
    elegir_merchandising(e.target.value);
})