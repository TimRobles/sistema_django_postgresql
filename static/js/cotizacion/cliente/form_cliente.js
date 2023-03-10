function seleccionar_interlocutor(id_cliente) {
    $interlocutor = $('#id_cliente_interlocutor')[0];
    
    url = '/cotizacion/cotizacion-cliente-interlocutor/' + id_cliente + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $interlocutor.innerHTML = xmlDoc.getElementById('id_cliente_interlocutor').innerHTML;
            console.log($interlocutor.innerHTML)
        }else{
            $interlocutor.innerHTML = '<option value="" selected="">---------</option>';
            console.log('error')
        }
    }
    xhr.send();
}

$(document).on('change', '#id_cliente', function (e) {
    seleccionar_interlocutor(e.target.value);
})