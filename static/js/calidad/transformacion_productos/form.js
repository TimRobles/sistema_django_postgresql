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
            $almacen.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_sede').unbind().on('change', function (e) {
    if (e.target.value) {
        cambiar_sede(e.target.value);
    } else {
        $('#id_almacen')[0].innerHTML = '<option value="" selected="">---------</option>';
    }
})