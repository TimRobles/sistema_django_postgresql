textareas = document.getElementsByTagName('textarea');

function inicio() {
    if (document.getElementById('observaciones')) {
        observaciones = document.getElementById('observaciones').innerHTML;
        console.log(observaciones);
        for (let index = 0; index < textareas.length; index++) {
            const element = textareas[index];
            element.value = observaciones.split('|')[index];
        }
    }
}

$('#modal').unbind().on('shown.bs.modal', function (e) {
    inicio();
});

function guardar() {
    url = $('#url_guardar')[0].innerHTML;
    var contador = 0;
    for (let index = 0; index < textareas.length; index++) {
        const element = textareas[index];
        if (element.value=="") {
            texto = null;
        } else {
            texto = encodeURIComponent(element.value);
        }
        id_cotizacion = element.name;
        sociedad = element.id;
        url_final = url + texto + '/' + id_cotizacion + '/' + sociedad + '/'
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

$('#guardar_formulario').unbind().on('click', function (e) {
    guardar();
});