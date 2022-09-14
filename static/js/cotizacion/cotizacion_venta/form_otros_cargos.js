igv = $('#igv')[0].innerHTML;
contador = 0;
inputs = document.getElementsByTagName('input');

function inicio() {
    if (document.getElementById('otros_cargos')) {
        otros_cargos = document.getElementById('otros_cargos').innerHTML;
        for (let index = 1; index < inputs.length; index++) {
            const element = inputs[index];
            element.value = otros_cargos.split('|')[index-1];
        }
    }
}

$('#modal').unbind().on('shown.bs.modal', function (e) {
    inicio();
});

function guardar() {
    url = $('#url_guardar')[0].innerHTML;
    var contador = 0;
    for (let index = 1; index < inputs.length; index++) {
        const element = inputs[index];
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

$('#guardar_formulario').unbind().on('click', function (e) {
    guardar();
});