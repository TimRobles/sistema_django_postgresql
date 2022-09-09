igv = $('#igv')[0].innerHTML;
contador = 0;
inputs = document.getElementsByTagName('input');

function inicio() {
    if (document.getElementById('descuentos')) {
        descuentos = document.getElementById('descuentos').innerHTML;
        var contador = 0;
        var indice = 0;
        for (let index = 1; index < inputs.length; index++) {
            const element = inputs[index];
            if (contador == 1) {
                contador--;
            }else {
                contador++;
                element.value = descuentos.split('|')[indice];
                indice++;
            }
        }
        calcular_con_igv();
    }
}

function calcular_sin_igv() {
    var contador = 0;
    for (let index = 1; index < inputs.length; index++) {
        const element_con_igv = inputs[index];
        if (contador == 1) {
            contador--;
            const element_sin_igv = inputs[index-1];
            if (element_con_igv.value != "") {
                con_igv = parseFloat(element_con_igv.value);
            } else {
                con_igv = 0;
            }
            element_sin_igv.value = Math.round(100 * con_igv / (1 + parseFloat(igv)))/100;
        }else {
            contador++;
        }
    }
}

function calcular_con_igv() {
    var contador = 0;
    for (let index = 1; index < inputs.length; index++) {
        const element_sin_igv = inputs[index];
        if (contador == 1) {
            contador--;
        }else {
            contador++;
            const element_con_igv = inputs[index+1];
            if (element_sin_igv.value != "") {
                sin_igv = parseFloat(element_sin_igv.value);
            } else {
                sin_igv = 0;
            }
            element_con_igv.value = Math.round(sin_igv * 100 * (1 + parseFloat(igv)))/100;
        }
    }
}
for (let index = 1; index < inputs.length; index++) {
    const element = inputs[index];
    if (contador == 1) {
        contador--;
        element.addEventListener('input', calcular_sin_igv);
    }else {
        contador++;
        element.addEventListener('input', calcular_con_igv);
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