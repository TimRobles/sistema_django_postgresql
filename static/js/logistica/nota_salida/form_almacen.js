function seleccionar_sede(id_sede) {
    $almacen = $('#id_almacen')[0];
    
    if (id_sede=="") {
        url = '/logistica/almacen/0/';
        
    } else {
        url = '/logistica/almacen/' + id_sede + '/';
        
    }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $almacen.innerHTML = xmlDoc.getElementById('id_almacen').innerHTML;
        }else {
            $almacen.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_sede').on('change', function (e) {
    seleccionar_sede(e.target.value);
})