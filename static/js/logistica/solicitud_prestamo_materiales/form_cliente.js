function seleccionar_cliente(id_cliente) {
    $interlocutor = $('#id_interlocutor_cliente')[0];
    
    url = '/logistica/cliente-interlocutor/' + id_cliente + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $interlocutor.innerHTML = xmlDoc.getElementById('id_interlocutor_cliente').innerHTML;
            console.log($interlocutor.innerHTML)
        }else{
            console.log('error')
        }
    }
    xhr.send();
}

$(document).on('change', '#id_cliente', function (e) {
    seleccionar_cliente(e.target.value);
})
