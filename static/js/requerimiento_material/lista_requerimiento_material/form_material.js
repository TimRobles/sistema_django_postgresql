function elegir_material(material) {
    url = $('#url_material')[0].innerHTML;
    unidad = $('#id_unidad')[0];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url + material);
    xhr.onload = function(){
        if (this.status === 200) {
            $respuesta = JSON.parse(xhr.responseText);
            unidad.value = $respuesta['unidad_base']
        }else{
            $respuesta = false;
        }
    }
    xhr.send();
}

$('#id_material').unbind().on('change', function (e) {
    console.log(e.target.value);
    elegir_material(e.target.value);
})