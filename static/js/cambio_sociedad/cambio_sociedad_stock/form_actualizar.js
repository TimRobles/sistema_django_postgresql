function cambiar_sociedad(id_sociedad) {
    sede = $('#id_sede')[0]
    url = $('#url_sede')[0].innerHTML + id_sociedad;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            sede.innerHTML = $respuesta['info'];
        }else{
            $respuesta = false;
        }
    }
    xhr.send();
}

$('#id_sociedad_inicial').unbind().on('change', function (e) {
    cambiar_sociedad(e.target.value);
})