function CambioSede(elemento) {
    $id_sede = elemento.value;
    url = '/recepcion/confirmar-sede/' + $id_sede;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            $('#confirmar')[0].innerHTML = xhr.responseText;
        }
    }
    xhr.send();
}

$('#id_sede').on('change', function (e) {
    CambioSede(e.target);
})