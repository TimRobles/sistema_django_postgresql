
function seleccionar_activo(id_asignacion) {
    $activo = $('#id_activo')[0];
    
    url = '/activos/devolucion_activo/asignacion/' + id_asignacion + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function(){
        if (this.status === 200) {
            info = JSON.parse(xhr.responseText)['info'];
            var parser, xmlDoc;
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(info, "text/xml");
            $activo.innerHTML = xmlDoc.getElementById('id_activo').innerHTML;
        }else{
            $activo.innerHTML = '<option value="" selected="">---------</option>';
        }
    }
    xhr.send();
}

$('#id_asignacion').on('change', function (e) {
    seleccionar_activo(e.target.value);
})