textareas = document.getElementsByTagName('textarea');

function inicio() {
    if (document.getElementById('observaciones')) {
        observaciones = document.getElementById('observaciones').innerHTML;
        var contador = 0;
        var indice = 0;
        for (let index = 1; index < textareas.length; index++) {
            const element = textareas[index];
            if (contador == 1) {
                contador--;
            }else {
                contador++;
                element.value = observaciones.split('|')[indice];
                indice++;
            }
        }
    }
}

$('#modal').unbind().on('shown.bs.modal', function (e) {
    inicio();
});

function guardar() {
    url = $('#url_guardar')[0].innerHTML;
    var contador = 0;
    for (let index = 1; index < textareas.length; index++) {
        const element = textareas[index];
        if (contador == 1) {
            contador--;
        }else {
            contador++;
            if (element.value != "") {
                monto = parseFloat(element.value);
            } else {
                monto = 0;
            }
            id_cotizacion = element.name;
            sociedad = element.id;
            url_final = url + monto + '/' + id_cotizacion + '/' + sociedad + '/'
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url_final);
            xhr.onload = function(){
                if (this.status === 200) {
                    setTimeout(() => {
                        inicio();
                    }, 1000);
                }
            }
            xhr.send();
        }
    }
}

$('#guardar_formulario').unbind().on('click', function (e) {
    guardar();
});