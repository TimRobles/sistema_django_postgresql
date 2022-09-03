function seleccionar_precio_lista(id_material) {
    $precio_lista= $('#id_precio_lista')[0];
    
    url = '/material/precio-lista/' + id_material + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = xhr.responseText;
            $precio_lista.value = info;
            console.log(info)
        }else{
            console.log('error')
        }
    }
    xhr.send();
}

$(document).unbind().on('change', '#id_material', function (e) {
    seleccionar_precio_lista(e.target.value);
})

// console.log('hola')