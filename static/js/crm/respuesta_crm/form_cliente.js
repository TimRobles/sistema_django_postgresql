function seleccionar_interlocutor(id_cliente_crm) {
    $interlocutor = $('#id_interlocutor')[0];
    
    url = '/cotizacion/cotizacion-cliente-interlocutor/' + id_cliente_crm + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $interlocutor.innerHTML = xmlDoc.getElementById('id_interlocutor').innerHTML;
            console.log($interlocutor.innerHTML)
            console.log("hola")
        }else{
            $interlocutor.innerHTML = '<option value="" selected="">---------</option>';
            console.log('error')
        }
    }
    xhr.send();
}

$(document).on('change', '#id_cliente_crm', function (e) {
    seleccionar_interlocutor(e.target.value);
})