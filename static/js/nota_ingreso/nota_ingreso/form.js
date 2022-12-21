function cambiar_sede(id_sede) {
    almacen = $('#id_almacen')[0]
    url_sede = $('#url_sede')[0].innerHTML + id_sede;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url_sede);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            almacen.innerHTML = $respuesta['info'];
        }else{
            $respuesta = false;
        }
    }
    xhr.send();
}

$('#id_sede').unbind().on('change', function (e) {
    cambiar_sede(e.target.value);
})