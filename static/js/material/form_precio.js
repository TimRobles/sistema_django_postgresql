function seleccionar_comprobante(id_comprobante) {
    console.log(id_comprobante);
    // $subfamilia = $('#id_subfamilia')[0];
    
    // url = '/material/subfamilia/' + id_familia + '/';

    // var xhr = new XMLHttpRequest();
    // xhr.open('GET', url);
    // xhr.onload = function(){
    //     if (this.status === 200) {
    //         info = JSON.parse(xhr.responseText)['info'];
    //         var parser, xmlDoc;
    //         parser = new DOMParser();
    //         xmlDoc = parser.parseFromString(info, "text/xml");
    //         $subfamilia.innerHTML = xmlDoc.getElementById('id_subfamilia').innerHTML;
    //         seleccionar_subfamilia($subfamilia.value);
    //     }
    // }
    // xhr.send();
}

$('#id_comprobante').on('change', function (e) {
    seleccionar_comprobante(e.target.value);
})

seleccionar_comprobante($('#id_comprobante')[0].value);