function seleccionar_proveedor(id_proveedor) {
    $interlocutor = $('#id_interlocutor_temporal')[0];
    
    url = '/requerimiento-material/proveedor-interlocutor/' + id_proveedor + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $interlocutor.innerHTML = xmlDoc.getElementById('id_interlocutor_proveedor').innerHTML;
            console.log($interlocutor.innerHTML)
        }else{
            console.log('error')
        }
    }
    xhr.send();
}

$(document).on('change', '#id_proveedor_temporal', function (e) {
    seleccionar_proveedor(e.target.value);
})

seleccionar_proveedor($('#id_proveedor_temporal')[0].value);